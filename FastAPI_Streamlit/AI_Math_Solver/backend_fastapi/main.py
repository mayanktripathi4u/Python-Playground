from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai, os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"],
)

class MathProblem(BaseModel):
    question: str
    
@app.post("/solve")
async def solve_math(problem: MathProblem):
    prompt = f"Solve and explain step-by-step with LaTex math formatting: {problem.question}"

    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = [
            {"role": "user", "content": prompt}
        ]
    )
    answer = response['choices'][0]['message']['content']
    return {"solution": answer}

