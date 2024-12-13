FROM auterion/app-base:v2

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -qq -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

# COPY APP
WORKDIR /app
COPY log.sh /app/log.sh

ENTRYPOINT [ "/app/log.sh" ]
