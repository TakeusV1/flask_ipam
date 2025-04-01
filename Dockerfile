FROM python:3.13.2-alpine3.21
WORKDIR /fipam
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app /fipam/app
COPY instance /fipam/instance
ENV APP_HOME=/fipam
ENV PYTHONPATH=${APP_HOME}
ENV PATH="$PATH:${APP_HOME}/.local/bin"
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:5000 --workers=2 --preload"
EXPOSE 5000
ENTRYPOINT ["gunicorn","app:create_app()"]
