from api.complaints.complaints_controller import ComplaintsController
from config import api_port
from fastapi import FastAPI
import uvicorn
app=FastAPI()
app.include_router(ComplaintsController.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=api_port)