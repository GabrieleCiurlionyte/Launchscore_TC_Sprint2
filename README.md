# LaunchScore - App Profitability Evaluator

A RAG application that helps evaluate the business potential of an Android or App Store app idea.

The app analyzes market context and supporting data to produce:

- a profitability score
- a market risk assessment
- monetization recommendations
- a go / no-go decision

It is designed to support early-stage product research by turning market signals and reference documents into a structured recommendation.

## Run the project

This repository uses [`uv`](https://docs.astral.sh/uv/) for Python project and dependency management.

After pulling the repository, install dependencies and start the Streamlit app with:

```bash
uv sync
uv run python scripts/build_index.py
uv run streamlit run main.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## First-time setup

If you do not have `uv` installed yet, install it first:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then clone the repository and run:

```bash
uv sync
uv run python scripts/build_index.py
uv run streamlit run main.py
```

Re-run `uv run python scripts/build_index.py` whenever the source PDF data changes. The Streamlit app now only loads the persisted vector store at runtime, so it does not re-embed the document corpus on every rerun.

## Testing

Tests are stored under the `tests/` folder. Example:

- `tests/tools/swotAnalysis/test_swot_analysis_tool.py`

Run all tests:

```bash
uv run pytest
```

Run only integration tests:

```bash
uv run pytest -m integration -s
```

The `integration` marker is optional, but recommended. It lets you separate slower tests that call external APIs from fast local/unit tests.

Integration tests that call OpenAI require `OPENAI_API_KEY` in your environment (or `.env` if loaded by `tests/conftest.py`).
