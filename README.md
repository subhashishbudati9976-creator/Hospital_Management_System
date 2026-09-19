# Hospital Appointment Agent — LangChain + OpenAI + Agentic AI

This Python project that demonstrates how to build a **multi-tool Agentic AI application with LangChain and the OpenAI API**.

> **Safety / scope:** This project uses simulated hospital data only. It is an educational demonstration of appointment workflows, tool calling, multi-tool agents, and human approval. It is **not** connected to a real hospital and must not be used for diagnosis, treatment, medication, emergency triage, or real patient care.

## you will learn

```text
Python
  ↓
OpenAI API
  ↓
LangChain ChatOpenAI
  ↓
LangChain Tools
  ↓
Multi-Tool Agent
  ↓
Human Approval
  ↓
Agentic AI Workflow
```

The agent can:

- list departments
- find doctors by department
- check demo appointment slots
- request a booking
- pause for human approval before booking
- cancel demo appointments

## Project architecture

```text
                         USER
                           ↓
                    NATURAL LANGUAGE
                           ↓
                 LANGCHAIN AGENT
                           ↓
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
   Department Tool    Doctor Tool      Slot Tool
          ↓                ↓                ↓
          └────────────────┼────────────────┘
                           ↓
                    Booking Tool
                           ↓
                  HUMAN APPROVAL
                     ↙           ↘
                 APPROVE       CANCEL
                    ↓              ↓
               Book Demo      No Booking
```

## 1. Prerequisites

Install **Python 3.10 or newer**.

Check your Python version:

### Windows

```powershell
py --version
```

or:

```powershell
python --version
```

### Linux / macOS

```bash
python3 --version
```

Install Git if you plan to push this project to GitHub.

## 2. Get an OpenAI API key

Create an API key from the OpenAI Platform:

- https://platform.openai.com/
- OpenAI API documentation: https://developers.openai.com/api/docs/quickstart

LangChain's current OpenAI integration uses the `langchain-openai` package and the `OPENAI_API_KEY` environment variable. See:

- https://docs.langchain.com/oss/python/integrations/chat/openai

**Never commit your real API key to GitHub.**

## 3. Clone or download the project

If you already have the ZIP, extract it and open a terminal in the project folder.

Expected structure:

```text
hospital-appointment-agent/
│
├── README.md
├── requirements.txt
├── app.py
├── config.py
├── test_openai.py
├── test_setup.py
├── .env.example
├── .gitignore
│
├── data/
│   └── hospital_data.py
│
└── src/
    ├── __init__.py
    ├── agent.py
    └── tools.py
```

## 4. Create a virtual environment

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
py -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, you should see something like:

```text
(.venv)
```

## 5. Install dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project requirements:

```bash
pip install -r requirements.txt
```

The main packages are:

```text
langchain
langgraph
langchain-openai
openai
python-dotenv
```

## 6. Create your `.env` file

Copy `.env.example` to `.env`.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Windows CMD

```cmd
copy .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Open `.env` and add your API key:

```text
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
MODEL_NAME=gpt-5.6-luna
```

`MODEL_NAME` is configurable. Use a model that is available to your OpenAI API project. OpenAI's current model catalog is here:

https://platform.openai.com/docs/models

If `gpt-5.6-luna` is not available to your project, replace it with a currently available model.

## 7. Important security check

Your real `.env` file should **not** be uploaded to GitHub.

The `.gitignore` file already includes:

```text
.env
.venv/
__pycache__/
*.pyc
```

Check before committing:

```bash
git status
```

You should **not** see `.env` listed as a file to commit.

## 8. Test the OpenAI API

Run:

```bash
python test_openai.py
```

Expected output:

```text
OpenAI API connection successful.
```

If this fails, check:

1. `.env` exists.
2. `OPENAI_API_KEY` is correct.
3. The key belongs to an API project with API access/credits.
4. `MODEL_NAME` is valid for your project.
5. Your internet connection is working.

## 9. Test the LangChain agent setup

Run:

```bash
python test_setup.py
```

Expected output:

```text
API key configured: True
Model: gpt-5.6-luna
Agent created: True
Setup test passed.
```

The displayed model will match your `.env` value.

## 10. Run the complete project

Run:

```bash
python app.py
```

You should see:

```text
======================================================================
HOSPITAL APPOINTMENT AGENT - LANGCHAIN + OPENAI + AGENTIC AI
CLASSROOM DEMO: ALL HOSPITAL DATA IS SIMULATED
======================================================================
```

The application then waits for natural-language requests.

## 11. Hands-on exercises

### Exercise 1 — List departments

```text
List the hospital departments.
```

The agent should use:

```text
list_departments()
```

### Exercise 2 — Find a doctor

```text
Find a dermatologist.
```

The agent should use:

```text
find_doctors()
```

### Exercise 3 — Check available slots

```text
What slots are available with Dr. Ananya Rao on 2026-10-15?
```

The agent should use:

```text
check_available_slots()
```

### Exercise 4 — Multi-tool request

```text
Find a dermatologist and tell me the available slots for Dr. Ananya Rao on 2026-10-15.
```

you should observe that the agent can use more than one tool to complete the request.

### Exercise 5 — Booking with human approval

```text
Book a dermatology appointment for Venky Naidu on 2026-10-15 at 11:00 with Dr. Ananya Rao.
```

The booking tool will pause and display:

```text
--- HUMAN APPROVAL REQUIRED ---
Patient   : Venky Naidu
Department: Dermatology
Doctor    : Dr. Ananya Rao
Date      : 2026-10-15
Time      : 11:00

