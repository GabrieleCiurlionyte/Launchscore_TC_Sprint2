import logging

from langchain.chat_models import init_chat_model
from langchain.tools import tool

from settings import get_settings
from rag.tools.swotAnalysis.swot_analysis_input import SWOTInput
from rag.tools.swotAnalysis.swot_analysis_output import SWOTOutput
from rag.tools.swotAnalysis.swot_prompt import SWOT_PROMPT

logger = logging.getLogger(__name__)
settings = get_settings()

model = init_chat_model(
    settings.openai_model,
    api_key=settings.openai_api_key,
    temperature=0,
    timeout=20,
    max_tokens=1000,
    max_retries=2,
).with_structured_output(SWOTOutput)

@tool(args_schema=SWOTInput)
def generate_swot_analysis(
    idea_summary: str,
    target_market: str,
    context: str = "",
) -> dict:
    """
    Generate SWOT analysis for an app idea using provided market context.
    """

    logger.info(
        "Calling SWOT analysis tool | idea=%s | target=%s",
        idea_summary,
        target_market,
    )

    conversation = [
        ("system", SWOT_PROMPT),
        ("user", f"Summary: {idea_summary}\nTarget: {target_market}\nContext: {context}")
    ]

    try:
        result: SWOTOutput = model.invoke(conversation)

        logger.info(
            "SWOT analysis generated successfully | strengths=%d | weaknesses=%d",
            len(result.strengths),
            len(result.weaknesses),
        )

        return result.model_dump()

    except Exception as e:
        logger.exception("SWOT analysis generation failed")
        raise RuntimeError(f"Failed to generate SWOT analysis: {str(e)}")
