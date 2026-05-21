import os
import json
import pytest

from rag.tools.swotAnalysis.swotAnalysisTool import generate_swot_analysis

pytestmark = pytest.mark.integration

@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY") or os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="OPENAI_API_KEY not set or RUN_INTEGRATION_TESTS is not enabled"
)
def test_generate_swot_analysis_real_call():
    result = generate_swot_analysis.invoke({
        "idea_summary": "AI travel planner",
        "target_market": "Digital nomads",
        "context": "Growing remote work market"
    })
    print("\nSWOT result:\n" + json.dumps(result, indent=2, ensure_ascii=False))

    assert isinstance(result, dict)
    for key in ["strengths", "weaknesses", "opportunities", "threats"]:
        assert key in result
        assert isinstance(result[key], list)
        assert len(result[key]) > 0
    assert "overall_assessment" in result
    assert isinstance(result["overall_assessment"], str)
    assert result["overall_assessment"].strip()
