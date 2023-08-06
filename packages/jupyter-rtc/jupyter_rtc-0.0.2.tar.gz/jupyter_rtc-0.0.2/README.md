[![Datalayer](https://assets.datalayer.design/datalayer-25.svg)](https://datalayer.io)

# Jupyter RTC

> 🪐 👥 Multi-user Jupyter server with realtime history backed by Apache Cassandra

The Realtime collaboration for Jupyter is being actively designed and developed by the Jupyter community. The RTC feature presents technical challenges for security (how to secure and trust a notebook being edited by multiple users). The current jupyter server is also not multi-user which can for some use cases be limiting. RTC nature goes also beyond what the current community is used to (a lot of historical data needs to be persisted which demands central and scalable infrastructure, so not really the casual laptop with a notebook). We are also facing divergence in the community in how the JupyterLab components will be further developed. The vote to remove the JupyterLab shared-model package has just passed https://github.com/jupyterlab/jupyterlab/issues/12708#issuecomment-1179837791 and the decision goes against the reusability for third party applications. Datalayer is willing to offer a one-stop solution with an end-user model a-la-nbformat which will be collaborative (nbshared), backed by a multi-user Jupyter server with realtime history capabilities. The user history will be persisted in a local file, in PostgreSQL or in Apache Cassandra.

The repository will be hosted under https://github.com/datalayer/jupyter-rtc. The planned deliverables are a “nbshared” model the first 3 months, a multi-user server with history on local file the first 6 months, PostgreSQL and Cassandra support after 1 year.

```bash
pip install -e .[test]
jupyter labextension develop . --overwrite
jupyter labextension list
jupyter server extension list
# open http://localhost:8686/api/jupyter/lab?token=60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6
yarn jupyterlab
```
