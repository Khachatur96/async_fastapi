from contextlib import asynccontextmanager
from typing import Annotated
import uvicorn
from fastapi import FastAPI, Path
from api_v1 import router as router_v1
from core.config import settings
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(router_v1, prefix=settings.api_v1_prefix)


@app.get("/hello/{name}/")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/items/{item_id}/")
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        "item": {
            "id": item_id,
        },
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
