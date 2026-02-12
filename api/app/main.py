from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routers import auth, leave, approvals

app = FastAPI(title=settings.APP_NAME)

origins = ["http://localhost:3000", "https://*.ejada.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(leave.router)
app.include_router(approvals.router)

@app.get("/health")
def health():
    return {"status": "ok"}