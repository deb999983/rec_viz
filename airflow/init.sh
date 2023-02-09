ROOT_DIR=$(dirname $(dirname $(realpath $0)))

export AIRFLOW__CORE__LOAD_EXAMPLES=false
export AIRFLOW__CORE__DAGS_FOLDER=${ROOT_DIR}/airflow/dags
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
export AIRFLOW__CORE__PARALLELISM=2
export AIRFLOW__CORE__SQL_ALCHEMY_POOL_SIZE=1
export AIRFLOW__CORE__SQL_ALCHEMY_MAX_OVERFLOW=5
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://postgres:postgres@rec_viz_airflow_db:5432/airflow"
export AIRFLOW__WEBSERVER__WEB_SERVER_NAME=localhost
export AIRFLOW__WEBSERVER__EXPOSE_CONFIG=true
export DATA_FOLDER=${ROOT_DIR}/airflow/.airflow/data
export AIRFLOW_HOME=${ROOT_DIR}/airflow/.airflow
export PYTHONPATH="${ROOT_DIR}:${ROOT_DIR}/airflow"


export AIRFLOW__API__AUTH_BACKENDS="airflow.api.auth.backend.session,airflow.api.auth.backend.basic_auth"


env | grep 'AIRFLOW'
echo $ROOT_DIR

initdb() {
    airflow db init
    echo "Airflow DB initialised"

    echo Creating Admin user airflow:airflow
    airflow users create -e admin@example.org -u airflow -p airflow -r Admin -f airflow -l airflow
    
    if [ -f "${ROOT_DIR}/airflow/variables.local.json" ]; then      
      echo Import airflow variables from "${ROOT_DIR}/airflow/variables.local.json";
      airflow variables import "${ROOT_DIR}/airflow/variables.local.json";
      echo Done importing variables;
    fi

    if [ -f "${ROOT_DIR}/airflow/connections.local.json" ]; then      
      echo Import airflow connections from "${ROOT_DIR}/airflow/connections.local.json";
      airflow connections import "${ROOT_DIR}/airflow/connections.local.json";
      echo Done importing connections;
    fi
}

initdb
# With the "Local" and "Sequential" executors it should all run in one container.
rm -rf "${AIRFLOW_HOME}/airflow-webserver.pid"
airflow scheduler &
exec airflow webserver
