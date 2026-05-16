from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
from datetime import date
from typing import Optional
import os

load_dotenv()

app = FastAPI(title="Digital Archive API")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# MODELS
class Archive(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    file_url: Optional[str] = None

class DailyReport(BaseModel):
    date: date
    total_archives: Optional[int] = 0
    notes: Optional[str] = None

# ARCHIVE ROUTES
@app.get("/archives")
def get_all_archives():
    result = supabase.table("archives").select("*").execute()
    return result.data

@app.get("/archives/search")
def search_archives(query: str):
    result = supabase.table("archives").select("*").ilike("title", f"%{query}%").execute()
    return result.data

@app.get("/archives/{id}")
def get_archive(id: str):
    result = supabase.table("archives").select("*").eq("id", id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Archive not found")
    return result.data[0]

@app.post("/archives")
def create_archive(archive: Archive):
    result = supabase.table("archives").insert(archive.dict()).execute()
    return result.data[0]

@app.put("/archives/{id}")
def update_archive(id: str, archive: Archive):
    result = supabase.table("archives").update(archive.dict()).eq("id", id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Archive not found")
    return result.data[0]

@app.delete("/archives/{id}")
def delete_archive(id: str):
    result = supabase.table("archives").delete().eq("id", id).execute()
    return {"message": "Archive deleted successfully"}

# DAILY REPORT ROUTES
@app.get("/reports")
def get_all_reports():
    result = supabase.table("daily_reports").select("*").execute()
    return result.data

@app.post("/reports")
def create_report(report: DailyReport):
    result = supabase.table("daily_reports").insert(report.dict()).execute()
    return result.data[0]

# HEALTH CHECK
@app.get("/")
def root():
    return {"message": "Digital Archive API is running"}
