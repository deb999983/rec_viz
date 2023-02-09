FROM  postgres:14
COPY init_db.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_user=postgres