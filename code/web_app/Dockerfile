FROM python:3

COPY code/* /code/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

CMD ["python", "/code/main.py"]