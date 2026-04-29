# Streamlit Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold a minimal Streamlit app with a title, isolated in a virtual environment, and verified running at localhost:8501.

**Architecture:** Flat layout — `app.py` at root is the sole entry point; a `.venv/` virtual environment isolates dependencies; `requirements.txt` pins the installed packages. No pages, no src layout, no data layer.

**Tech Stack:** Python 3.14, Streamlit, streamlit.testing.v1 (for app-level tests)

---

## File Map

| Path | Action | Responsibility |
|------|--------|----------------|
| `.venv/` | Create (command) | Isolated Python environment |
| `requirements.txt` | Create | Pin Streamlit version |
| `app.py` | Create | Single-page Streamlit entry point |
| `tests/test_app.py` | Create | Verify app title renders correctly |

---

### Task 1: Create virtual environment

**Files:**
- No files written — `.venv/` is created by command and is gitignored

- [ ] **Step 1: Create the venv**

```bash
cd /Users/alexalabra/isba-4715/basket-craft-dashboard
python3 -m venv .venv
```

- [ ] **Step 2: Verify the venv Python works**

```bash
.venv/bin/python --version
```

Expected output: `Python 3.14.x`

- [ ] **Step 3: Commit (nothing to commit — .venv is gitignored)**

No commit needed for this task.

---

### Task 2: Install Streamlit and pin requirements

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: Install Streamlit into the venv**

```bash
.venv/bin/pip install streamlit
```

Expected: pip resolves and installs streamlit and its dependencies.

- [ ] **Step 2: Pin installed packages to requirements.txt**

```bash
.venv/bin/pip freeze > requirements.txt
```

- [ ] **Step 3: Verify streamlit is listed**

```bash
grep -i streamlit requirements.txt
```

Expected output (version may differ): `streamlit==1.x.x`

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "chore: add Streamlit dependency"
```

---

### Task 3: Write failing test for app title

**Files:**
- Create: `tests/test_app.py`

- [ ] **Step 1: Create the tests directory**

```bash
mkdir -p tests
```

- [ ] **Step 2: Write the failing test**

Create `tests/test_app.py`:

```python
from streamlit.testing.v1 import AppTest


def test_dashboard_title():
    at = AppTest.from_file("../app.py")
    at.run()
    assert at.title[0].value == "BasketCraft Dashboard"
```

- [ ] **Step 3: Run the test — verify it fails**

```bash
.venv/bin/pytest tests/test_app.py -v
```

Expected: `ERROR` or `FAILED` — `app.py` does not exist yet.

---

### Task 4: Create app.py and make the test pass

**Files:**
- Create: `app.py`

- [ ] **Step 1: Create app.py**

```python
import streamlit as st

st.title("BasketCraft Dashboard")
```

- [ ] **Step 2: Run the test — verify it passes**

```bash
.venv/bin/pytest tests/test_app.py -v
```

Expected output:
```
tests/test_app.py::test_dashboard_title PASSED
```

- [ ] **Step 3: Commit**

```bash
git add app.py tests/test_app.py
git commit -m "feat: add minimal Streamlit dashboard with title"
```

---

### Task 5: Run the app and verify in browser

**Files:** None modified

- [ ] **Step 1: Start the Streamlit dev server**

```bash
.venv/bin/streamlit run app.py
```

Expected output includes:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

- [ ] **Step 2: Open browser and verify**

Navigate to `http://localhost:8501`. You should see a white page with the heading **"BasketCraft Dashboard"** and nothing else.

- [ ] **Step 3: Stop the server**

Press `Ctrl+C` in the terminal.
