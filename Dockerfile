FROM python:3

COPY piezo_web_app/ /piezo_web_app/

COPY piezo_web_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /piezo_web_app/

ENV PATH /piezo_web_app:$PATH
ENV PYTHONPATH /piezo_web_app/

EXPOSE 8888

CMD ["python", "./PiezoWebApp/run_piezo.py"]