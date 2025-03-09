

import os
from langchain_openai import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from loguru import logger
from app.types import GenerateRequest
from dotenv import load_dotenv

load_dotenv()


GENERATE_EXCUSE_PROMPT = PromptTemplate.from_template("""Generate a {type} WhatsApp/Slack text for a {job_role} who needs {days_off} days off from work. The excuse should be believable and professional so that it is acceptable to a manager.  
{constraints}  
Ensure the excuse is realistic, polite, simple and justifiable while keeping it concise, not more than 30 words,  
Generate text which are ready to sent and return only 1 text""")

excuse_map = {
    "serious": "Serious excuse (realistic & professional)",
    "funny": "Funny excuse (wild & creative)",
    "extreme": "Extreme excuse (outrageous but possibly believable)"
}

if "OPENAI_API_KEY" not in os.environ:
    logger.critical("No OPEN_API_KEY found")

if "GOOGLE_API_KEY" not in os.environ:
    logger.critical("No GOOGLE_API_KEY found")


def generate_prompt(args: GenerateRequest):
    args.type = excuse_map.get(args.type, "funny")

    return GENERATE_EXCUSE_PROMPT.format(**args.model_dump())


open_ai_llm = OpenAI()

gemini_ai_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def open_ai_llm_call(prompt: str):
    try:
        res = open_ai_llm.invoke(prompt)
    except Exception as e:
        logger.error(e)
        raise Exception("Error getting response from LLM")
    return res


def gemini_ai_llm_call(prompt: str):
    try:
        res = gemini_ai_llm.invoke(prompt)
    except Exception as e:
        logger.error(e)
        raise Exception("Error getting response from LLM")
    return res.content
