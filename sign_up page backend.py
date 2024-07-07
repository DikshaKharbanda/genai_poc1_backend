from fastapi import FastAPI, HTTPException, Form, Depends
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'EKYC',
    'user': 'root',
    'password': 'xyz'
}

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Function to connect to the database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail="Database connection failed")

# Signup endpoint
@app.post("/signup")
async def signup(request: SignupRequest):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (request.email,))
        user = cursor.fetchone()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        # Insert new user
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (request.name, request.email, request.password))
        connection.commit()
        return {"message": "Signup successful", "redirect_url": "/login"}
    except Error as e:
        raise HTTPException(status_code=500, detail="Failed to signup")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Login endpoint
@app.post("/login")
async def login(request: LoginRequest):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (request.email, request.password))
        user = cursor.fetchone()
        
        if user:
            return {"message": "Login successful", "redirect_url": "/landing-page"}
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Error as e:
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Forgot password endpoint
@app.post("/forgot-password")
async def forgot_password(email: str = Form(...)):
    # Implement your forgot password logic here
    return {"message": "Password reset link has been sent to your email"}

# Endpoint for the landing page
@app.get("/landing-page")
async def landing_page():
    return {"message": "Welcome to the landing page!"}

# Run the server using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
