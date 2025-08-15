from fastapi import FastAPI, UploadFile, File , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
from typing import Dict,Any
import json

from agents.orchestrator import start

app = FastAPI(title="Automated Data Analyst API - Phase 1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development only. Restrict this in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
