FROM apache/airflow:2.4.2-python3.9

USER root
RUN usermod -u 501 airflow
RUN apt-get update && \
    apt-get install lsof && \
    apt-get install docker.io -y
USER airflow

EXPOSE 8080
EXPOSE 8793

WORKDIR /workspaces/airflow

COPY airflow/requirements.txt .

RUN mkdir -p .airflow \
&& pip3 install -r requirements.txt


COPY --chown=501:0 airflow .

ENTRYPOINT ./init.sh
