# Zeus kubernetes Agent

## Commands

### `Python3` as default `python`.

- Run locally
```
# Initialize the virtual env and the deps.
make init
# run project
make run
```

- Run on kubernetes
```
docker build -t zeus-agent:latest .
docker push zeus-agent:latest
make deploy
```
••Please chnage the image name in `deployment/deployment.yaml` according to your repo name.••

- Clean up
```
# For local
make clean

# Uninstall kubernetes deployments.
make uninstall
```