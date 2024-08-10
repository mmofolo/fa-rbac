FROM python:3.10

WORKDIR /app

COPY ./requirements.txt ./tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./tmp/requirements.txt

COPY ./app/ /app/

VOLUME [ "/app" ]
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002","--reload" ]
# CMD [ "uvicorn", "main:app", "--host", "0.0.0.0","--reload" , "--root-path", "/api/v1"]
