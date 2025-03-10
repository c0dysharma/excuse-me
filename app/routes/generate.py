import json
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from app.helper import gemini_ai_llm_call, generate_prompt, open_ai_llm
from app.types import GenerateRequest, GenerateResponse


router = APIRouter()


@router.post("/generate",
             response_model=GenerateResponse,
             summary="Generate Excuse with details")
def generate_excuse(args: GenerateRequest):
    # do LLM call with the inputs and respond
    try:
        prompt = generate_prompt(args)
        res = open_ai_llm(prompt)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    data = {
        "excuse": res,
        "prompt": prompt,
        "input": args.model_dump()
    }
    return JSONResponse(status_code=201, content=data)
