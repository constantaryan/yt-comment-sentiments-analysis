FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgomp1

COPY flask_app/ /app/
COPY tfidf_vectorizer.pkl /app/tfidf_vectorizer.pkl
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN python -m nltk.downloader stopwords wordnet

EXPOSE 5000
# CMD ["python", "app.py"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]