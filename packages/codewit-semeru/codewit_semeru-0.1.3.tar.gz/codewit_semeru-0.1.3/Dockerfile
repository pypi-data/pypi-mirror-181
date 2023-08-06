# For more information, please refer to https://aka.ms/vscode-docker-python
FROM jupyter/tensorflow-notebook

# Install pip requirements
# COPY requirements.txt .
# RUN python -m pip install -r requirements.txt

COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/

RUN pip install --quiet -r /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"