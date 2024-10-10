# encoding='utf-8'

# @Time: 2024-09-11
# @File: app.py
#!/usr/bin/env python
from icecream import ic
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile
import pandas as pd
import PyPDF2
import base64
import io
from pdf2image import convert_from_path

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContainerRequest(BaseModel):
    container_number: str


@app.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open("result_.xlsx", "wb") as f:
            f.write(contents)
        return {"message": "Excel file uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open("output.pdf", "wb") as f:
            f.write(contents)
        return {"message": "PDF file uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_location_pdf")
async def get_location_pdf(request: ContainerRequest):
    # try:
    # Check if the required files exist
    if not os.path.exists('result_.xlsx'):
        raise HTTPException(
            status_code=404,
            detail="Excel file not found. Please upload it first."
        )
    if not os.path.exists('output.pdf'):
        raise HTTPException(
            status_code=404,
            detail="PDF file not found. Please upload it first."
        )

    # Read the Excel file
    df = pd.read_excel('result_.xlsx')
    
    # Find the corresponding location ID for the given container number
    matching_rows = df[df['container_number'] == request.container_number]
    ic(matching_rows)
    
    if matching_rows.empty:
        raise HTTPException(
            status_code=404,
            detail="Container number not found"
        )
    
    location_id = str(matching_rows['location_id'].iloc[0])
    ic(location_id)
    
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader('output.pdf')
    
    # Find the page containing the location_id
    target_page = None
    for page_num, page in enumerate(pdf_reader.pages):
        if location_id in page.extract_text():
            target_page = page_num
            break
    
    if target_page is None:
        raise HTTPException(
            status_code=404,
            detail="Location ID not found in PDF"
        )
    
    # Convert the PDF page to an image
    try:
        images = convert_from_path(
            'output.pdf',
            first_page=target_page+1,
            last_page=target_page+1
        )
    except Exception as e:
        ic(f"PDF conversion error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Unable to convert PDF. Please ensure Poppler is installed and in PATH."
        )
    
    if not images:
        raise HTTPException(
            status_code=500,
            detail="Failed to convert PDF to image"
        )
    
    # Resize the image to have a width of 1200 pixels
    from PIL import Image
    image = images[0]
    width_percent = (1200 / float(image.size[0]))
    height_size = int((float(image.size[1]) * float(width_percent)))
    image = image.resize((1200, height_size), Image.LANCZOS)
    ic(width_percent, height_size)
    # Rotate the image 90 degrees clockwise
    rotated_image = image.rotate(-90, expand=True)
    
    # Convert the rotated image to base64
    buffered = io.BytesIO()
    rotated_image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return {"image": img_base64}
    
    # Convert the resized image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return {"image": img_base64}

    # except Exception as e:
    #     ic(f"Unexpected error: {str(e)}")
    #     raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}


# if __name__ == "__main__":
#     uvicorn.run("app:app", reload=True, port=5051, host="0.0.0.0")
