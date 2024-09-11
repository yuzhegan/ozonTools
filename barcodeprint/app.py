# encoding='utf-8

# @Time: 2024-09-11
# @File: %
#!/usr/bin/env python
from icecream import ic
import os
from pydantic import BaseModel
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import base64
import io
import barcode
import tempfile
from PIL import Image, ImageDraw, ImageFont
import platform
import subprocess

app = FastAPI()

# 添加CORS中间件
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
    try:
        # Check if the required files exist
        if not os.path.exists('result_.xlsx'):
            raise HTTPException(status_code=404, detail="Excel file not found. Please upload it first.")
        if not os.path.exists('output.pdf'):
            raise HTTPException(status_code=404, detail="PDF file not found. Please upload it first.")

        # Read the Excel file
        df = pd.read_excel('result_.xlsx')
        
        # Find the corresponding location ID for the given container number
        matching_rows = df[df['container_number'] == request.container_number]
        ic(matching_rows)
        
        if matching_rows.empty:
            raise HTTPException(status_code=404, detail="Container number not found")
        
        location_id = str(matching_rows['location_id'].iloc[0])
        ic(location_id)
        
        # Open the PDF file
        pdf_reader = PdfReader("output.pdf")
        
        # Find the page with the matching location ID
        target_page = None
        for i, page in enumerate(pdf_reader.pages):
            if location_id in page.extract_text():
                target_page = page
                break
        
        if target_page is None:
            raise HTTPException(status_code=404, detail="Location ID not found in PDF")
        
        # Generate barcode image
        barcode_type = 'code128'  # You may need to adjust this based on your requirements
        barcode_data = location_id  # Using location_id as barcode data
        barcode_class = barcode.get_barcode_class(barcode_type)
        barcode_instance = barcode_class(barcode_data)
        
        # Save barcode image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            ic(temp_file.name)
            barcode_instance.save(temp_file.name)  # Save directly to the temp file

        try:
            # Ensure the file is closed before opening it with PIL
            temp_file.close()
            
            # Open the saved image
            image = Image.open(temp_file.name)

            # Create a drawing context
            draw = ImageDraw.Draw(image)

            # Load a font
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except IOError:
                # Fallback to default font if arial.ttf is not available
                font = ImageFont.load_default()

            # Add text below the barcode
            text = barcode_data
            text_width, text_height = draw.textsize(text, font=font)
            x = (image.width - text_width) / 2
            y = image.height - text_height - 10
            draw.text((x, y), text, font=font, fill="black")

            # Save the modified image
            image.save(temp_file.name)

            # Print the barcode
            if platform.system() == "Windows":
                os.startfile(temp_file.name, "print")
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["lpr", temp_file.name])
            else:  # Linux and other Unix-like systems
                subprocess.run(["lpr", temp_file.name])

        except Exception as img_error:
            ic(f"Error processing image: {str(img_error)}")
            ic(f"Temp file path: {temp_file.name}")
            ic(f"File exists: {os.path.exists(temp_file.name)}")
            ic(f"File size: {os.path.getsize(temp_file.name) if os.path.exists(temp_file.name) else 'N/A'}")
            
            # Additional debugging information
            ic(f"Barcode data: {barcode_data}")
            ic(f"Barcode type: {barcode_type}")
            
            # Try to read the file content
            try:
                with open(temp_file.name, 'rb') as f:
                    file_content = f.read()
                ic(f"File content (first 100 bytes): {file_content[:100]}")
            except Exception as read_error:
                ic(f"Error reading file: {str(read_error)}")
            
            raise HTTPException(status_code=500, detail=f"Error processing image: {str(img_error)}")

        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
        
        # Create a PDF writer object
        pdf_writer = PdfWriter()
        pdf_writer.add_page(target_page)
        
        # Save the PDF to a bytes buffer
        buffer = io.BytesIO()
        pdf_writer.write(buffer)
        buffer.seek(0)
        
        # Encode the PDF as base64
        base64_pdf = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {"base64_pdf": base64_pdf}
    
    except Exception as e:
        ic(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
   uvicorn.run("app:app", reload=True, port=5051, host="0.0.0.0")
