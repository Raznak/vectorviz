from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from urllib3.exceptions import NewConnectionError
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from settings import settings
from const import query
import requests
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "PUT", "POST", "PATCH", "DELETE"],
    allow_credentials=True,
    allow_headers=["*"],
)


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


@app.get("/query")
async def read_query(url: str):
    try:
        response = requests.post(f"{url}/graphql", json={"query": query})
        response.raise_for_status()
        return format_response(response.json()["data"])
    except NewConnectionError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect to {url}",
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch data from {url}",
        ) from e


if not settings.DEV_MODE:
    templates = Jinja2Templates(directory="templates/spa/")

    app.mount("/assets", StaticFiles(directory="templates/spa/assets"), name="static")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def main(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
