# import mlflow
# from mlflow.tracking import MlflowClient

# mlflow.set_tracking_uri("http://ec2-43-204-145-141.ap-south-1.compute.amazonaws.com:5000")

# # Load model from the model registry
# def load_model_from_registry(model_name, model_version):
#     model_uri = f"models:/{model_name}/{model_version}"
#     model = mlflow.pyfunc.load_model(model_uri)
#     return model

# # example
# model = load_model_from_registry("yt_chrome_plugin_model","1")
# print("Model Loaded sucessfullly")


from flask import Flask, request, jsonify
from flask_cors import CORS
import mlflow
import numpy as np
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from mlflow.tracking import MlflowClient

app = Flask(__name__)
CORS(app)

def preprocess_comment(comment):
    """Apply preprocessing transformations to a comment."""
    try:
        # Convert to lowercase
        comment = comment.lower()

        # Remove trailing and leading whitespaces
        comment = comment.strip()

        # Remove newline characters
        comment = re.sub(r'\n', ' ', comment)

        # Remove non-alphanumeric characters, except punctuation
        comment = re.sub(r'[^A-Za-z0-9\s!?.,]', '', comment)

        # Remove stopwords but retain important ones for sentiment analysis
        stop_words = set(stopwords.words('english')) - {'not', 'but', 'however', 'no', 'yet'}
        comment = ' '.join([word for word in comment.split() if word not in stop_words])

        # Lemmatize the words
        lemmatizer = WordNetLemmatizer()
        comment = ' '.join([lemmatizer.lemmatize(word) for word in comment.split()])

        return comment
    except Exception as e:
        print(f"Error in preprocessing comment: {e}")
        return comment
    

def load_model_and_vectorizer(model_name, model_version, vectorizer_path):
    # Set MLflow tracking URI to your server
    mlflow.set_tracking_uri("http://ec2-43-204-145-141.ap-south-1.compute.amazonaws.com:5000")  # Replace with your MLflow tracking URI
    client = MlflowClient()
    model_uri = f"models:/{model_name}/{model_version}"
    model = mlflow.pyfunc.load_model(model_uri)
    vectorizer = joblib.load(vectorizer_path)  # Load the vectorizer
    return model, vectorizer

# Initialize the model and vectorizer
model, vectorizer = load_model_and_vectorizer("yt_chrome_plugin_model","1", "./tfidf_vectorizer.pkl")  # Update paths and versions as needed

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    comments = data.get('comments')
    
    if not comments:
        return jsonify({"error": "No comments provided"}), 400

    try:
        # Preprocess each comment before vectorizing
        preprocessed_comments = [preprocess_comment(comment) for comment in comments]
        
        # Transform comments using the vectorizer
        transformed_comments = vectorizer.transform(preprocessed_comments)
        
        # Make predictions
        predictions = model.predict(transformed_comments).tolist()  # Convert to list
        
        # Convert predictions to strings for consistency
        predictions = [str(pred) for pred in predictions]
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
    # Return the response with original comments and predicted sentiments
    response = [{"comment": comment, "sentiment": sentiment} for comment, sentiment in zip(comments, predictions)]
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)