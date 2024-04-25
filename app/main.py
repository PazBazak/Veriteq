import uvicorn
from auth import get_authenticated_account
from fastapi import Depends, FastAPI
from routers.sign_router import router as sign_router
from utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Initiating FastAPI app")
app = FastAPI(root_path="/api", dependencies=[Depends(get_authenticated_account)])

app.include_router(sign_router, prefix="/v1")
app.include_router(sign_router, prefix="/latest")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
