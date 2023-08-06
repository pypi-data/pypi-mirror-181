[![Datalayer](https://assets.datalayer.design/datalayer-25.svg)](https://datalayer.io)

# 🪐 💁 Jupyter Admin

> 🛂 `Jupyter Admin` is a UI (Web User Interface) and CLI (Command Line Interface) to manage the Datalayer Jupyter components.

Jupyter Administration UI and CLI for the Jupyter ecosystem, with telemetry. It provides facilities to the Jupyter components to:

- Deploy
- Configure
- Monitor
- Manage

```bash
# Start the frontend webpack server and jupyter server.
# echo open http://localhost:2003
# echo open http://localhost:8686/hub/jupyter-admin
# make start
```

```bash
# Connect to the jupyterhub local sqlite database and run e.g.
# .schema
# .tables
# .schema api_tokens
# select * from api_tokens;
# make sqlite
```

```bash
# open http://localhost:3063
# open http://localhost:8686/api/jupyter/lab?token=60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6
yarn start
```

```bash
pip install -e .[test]
jupyter labextension develop . --overwrite
jupyter labextension list
# jupyter server extension enable datalayer
jupyter server extension list
# open http://localhost:8686/api/jupyter/lab?token=60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6
yarn jupyterlab
```
