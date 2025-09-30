import os
import json
import tempfile
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from crew_app.file_tools.file_loader import detect_and_extract
from crew_app.crew import run_pipeline
from crew_app.utils import txt_to_docx_bytes, txt_to_pdf_bytes
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(title="ATS Resume Optimization API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://*.herokuapp.com",  # Heroku
        "https://*.railway.app",   # Railway
        "https://*.onrender.com",   # Render
        "https://*.vercel.app",     # Vercel
        "https://*.netlify.app"     # Netlify
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (React build)
if os.path.exists("build"):
    app.mount("/static", StaticFiles(directory="build/static"), name="static")

@app.get("/")
async def root():
    if os.path.exists("build/index.html"):
        return FileResponse("build/index.html")
    return {"message": "ATS Resume Optimization API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "endpoints": ["/process-resume", "/download-pdf", "/download-docx", "/download-txt"]}

@app.post("/process-resume")
async def process_resume(
    file: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...)
):
    try:
        # Check environment variables
        openai_key = os.getenv("OPENAI_API_KEY")
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        print(f"OpenAI API Key present: {bool(openai_key)}")
        print(f"OpenAI Model: {openai_model}")
        
        if not openai_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not found. Please check environment variables.")
        
        # Read file content
        file_content = await file.read()
        
        # Extract text from uploaded file
        file_ext, raw_text = detect_and_extract(file.filename, file_content)
        
        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the file")
        
        print(f"Processing resume for job: {job_title}")
        print(f"Resume text length: {len(raw_text)}")
        
        # Run the CrewAI pipeline
        cleaned, rewritten, final_resume, evaluation = run_pipeline(
            raw_resume_text=raw_text,
            job_title=job_title.strip(),
            job_description=job_description.strip()
        )
        
        # Try to parse evaluation as JSON
        parsed_evaluation = None
        try:
            # Clean up the evaluation text for JSON parsing
            eval_text = evaluation.strip()
            # Replace single quotes with double quotes for JSON compatibility
            eval_text = eval_text.replace("'", '"')
            parsed_evaluation = json.loads(eval_text)
        except Exception:
            # If JSON parsing fails, return as string
            parsed_evaluation = evaluation
        
        return {
            "success": True,
            "results": {
                "cleaned": cleaned,
                "rewritten": rewritten,
                "final": final_resume,
                "evaluation": parsed_evaluation
            }
        }
        
    except Exception as e:
        print(f"Error processing resume: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post("/download-txt")
async def download_txt(content: str = Form(...), filename: str = Form("resume.txt")):
    """Generate and return a TXT file download"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        return FileResponse(
            path=tmp_file_path,
            filename=filename,
            media_type='text/plain'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.post("/download-docx")
async def download_docx(content: str = Form(...), filename: str = Form("resume.docx")):
    """Generate and return a DOCX file download"""
    try:
        # Convert text to DOCX bytes
        docx_bytes = txt_to_docx_bytes(content)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            tmp_file.write(docx_bytes)
            tmp_file_path = tmp_file.name
        
        return FileResponse(
            path=tmp_file_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.post("/download-pdf")
async def download_pdf(content: str = Form(...), filename: str = Form("resume.pdf")):
    """Generate and return a PDF file download"""
    try:
        print(f"PDF Generation: Starting PDF generation for {filename}")
        print(f"PDF Generation: Content length: {len(content)} characters")
        
        # Convert text to PDF bytes
        pdf_bytes = txt_to_pdf_bytes(content)
        print(f"PDF Generation: Generated PDF size: {len(pdf_bytes)} bytes")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_file_path = tmp_file.name
        
        print(f"PDF Generation: Temporary file created at {tmp_file_path}")
        
        return FileResponse(
            path=tmp_file_path,
            filename=filename,
            media_type='application/pdf'
        )
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
