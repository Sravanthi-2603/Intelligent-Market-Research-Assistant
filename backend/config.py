import os
from dotenv import load_dotenv

# Try to load from config.env if .env is not available
load_dotenv("config.env")
load_dotenv()

IBM_API_KEY = os.getenv("IBM_API_KEY", "M-6oyiybKr3nuDXbeVI4PDsPpv_GDCq_a1_s0vBbeOKI")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID", "b1f23f7e-33d1-4aeb-879e-69b65ec56960")
IBM_WATSONX_URL = os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "intelligent-market-research-2024")

# IBM Granite model IDs
GRANITE_MODEL_ID = "ibm/granite-3-8b-instruct"
GRANITE_EMBEDDING_MODEL = "ibm/slate-125m-english-rtrvr"

# WatsonX endpoints
WATSONX_GENERATE_URL = f"{IBM_WATSONX_URL}/ml/v1/text/generation?version=2023-05-29"
WATSONX_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
