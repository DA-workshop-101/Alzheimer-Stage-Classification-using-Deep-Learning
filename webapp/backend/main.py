import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi import FastAPI, File, UploadFile # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from .predictor import predict
import uvicorn # type: ignore

app = FastAPI()

os.environ["RUN_MAIN"] = "true"

# frontend_url = os.getenv("FRONTEND_URL", "http://127.0.0.1:3000") 

# print("Frontend URL (for CORS):", frontend_url)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://adapt-webapp-007.netlify.app/", "https://da-workshop-101.github.io/"],
    allow_credentials=True,
    allow_methods=["*"],  # ["GET", "POST"]
    allow_headers=["*"]   # ["Content-Type", "Authorization"]
)


@app.get("/ping")
async def ping():
    return "hello,main jinda hun"


@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    print("Received file for prediction...")
    try:
        image_bytes = await file.read()
        print("File read complete.")
        result = predict(image_bytes)
        print("Prediction complete.")
    except Exception as e:
        print(f"Error during prediction: {e}")
    return result


# if __name__=="__main__" and os.getenv("RUN_MAIN") == "true" :
#     uvicorn.run(app,host='0.0.0.0',port=8000)