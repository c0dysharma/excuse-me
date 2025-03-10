import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.helper import generate_prompt, llm_call
from app.types import GenerateRequest, GenerateResponse


router = APIRouter()


@router.post("/generate",
             response_model=GenerateResponse,
             summary="Generate Excuse with details")
def generate_excuse(args: GenerateRequest):
    # do LLM call with the inputs and respond
    res: dict
    try:
        prompt = generate_prompt(args)
        res = llm_call(prompt)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    data = {
        "excuse": res['content'],
        "provider": res['provider'],
        "prompt": prompt,
        "input": args.model_dump()
    }
    return JSONResponse(status_code=201, content=data)
