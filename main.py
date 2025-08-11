from fastapi import FastAPI
from app.routes import routes
from app.models.database import Base, engine

app = FastAPI()

app.include_router(routes.router)

# Base.metadata.create_all(bind=engine)