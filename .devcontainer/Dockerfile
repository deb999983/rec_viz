FROM apache/airflow:2.4.2-python3.9

USER root
RUN usermod -u 501 airflow

RUN \
 apt update && \
 apt install lsof libpq-dev python3-dev gcc -y
USER airflow

EXPOSE 8000
EXPOSE 8080
EXPOSE 8793

WORKDIR /workspaces/rec_viz
ENV PYTHONPATH=/workspaces/rec_viz

COPY airflow/requirements.txt airflow/requirements.txt
COPY server/requirements.txt server/requirements.txt

RUN \    
    pip3 install -r airflow/requirements.txt && \
    pip3 install -r server/requirements.txt

COPY . .

ENTRYPOINT ["sleep", "infinity"]
