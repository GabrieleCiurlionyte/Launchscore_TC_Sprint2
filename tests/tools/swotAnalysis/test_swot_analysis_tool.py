# tests/tools/swotAnalysis/test_swot_analysis_tool_integration.py
import os
import pytest

from rag.tools.swotAnalysis.swotAnalysisTool import generate_swot_analysis

pytestmark = pytest.mark.integration

@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)
def test_generate_swot_analysis_real_call():
    result = generate_swot_analysis.invoke({
        "idea_summary": "AI travel planner",
        "target_market": "Digital nomads",
        "context": "Growing remote work market"
    })

    assert isinstance(result, dict)
    for key in ["strengths", "weaknesses", "opportunities", "threats"]:
        assert key in result
        assert isinstance(result[key], list)
        assert len(result[key]) > 0