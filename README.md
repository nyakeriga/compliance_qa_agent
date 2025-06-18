
# 🧠 AI Compliance & News Intelligence Portal

A Django-based smart system combining document-driven compliance Q\&A and real-time news alerting based on uploaded rule resources. Built to empower regulatory insight and automated monitoring.

---

## 🚀 Features

### 🔹 Agent 1 – Compliance QA

* Upload compliance-related PDFs/ZIPs
* Ask questions via a smart interface
* Answers based on internal documents + online web sources

### 🔹 Agent 2 – News Intelligence

* Upload rule/resource documents (e.g., Medicare.txt)
* Monitor live news feeds (RSS)
* Trigger alerts and email notifications when news matches rules
* View alert history via web UI

---

## 🛠️ Technologies

* **Django 5.2** (Admin, Routing, ORM)
* **LangChain** for LLM integration
* **OpenAI Embeddings + FAISS** for semantic search
* **Feedparser** for RSS aggregation
* **ChromaDB** + optional web scraping

---

## ⚙️ Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/your-org/ai-compliance-portal.git
cd ai-compliance-portal
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Start development server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Usage Guide

### Agent 1 – Compliance QA

* Upload documents to `/agent1/upload/`
* Ask questions at `/agent1/ask/`

### Agent 2 – News Intelligence

* Upload resource file at `/agent2/resource/`
* Trigger news scan at `/agent2/fetch/`
* View alerts at `/agent2/alerts/`

---

## ✉️ Email Alert Setup

Edit `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

> Use Gmail App Password or SMTP credentials

---

## 🧾 License

MIT License. © Your Company / Client Name 2025

---

## 🤝 Credits

Built with ❤️ by elite devs & AI engineers.
Powerful. Smart. Custom. Exactly as required.
