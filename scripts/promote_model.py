# promote model

import os
import mlflow

def promote_model():
    dagshub_token = os.getenv("CAPSTONE_TEST")
    if not dagshub_token:
        raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = "altamashdsa99"
    repo_name = "mlops-project"

    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    client = mlflow.MlflowClient()
    model_name = "my_model"

    staging_model = client.get_model_version_by_alias(model_name, "Staging")
    latest_version_staging = staging_model.version

    try:
        prod_model = client.get_model_version_by_alias(model_name, "Production")
        client.delete_registered_model_alias(model_name, "Production")
        print(f"Removed Production alias from version {prod_model.version}")
    except Exception:
        print("No existing Production alias found")

    
    client.set_registered_model_alias(model_name, "Production", latest_version_staging)
    print(f"Model version {latest_version_staging} promoted to Production")

if __name__ == "__main__":
    promote_model()