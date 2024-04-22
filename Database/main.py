from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
from pydantic import BaseModel
import redis
import uuid  # Import the uuid module to generate UUIDs
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

redis_conn = get_redis_connection(
    host="redis-14293.c212.ap-south-1-1.ec2.redns.redis-cloud.com",
    port=14293,
    password="er9OV9w3zdOW68yrXWvIg0YgMLnGePvq",
    decode_responses=True
)

class Inputs(BaseModel):
    title: str
    description: str
    resume: str

    class Meta:
        database = redis_conn

@app.get("/")
async def read_root():
    # Instead of returning "Hello World!", return the HTML file
    with open("static/main.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/inputs")
def all():
    return [format(pk) for pk in Inputs.all_pks()]

def format(pk:str):
    inputs = Inputs.get(pk)
    return {
        'id': pk,
        'title': inputs.title,
        'description': inputs.description,
        'resume': inputs.resume
    }

@app.post("/inputs")
async def create(inputs: Inputs, resume: UploadFile = File(...)):
    try:
        unique_id = str(uuid.uuid4())
        key = f"input:{unique_id}"
        inputs_dict = inputs.dict()
        
        # Save the uploaded resume file
        resume_content = await resume.read()
        resume_path = f"data/{unique_id}.pdf"
        with open(resume_path, "wb") as resume_file:
            resume_file.write(resume_content)

        # Convert PDF to text
        resume_text = textract.process(resume_path).decode("utf-8")
        inputs_dict['resume_text'] = resume_text

        # Save the data to Redis
        redis_conn.hmset(key, inputs_dict)

        inputs_dict['id'] = unique_id
        return inputs_dict

    except Exception as e:
        # Handle exceptions (e.g., log the error)
        print(f"An error occurred: {e}")
        return {"error": "An error occurred while processing the request"}