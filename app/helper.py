import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from loguru import logger
from app.types import GenerateRequest
from dotenv import load_dotenv

load_dotenv()


GENERATE_EXCUSE_PROMPT = PromptTemplate.from_template("""Generate a {type} WhatsApp/Slack text for a person who needs {days_off} days off from work. The excuse should be believable and professional so that it is acceptable to a manager.  
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
    args = args.model_copy()
    args.type = excuse_map.get(args.type, "funny")

    return GENERATE_EXCUSE_PROMPT.format(**args.model_dump())


open_ai_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

gemini_ai_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def clean_output(output: str) -> str:
    """
    Clean the output from the LLM invoke method.

    Args:
        output (str): The raw output from the LLM invoke method.

    Returns:
        str: The cleaned output.
    """
    # Remove leading and trailing quotes and whitespace
    cleaned_output = output.strip().strip('"')
    return cleaned_output


def open_ai_llm_call(prompt: str) -> str:
    try:
        res = open_ai_llm.invoke(prompt).content
        cleaned_res = clean_output(res)
        return cleaned_res
    except Exception as e:
        logger.error(e)
        raise Exception("Error getting response from LLM")


def gemini_ai_llm_call(prompt: str) -> str:
    try:
        res = gemini_ai_llm.invoke(prompt).content
        cleaned_res = clean_output(res)
        return cleaned_res
    except Exception as e:
        logger.error(e)
        raise Exception("Error getting response from LLM")


def llm_call(prompt: str) -> dict:
    provider = os.getenv("LLM_PROVIDER", "gemini")

    if provider == "openai":
        res = open_ai_llm_call(prompt)
    else:
        res = gemini_ai_llm_call(prompt)

    return {
        "content": res,
        "provider": provider
    }
