import mlflow.pyfunc
import pytest 
from mlflow.tracking import MlflowClient
import dagshub

dagshub.init(repo_owner='constantaryan', repo_name='yt-comment-sentiments-analysis', mlflow=True)
mlflow.set_tracking_uri("https://dagshub.com/constantaryan/yt-comment-sentiments-analysis.mlflow")
# mlflow.set_tracking_uri("http://ec2-43-204-145-141.ap-south-1.compute.amazonaws.com:5000")

@pytest.mark.parametrize("model_name, stage",[
    ("yt_chrome_plugin_model","Staging"),])

def test_load_latest_staging_model(model_name, stage):
    client = MlflowClient()

    # Let's get Latest model
    latest_version_info = client.get_latest_versions(model_name, stages = [stage])
    latest_version = latest_version_info[0].version if latest_version_info else None 
    
    assert(latest_version is not None, f"No model found in the '{stage}' stage for '{model_name}' ")

    try:
        # Load latest version of the model
        model_uri = f"models:/{model_name}/{latest_version}"
        model = mlflow.pyfunc.load_model(model_uri)

        # Ensure the model loads successfully
        assert model is not None, "Model failed to load"
        print(f"Model '{model_name}' version {latest_version} loaded successfully from '{stage}' stage.")

    except Exception as e:
        pytest.fail(f"Model Loading failed with error: {e}")



