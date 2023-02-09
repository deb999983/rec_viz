FROM apache/airflow:2.4.2-python3.9

USER root
RUN apt-get update && apt-get install lsof
USER airflow

EXPOSE 8080
EXPOSE 8793

WORKDIR /workspaces/airflow

COPY airflow/requirements.txt .

RUN mkdir -p .airflow && pip3 install -r requirements.txt

COPY server/applications /workspaces/airflow/applications
COPY airflow .

ENTRYPOINT ./init.sh
