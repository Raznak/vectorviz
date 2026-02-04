from fastapi import APIRouter, HTTPException, status
from urllib3.exceptions import NewConnectionError
from core.settings import settings
from core.log import logger
from const import query
import requests
import yaml

router = APIRouter()


def _load_config_map():
    if not settings.VECTOR_CONFIG_MAP_PATH:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="VECTOR_CONFIG_MAP_PATH is required",
        )

    try:
        with open(settings.VECTOR_CONFIG_MAP_PATH, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except FileNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config map file not found: {settings.VECTOR_CONFIG_MAP_PATH}",
        ) from err
    except OSError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read config map file: {settings.VECTOR_CONFIG_MAP_PATH}",
        ) from err

    if not isinstance(data, dict):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Config map must be a YAML mapping",
        )

    instances = []
    for name, entry in data.items():
        if not isinstance(entry, dict):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Config map entry '{name}' must be a mapping",
            )

        url = entry.get("url")
        if not url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Config map entry '{name}' must define url",
            )

        instances.append(
            {
                "name": name,
                "url": url,
                "config_file": entry.get("config_file"),
                "config": entry.get("config"),
            }
        )

    return instances


def _get_config_source(url: str):
    config_map = _load_config_map()
    for inst in config_map:
        if inst["url"] == url:
            return inst
    return None


def _load_vector_config(url: str):
    source = _get_config_source(url)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No config path found for {url}",
        )

    if source.get("config") is not None:
        if isinstance(source["config"], dict):
            return source["config"]
        if isinstance(source["config"], str):
            return yaml.safe_load(source["config"]) or {}
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Invalid inline config for {url}",
        )

    path = source.get("config_file")
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No config file found for {url}",
        )

    try:
        with open(path, "r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}
    except FileNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config file not found: {path}",
        ) from err
    except OSError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read config file: {path}",
        ) from err


def _normalize_input_id(input_id: str) -> str:
    # route outputs are referenced as "<component>.<output>"
    return input_id.split(".", 1)[0]


def _build_graph_from_config(cfg: dict, metrics_by_id: dict):
    nodes = {}
    edges = {}

    def add_node(node_id, type_):
        nodes[node_id] = {
            "id": node_id,
            "label": node_id,
            "type": type_,
            "metrics": metrics_by_id.get(node_id),
        }

    def add_edge(src, dst):
        edge_id = f"{src}->{dst}"
        edges[edge_id] = {
            "id": edge_id,
            "source": src,
            "target": dst,
            "animated": True,
        }

    sources = cfg.get("sources", {}) or {}
    transforms = cfg.get("transforms", {}) or {}
    sinks = cfg.get("sinks", {}) or {}

    for name in sources.keys():
        add_node(name, "sources")

    for name in transforms.keys():
        add_node(name, "transforms")

    for name in sinks.keys():
        add_node(name, "sinks")

    def connect_inputs(component_name, component_def):
        for input_id in component_def.get("inputs", []) or []:
            src_id = _normalize_input_id(input_id)
            if src_id in nodes:
                add_edge(src_id, component_name)

    for name, data in transforms.items():
        connect_inputs(name, data)

    for name, data in sinks.items():
        connect_inputs(name, data)

    return list(nodes.values()), list(edges.values())


def _metrics_from_graphql(url: str) -> dict:
    response = requests.post(f"{url}/graphql", json={"query": query})
    response.raise_for_status()
    data = response.json()["data"]

    metrics_by_id = {}
    for section in ("sources", "transforms", "sinks"):
        for edge in data[section]["edges"]:
            node = edge["node"]
            metrics_by_id[node["componentId"]] = node.get("metrics")

    meta = {"version": data["meta"]["versionString"].split(" ")[0]}
    return {
        "metrics_by_id": metrics_by_id,
        "meta": meta,
        "hostMetrics": data["hostMetrics"],
    }


def format_response(data):
    nodes = {}
    edges = {}

    def add_node(node_id, type_, metrics):
        nodes[node_id] = {
            "id": node_id,
            "label": node_id,
            "type": type_,
            "metrics": metrics,
        }

    def add_edge(src, dst):
        edge_id = f"{src}->{dst}"
        edges[edge_id] = {
            "id": edge_id,
            "source": src,
            "target": dst,
            "animated": True,
        }

    for section in ("sources", "transforms", "sinks"):
        for edge in data[section]["edges"]:
            node = edge["node"]
            node_id = node["componentId"]

            add_node(node_id, section, node.get("metrics"))

            # Upstream parents (always valid when present)
            for src in node.get("sources", []) or []:
                add_edge(src["componentId"], node_id)

            # "transforms" field is ambiguous depending on component kind:
            # - on TRANSFORMS: it's downstream children transforms
            # - on SINKS: it's upstream transforms feeding the sink
            for tr in node.get("transforms", []) or []:
                tr_id = tr["componentId"]
                if section == "transforms":
                    add_edge(node_id, tr_id)  # transform -> next transform
                else:
                    add_edge(tr_id, node_id)  # transform -> sink (parent)

    return {
        "nodes": list(nodes.values()),
        "edges": list(edges.values()),
        "meta": {"version": data["meta"]["versionString"].split(" ")[0]},
        "hostMetrics": data["hostMetrics"],
    }


@router.get("/urls")
async def read_urls():
    config_map = _load_config_map()
    return {"urls": [{"name": inst["name"], "url": inst["url"]} for inst in config_map]}


@router.get("/query")
async def read_query(url: str):
    try:
        config = _load_vector_config(url)

        metrics_by_id = {}
        meta = {}
        host_metrics = {}
        try:
            metrics_payload = _metrics_from_graphql(url)
            metrics_by_id = metrics_payload["metrics_by_id"]
            meta = metrics_payload["meta"]
            host_metrics = metrics_payload["hostMetrics"]
        except requests.exceptions.RequestException as err:
            logger.error(f"Failed to fetch metrics from {url}")
            logger.critical(err)

        nodes, edges = _build_graph_from_config(config, metrics_by_id)

        return {
            "nodes": nodes,
            "edges": edges,
            "meta": meta,
            "hostMetrics": host_metrics,
        }
    except NewConnectionError as err:
        logger.error(f"Failed to connect to {url}")
        logger.critical(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect to {url}",
        )
    except requests.exceptions.RequestException as err:
        logger.error(f"Failed to fetch data from {url}")
        logger.critical(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch data from {url}",
        ) from err


@router.get("/health")
def health(url: str):
    try:
        response = requests.get(f"{url}/health")
        response.raise_for_status()
        return response.json()
    except NewConnectionError as err:
        logger.error(f"Failed to connect to {url}")
        logger.critical(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect to {url}",
        )
    except requests.exceptions.RequestException as err:
        logger.error(f"Failed to fetch data from {url}")
        logger.critical(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch data from {url}",
        ) from err
