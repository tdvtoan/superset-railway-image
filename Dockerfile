FROM apache/superset:latest

USER root

# Set default environment values (these will be overridden by Railway at runtime)
ENV PYTHONPATH=/app/pythonpath:/app/docker/pythonpath_prod
ENV SUPERSET_ENV=production
ENV SUPERSET_LOAD_EXAMPLES=no
ENV CYPRESS_CONFIG=False
ENV SUPERSET_PORT=8088
ENV SUPERSET_CONFIG_PATH=/app/docker/superset_config.py

EXPOSE 8088

# Install additional Python packages using the system pip (will install into global site-packages)
# The superset process will be able to access these packages
RUN pip3 install --no-cache-dir \
    google \
    google-api-core \
    google-cloud-bigquery \
    google-cloud-storage \
    google-api-python-client \
    psycopg2-binary

# Copy configuration files
COPY startup.sh ./startup.sh
COPY bootstrap.sh /app/docker/docker-bootstrap.sh
COPY superset_config.py /app/docker/superset_config.py

RUN chmod +x ./startup.sh
RUN chmod +x /app/docker/docker-bootstrap.sh

CMD ["sh", "-c", "./startup.sh"]