This is a DEMO booking. No real hospital system is connected.

Type APPROVE to confirm, or anything else to cancel:
```

Type:

```text
APPROVE
```

Only after approval is the simulated appointment recorded.

### Exercise 6 — Cancel a booking

After a successful booking, use the returned demo booking ID, for example:

```text
Cancel appointment DEMO-0001.
```

The agent should call:

```text
cancel_appointment()
```

## 12. Understanding the Agent

The user gives a goal in natural language. The model decides which available tool(s) are appropriate, the tools return observations, and the agent continues until it can answer or reaches a stop condition.

In this project:

```text
User Goal
   ↓
Agent
   ↓
Choose Tool
   ↓
Execute Tool
   ↓
Observe Result
   ↓
Choose Next Tool (if needed)
   ↓
Final Answer
```

LangChain's current agent API uses `create_agent`, and its OpenAI integration supports tool calling. See:

- https://docs.langchain.com/oss/python/langchain/agents
- https://docs.langchain.com/oss/python/integrations/chat/openai

## 13. Why the booking tool has human approval

A booking changes application state. In an educational production-design discussion, this is a good example of a **side-effecting action** that can require explicit confirmation.

```text
Agent
  ↓
Propose Booking
  ↓
Human Approval
  ↓
Execute Booking
```

The demo therefore does not allow the LLM to silently complete a booking.

## 14. Troubleshooting

### Error: `OPENAI_API_KEY is missing`

Check that `.env` exists in the project root and contains:

```text
OPENAI_API_KEY=...
```

Then run the test again.

### Error: model not found / model not available

Change:

```text
MODEL_NAME=...
```

to a model available to your OpenAI API project. Check the current model catalog:

https://platform.openai.com/docs/models

### Error: authentication / quota / billing

Verify your OpenAI API project has API access and available usage/credits. ChatGPT subscriptions and API billing are separate products.

### Error: `No module named ...`

Activate the virtual environment again and run:

```bash
pip install -r requirements.txt
```

### PowerShell activation error

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```



## 15. Workshop extension ideas

Once the basic project works, you can extend it with:

- RAG over hospital policy PDFs
- doctor/department database instead of Python lists
- SQLite or PostgreSQL
- separate approval workflow
- appointment history
- email confirmation tool
- calendar integration
- LangGraph stateful workflow
- evaluation and tracing

## 16. Final learning architecture

```text
                 HOSPITAL APPOINTMENT AGENT
                            │
                            ▼
                         OPENAI
                            │
                            ▼
                        LANGCHAIN
                            │
                            ▼
                          AGENT
                            │
            ┌───────────────┼────────────────┐
            ↓               ↓                ↓
       Departments       Doctors           Slots
            Tool            Tool             Tool
            └───────────────┼────────────────┘
                            ↓
                       Booking Tool
                            ↓
                      HUMAN APPROVAL
                            ↓
                    DEMO APPOINTMENT
```

## Learning outcome

After completing this project, you should be able to explain and demonstrate:

- OpenAI API integration
- LangChain `ChatOpenAI`
- LangChain tools
- Tool calling
- Multi-tool agents
- Agent execution loops
- Human-in-the-loop approval
- Safe separation between an LLM and application side effects
- Basic Git/GitHub project workflow
