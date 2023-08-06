# BASE_URL = "http://censius-logs-prod1.us-east-1.elasticbeanstalk.com/v1"
# AMS_URL = "http://ams-prod.us-east-1.elasticbeanstalk.com"
# MONITORS_PROGRAMMATIC_BASE_URL = (
#     "http://monitors-prod.us-east-1.elasticbeanstalk.com//v1/programmatic"
# )
# BASE_URL = "http://censiuslogs-dev.us-east-1.elasticbeanstalk.com//v1"
# AMS_URL = "http://ams-dev0.us-east-1.elasticbeanstalk.com"
# MONITORS_PROGRAMMATIC_BASE_URL = (
#    "http://monitors-env.eba-ptkdpfrn.us-east-1.elasticbeanstalk.com/v1/programmatic"
# )

BASE_URL = "https://console.censius.ai/logs-svc/v1"
AMS_URL = "https://console.censius.ai/ams-svc"
MONITORS_PROGRAMMATIC_BASE_URL = (
    "http://monitors-prod.us-east-1.elasticbeanstalk.com//v1/programmatic"
)
# BASE_URL = "http://censiuslogs-dev.us-east-1.elasticbeanstalk.com/v1"
# AMS_URL = "http://ams-dev0.us-east-1.elasticbeanstalk.com"
# MONITORS_PROGRAMMATIC_BASE_URL = (
#     "http://monitors-env.eba-ptkdpfrn.us-east-1.elasticbeanstalk.com/v1/programmatic"
# )

# Models
REGISTER_MODEL_URL = lambda: f"{AMS_URL}/models/"
REVISE_MODEL_URL = lambda: f"{AMS_URL}/models/revise"
PROCESS_MODEL_URL = lambda: f"{AMS_URL}/models/schema-updation"
REGISTER_NEW_MODEL_VERSION = lambda: f"{AMS_URL}/models/model_version"

# Logs
LOG_URL = lambda: f"{BASE_URL}/logs"
UPDATE_ACTUAL_URL = lambda prediction_id: f"{BASE_URL}/logs/{prediction_id}/updateActual"
BULK_LOG_DATATYPE_VALIDATION_URL = f"{BASE_URL}/logs/validate_bulk_datatype"
BULK_LOG_URL = f"{BASE_URL}/logs/bulk_logs"
LOG_EXPLAINATIONS_URL = lambda: f"{BASE_URL}/explainations"
BULK_EXPLAINATIONS_URL = f"{BASE_URL}/explainations/bulk_explainations"

# Dataset
REGISTER_DATASET_URL = lambda: f"{AMS_URL}/datasets/create-and-upload"

# Project
REGISTER_PROJECT_URL = lambda: f"{AMS_URL}/projects/"


# Monitors
GET_MODEL_HEALTH_URL = lambda: f"{MONITORS_PROGRAMMATIC_BASE_URL}/get_model_health"
BULK_CHUNK_SIZE = 2000
