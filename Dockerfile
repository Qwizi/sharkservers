FROM python:3.10

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./shark_api /code/shark_api

#
CMD ["uvicorn", "shark_api.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]