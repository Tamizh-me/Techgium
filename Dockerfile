FROM gradio/python
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PORT=8080
EXPOSE $PORT
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app