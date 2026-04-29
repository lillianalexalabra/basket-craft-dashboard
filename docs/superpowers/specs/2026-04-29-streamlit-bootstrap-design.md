# Streamlit Bootstrap Design

**Date:** 2026-04-29
**Scope:** Minimal Streamlit app scaffold for BasketCraft Dashboard

## Summary

Bootstrap an empty Streamlit dashboard in the existing `basket-craft-dashboard` repo using a flat project layout with a Python virtual environment.

## Structure

```
basket-craft-dashboard/
├── .venv/              # virtual environment (git-ignored)
├── app.py              # single entry point
├── requirements.txt    # pinned dependencies
├── .env                # existing env file
└── .gitignore          # existing
```

## Environment

- Python 3.14.2 (system)
- Virtual environment at `.venv/` via `python3 -m venv`
- Streamlit installed into `.venv/` and pinned in `requirements.txt`

## App

`app.py` contains a single `st.title("BasketCraft Dashboard")` call — no other content.

## Running

```bash
source .venv/bin/activate
streamlit run app.py
```

## Out of Scope

- Multi-page layout (`pages/`)
- `src/` package structure
- Any charts, data, or widgets beyond the title
