# VectorViz

This app is a Vector visualizer.  
You will need to enable API on your Vector conf: [docs](https://vector.dev/docs/reference/api)

## How To

Pull docker image: `docker pull ghcr.io/raznak/vectorviz`  
Launch:

```
docker run -p 8000:8000 \
  -e VECTOR_CONFIG_MAP_PATH=/etc/vector/map.yaml
```

Go to http://localhost:8000

## DEVELOP

Launch dockers:

```
docker-compose -f docker-compose.yaml --build -d
```

Then go to: http://:localhost:9000  
Vector URL: http://vector:8686

## Config map (recommended)

You can define instances and their configs in a single YAML file:

```yaml
vector_prod:
  url: http://vector-prod:8686
  config_file: /etc/vector-configs/vector-prod.yaml

vector_stage:
  url: http://vector-stage:8686
  config: |
    api:
      enabled: true
      address: 0.0.0.0:8686
    sources:
      demo:
        type: demo_logs
```

Set the env:

```
VECTOR_CONFIG_MAP_PATH=/etc/vector-configs/map.yaml
```
