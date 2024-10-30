# 
FROM python:3.13

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY *.py /code/
COPY app.json /code/
COPY log_conf.yaml /code/

# 
CMD ["uvicorn", "main:app", "--log-config=log_conf.yaml", "--host=0.0.0.0", "--port=80", "--proxy-headers", "--forwarded-allow-ips='*'"]
