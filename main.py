from fastapi import FastAPI, HTTPException, UploadFile, File
from hugchat import hugchat
from hugchat.login import Login
import easyocr
import cv2
import numpy as np
import re
import mysql.connector
from mysql.connector import Error

EMAIL = "aditirathi0406@gmail.com"
PASSWD = "Aditi&diksha2024"
cookie_path_dir = "./cookies/"

app = FastAPI()
class LoginRequest():
    email: str
    password: str
@app.post("/login")
async def login(request: LoginRequest):
    try:
        connection = mysql.connector.connect(
        host='localhost',  # e.g., 'localhost'
        database='EKYC',   # Your database name
        user='root',  # Your MySQL username
        password='kharbanda'  
    )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE EMAIL = %s AND PASSWORD = %s"
            cursor.execute(query, (request.email, request.password))
            user = cursor.fetchone()

            if user:
                return {"message": "Login successful", "redirect_url": "/landing-page"}
            else:
                raise HTTPException(status_code=401, detail="Invalid email or password")
    except Error as e:
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

try:
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
except Exception as e:
    raise Exception(f"Failed to initialize chatbot: {e}")
# Function to perform OCR on the uploaded image
def perform_ocr(image: np.ndarray):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image)
    text_list = [item[1] for item in result]
    return text_list
# Endpoint to process Aadhaar card image and query the chatbot
@app.post("/process-aadhaar/")
async def process_aadhaar(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform OCR
        extracted_text = perform_ocr(img)
        
        # Generate dynamic prompt
        prompt = f"In this {extracted_text} extract name, Aadhaar number, father's name and address"

        # Query the chatbot
        query_result = str(chatbot.query(prompt, web_search=True))
        return {"result": query_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/process-pan/")
async def process_pan(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform OCR
        extracted_text = perform_ocr(img)
        
        # Generate dynamic prompt
        prompt = f"In this {extracted_text} extract name, PAN number, and Date of Birth"

        # Query the chatbot
        query_result = str(chatbot.query(prompt, web_search=True))
        return {"result": query_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Endpoint to verify both Aadhaar and PAN card images
@app.post("/verify/")
async def verify(aadhaar_file: UploadFile = File(...), pan_file: UploadFile = File(...)):
    try:
        # Process Aadhaar file
        aadhaar_contents = await aadhaar_file.read()
        aadhaar_nparr = np.frombuffer(aadhaar_contents, np.uint8)
        aadhaar_img = cv2.imdecode(aadhaar_nparr, cv2.IMREAD_COLOR)
        aadhaar_text = perform_ocr(aadhaar_img)
        aadhaar_prompt = f"In this {aadhaar_text} extract name, Aadhaar number, and address"
        aadhaar_result = str(chatbot.query(aadhaar_prompt, web_search=True))

        # Process PAN file
        pan_contents = await pan_file.read()
        pan_nparr = np.frombuffer(pan_contents, np.uint8)
        pan_img = cv2.imdecode(pan_nparr, cv2.IMREAD_COLOR)
        pan_text = perform_ocr(pan_img)
        pan_prompt = f"In this {pan_text} extract name, PAN number, and Date of Birth"
        pan_result = str(chatbot.query(pan_prompt, web_search=True))

        return {
            "aadhaar_result": aadhaar_result,
            "pan_result": pan_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

