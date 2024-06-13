# VectorViz

This app is a Vector visualizer.  
You will need to enable API on your Vector conf: [docs](https://vector.dev/docs/reference/api)

## How To

Pull docker image: `docker pull ghcr.io/raznak/vectorviz`  
Launch:

```
docker run -p 8000:8000 -e VECTOR_URLS=http://vector1:8686,http://vector2:8686
```

Go to http://localhost:8000

## DEVELOP

Launch dockers:

```
docker-compose -f docker-compose-dev.yaml --build -d
```

Then go to: http://:localhost:9000  
Vector URL: http://vector:8686
