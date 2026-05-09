import logging

from app.domain.feasability_form_input import FeasabilityFormInput
from rag.prompts.user_prompt import build_feasibility_user_prompt

logger = logging.getLogger(__name__)

def run_feasibility_analysis(agent, form_input: FeasabilityFormInput, thread_id: str):
    user_prompt = build_feasibility_user_prompt(form_input)

    response = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        },
        config={"configurable": {"thread_id": thread_id}}
    )

    return response["structured_response"]
            
