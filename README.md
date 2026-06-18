# Arkitect 

**Arkitect** is an AI-powered workflow planning platform that transforms a simple goal into a structured execution roadmap.

Users can enter goals such as:

> "Launch a SaaS startup in 90 days"

and Arkitect generates:

* Deliverables
* Tool Recommendations
* Step-by-Step Workflows
* AI Prompts
* Knowledge Areas
* Alternative Approaches
* Estimated Timelines

The platform combines AI-generated planning with a deterministic fallback pipeline to ensure reliable workflow generation even when external AI services are unavailable.

---

## 📸 Screenshots

### Landing Page
![Landing page](docs/landing.jpg)

### Workflow Generation

### Generated Workflow

### Workflow History

---

## ✨ Features

### AI Workflow Generation

Generate structured execution plans from natural language goals.

### Deliverable Detection

Automatically identifies key outputs required to achieve the objective.

### Tool Recommendations

Suggests relevant tools, platforms, and technologies for execution.

### AI Prompt Generation

Creates prompts that can be directly used with LLMs such as ChatGPT and Gemini.

### Knowledge Area Identification

Highlights concepts and skills that should be learned during execution.

### Alternative Strategies

Provides alternative workflow approaches and execution paths.

### Time Estimation

Generates realistic effort and timeline estimates.

### Deterministic Fallback Engine

If Gemini is unavailable or rate-limited, Arkitect automatically falls back to a deterministic workflow generation pipeline.

---

## 🏗 Architecture

```text
User
 │
 ▼
Frontend (React + TanStack Start)
 │
 ▼
Backend API (FastAPI)
 │
 ├── Gemini AI Engine
 │
 └── Deterministic Workflow Engine
          │
          ▼
      PostgreSQL
```

---

## 🛠 Tech Stack

### Frontend

* React 19
* TypeScript
* TanStack Start
* TanStack Router
* Vite
* Tailwind CSS
* Shadcn UI
* Supabase Auth

### Backend

* FastAPI
* Python
* SQLAlchemy
* Pydantic
* Async PostgreSQL

### Database

* PostgreSQL (Neon)

### Authentication

* Supabase Authentication

### AI

* Google Gemini API

### Deployment

* Vercel (Frontend)
* Render (Backend)
* Neon PostgreSQL
* Supabase

---

## 📂 Project Structure

```text
Arkitect/
│
├── frontend/
│   ├── src/
│   ├── routes/
│   ├── components/
│   └── lib/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── database/
│   │   └── auth/
│   │
│   └── tests/
│
├── docs/
│   ├── PRD.md
│   ├── DESIGN.md
│   ├── SYSTEM_CONTRACT.md
│   └── OWNERSHIP.md
│
└── README.md
```

---

## ⚙️ Local Setup

### Clone Repository

```bash
git clone https://github.com/AlfinMuhammedS/Arkitect.git
cd Arkitect
```

---

### Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create:

```env
backend/.env
```

```env
DATABASE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_JWT_SECRET=
GEMINI_API_KEY=
```

Run backend:

```bash
python -m uvicorn app.main:app --reload
```

Backend available at:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

### Frontend Setup

```bash
cd frontend

npm install
```

Create:

```env
frontend/.env
```

```env
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
VITE_API_URL=http://localhost:8000
```

Run frontend:

```bash
npm run dev
```

Frontend available at:

```text
http://localhost:3000
```

or

```text
http://localhost:5173
```

depending on configuration.

---

## 🧪 Testing

Backend tests:

```bash
cd backend

pytest
```

---

## 📈 Future Improvements

* Real-time workflow streaming
* Team collaboration
* Public workflow sharing
* Workflow export (PDF/Markdown)
* Advanced analytics
* Multi-model AI support
* Workflow templates marketplace

---

## 👨‍💻 Authors

**Alfin Muhammed S**

GitHub:
https://github.com/AlfinMuhammedS

---

## 📜 License

This project was developed for educational and portfolio purposes.
