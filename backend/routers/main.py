from fastapi import APIRouter, HTTPException, status
from urllib3.exceptions import NewConnectionError
from core.settings import settings
from core.log import logger
from const import query
import requests

router = APIRouter()


def format_response(tmp_data):
    nodes = []
    edges = []

    for type_ in ("sources", "transforms", "sinks"):
        for node in tmp_data[type_]["edges"]:
            node = node["node"]
            parents = []
            childs = []
            for source in node.get("sources", []):
                parents.append(source["componentId"])

            for transform in node.get("transforms", []):
                if type_ == "transforms":
                    childs.append(transform["componentId"])
                else:
                    parents.append(transform["componentId"])

            nodes.append(
                {
                    "id": node["componentId"],
                    "label": node["componentId"],
                    "type": type_,
                    "metrics": node["metrics"],
                }
            )

            for parent in parents:
                edges.append(
                    {
                        "id": f"{parent}-{node['componentId']}",
                        "source": parent,
                        "target": node["componentId"],
                        "animated": True,
                    }
                )

            for child in childs:
                edges.append(
                    {
                        "id": f"{node['componentId']}-{child}",
                        "source": node["componentId"],
                        "target": child,
                        "animated": True,
                    }
                )

    return {
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "version": tmp_data["meta"]["versionString"].split(" ")[0],
        },
        "hostMetrics": tmp_data["hostMetrics"],
    }


@router.get("/urls")
async def read_urls():
    return {"urls": settings.VECTOR_URLS.split(",")}


@router.get("/query")
async def read_query(url: str):
    try:
        response = requests.post(f"{url}/graphql", json={"query": query})
        response.raise_for_status()
        return format_response(response.json()["data"])
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
