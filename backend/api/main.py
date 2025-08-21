from fastapi import FastAPI, UploadFile, File , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
from typing import Dict,Any
import json
from dotenv import load_dotenv

load_dotenv()

from backend.orchestrator.runner import start
from pydantic import BaseModel
from backend.integrations.supabase_client import get_supabase_client

app = FastAPI(title="Automated Data Analyst API - Phase 1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://analytiq-seven.vercel.app",  # Your Vercel frontend
        os.getenv("FRONTEND_URL", "http://localhost:5173")  # Fallback to localhost for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def saveUploadedFile(upload_file : UploadFile , destination : str):
    try:
        with open(destination , "wb") as buffer:
            shutil.copyfileobj(upload_file.file , buffer)
    except Exception as e:
        print(f"error saving file : {e}")
        raise
    finally:
        upload_file.file.close()


@app.post("/api/v1/upload")
async def upload_and_analyze(file : UploadFile = File(...)):
    
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    report_id = str(uuid.uuid4())
    os.makedirs("uploads" , exist_ok=True)
    os.makedirs("reports" , exist_ok=True)
    
    original_file_path = f"uploads/{report_id}_{file.filename}"
    
    print(f"[API] Saving uploaded file {file.filename}...")
    saveUploadedFile(file, original_file_path)
    print(f"[API] File saved to {original_file_path}")
    
    print(f"[API] Starting analysis for report {report_id}...")
    
    try:
        result = await start(original_file_path)
        print(f"[API] Analysis completed for report {report_id}")
    except Exception as e:
        print(f"[API] Analysis failed for report {report_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    
    frontend_focused_report = {
        "report_id": report_id, # Include for potential future use or frontend tracking
        "storyteller_output": result.get("storyteller_output", {}),
        "chart_data": result.get("chart_data", [])
        # The full result dict contains all agent outputs if needed later
    }
    
    print(f"[API] Returning report for {report_id}")
    return frontend_focused_report


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "Automated Data Analyst Backend - Phase 1"}


class AnalyzeSupabaseRequest(BaseModel):
    bucket: str
    path: str


@app.post("/api/v1/analyze-supabase")
async def analyze_supabase_csv(req: AnalyzeSupabaseRequest):
    """Analyze a CSV file stored in Supabase Storage.

    Body params:
      - bucket: storage bucket name
      - path: path to the CSV inside the bucket
    """
    sb = get_supabase_client()
    # Download the file as bytes
    res = sb.storage.from_(req.bucket).download(req.path)
    if res is None:
        raise HTTPException(status_code=404, detail="File not found in Supabase")

    # Persist temporarily to local disk for the current pipeline
    report_id = str(uuid.uuid4())
    os.makedirs("uploads", exist_ok=True)
    original_file_path = f"uploads/{report_id}_{os.path.basename(req.path)}"
    with open(original_file_path, "wb") as f:
        f.write(res)

    try:
        result = await start(original_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        try:
            os.remove(original_file_path)
        except Exception:
            pass

    frontend_focused_report = {
        "report_id": report_id,
        "storyteller_output": result.get("storyteller_output", {}),
        "chart_data": result.get("chart_data", []),
    }
    return frontend_focused_report