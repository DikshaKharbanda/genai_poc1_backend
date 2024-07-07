from fastapi import FastAPI, HTTPException, UploadFile, File
from hugchat import hugchat
from hugchat.login import Login
import easyocr
import cv2
import numpy as np
import re

EMAIL = "aditirathi0406@gmail.com"
PASSWD = "Aditi&diksha2024"
cookie_path_dir = "./cookies/"

# Initialize FastAPI app
app = FastAPI()

# Login and get cookies for the chatbot
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

# Endpoint to process the image and query the chatbot
@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform OCR
        extracted_text = perform_ocr(img)
        
        # Generate dynamic prompt
        prompt = f"In this {extracted_text} extract name, adhar number, address"

        # Query the chatbot
        query_result = str(chatbot.query(prompt, web_search=True))
        return {"result": query_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Main function to run the FastAPI app
if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)