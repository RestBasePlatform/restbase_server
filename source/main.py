import os

import uvicorn
from controller.v1.utils import generate_secret_token
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger
from routes.v1 import v1_router


app = FastAPI()


@app.on_event("startup")
def create_module_dir():
    init_path = "modules/__init__.py"
    if not os.path.exists("modules"):
        os.makedirs("modules")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("")


app.include_router(v1_router)


@app.get("/")
def _redirect():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    if not os.getenv("SECRET_TOKEN"):
        logger.warning("Token not found.")
        token = (
            generate_secret_token() + generate_secret_token() + generate_secret_token()
        )
        os.environ["SECRET_TOKEN"] = token
        logger.info(f"Your token: '{token}'")

    uvicorn.run(app, port=8000, host="0.0.0.0")
