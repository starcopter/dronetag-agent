FROM python:3.12-alpine

RUN pip install libmav

WORKDIR /app
COPY log_mavlink.py async_libmav.py .
COPY mavlink mavlink

CMD python3 log_mavlink.py
