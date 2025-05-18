import json
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import logging
import httpx

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OpenAI API Proxy")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client (API key is read from OPENAI_API_KEY env variable)
client = OpenAI()

# Request model
class CompletionRequest(BaseModel):
    prompt: str
    model: str = "ft:gpt-4o-mini-2024-07-18:personal:cbt-clf-v1:BYBtmgda:ckpt-step-126"
    temperature: float = 0.2



@app.get("/")
async def  root():
    return {"message": "OpenAI API Proxy"}

def get_advice_prompt():
    return """
    You are a CBT therapist. You are given a list of CBT techniques and a patient's personal information, education, family problem, presenting problem and medical history. 
    You are to return a list of CBT techniques that the counselor could use for the patient.
    The list should be in the following format:
    [
        {
            "name": "CBT technique name",
            "description": "A description of the CBT technique",
            "implementation": "A plan on how to implement the CBT technique based on the patient's information",
            "possible_diagnosis": "A list of possible mental disorders the patient may have"
        }
    ]
    """


class CBTAdvice(BaseModel):
    name: str = Field(description="The name of the CBT technique")
    description: str = Field(description="A description of the CBT technique")
    implementation: str = Field(description="A plan on how to implement the CBT technique based on the patient's information")
    possible_diagnosis: str = Field(description="A list of possible mental disorders the patient may have")


class CBTList(BaseModel):  
    cbt_list: list[CBTAdvice] = Field(description="A list of CBT techniques that the counselor could use for the patient")

# Response model
class CompletionResponse(BaseModel):
    data: list[CBTAdvice]

@app.post("/api/completion", response_model=CompletionResponse)
async def get_completion(request: CompletionRequest):
    try:
        logger.info(f"Requesting completion for model: {request.model}")
        
        cbt_diagnosis= client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:cbt-clf-v1:BYBtmgda:ckpt-step-126",
            messages=[
                {"role": "system", "content": "You are a CBT therapist. Respond ONLY with a comma-separated list of CBT techniques."},
                {"role": "user", "content": request.prompt}
            ],
            temperature=0.2
        )

        cbt_diagnosis = cbt_diagnosis.choices[0].message.content
        cbt_advice = client.responses.parse(
            model="gpt-4o-mini-2024-07-18",
            input=[
                {"role": "system", "content": get_advice_prompt(), },
                {"role": "user", "content": f" ###patient's information: ${request.prompt} ,\n\n ###cbt_diagnosis: ${cbt_diagnosis}"}
            ],
            temperature=0.3,
            text_format=CBTList,
        )
        
        # Extract structured CBT advice list
        result: CBTList = cbt_advice.output_parsed
        return CompletionResponse(data=result.cbt_list)
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")

# comment for render deployment
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 