# AI SaaS Starter Kit

A production-ready FastAPI starter kit for AI-powered SaaS applications with authentication, credits system, and payment integration.

## Features

- ✅ User authentication (register, login, logout)
- ✅ JWT-based sessions with httponly cookies
- ✅ Password reset flow
- ✅ Credit system for API usage
- ✅ Clean component-based templates with Jinja2 macros
- 🚧 Stripe payment integration (coming soon)
- 🚧 AI API integration (OpenAI, Anthropic) (coming soon)

## Setup

1. **Clone the repository:**
```bash
   git clone https://github.com/rshiv1029/SaaS_Starter_Kit.git
   cd SaaS_Starter_Kit
```

2. **Create virtual environment:**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
   cp .env.example .env
   # Edit .env and change SECRET_KEY to a random string
```

5. **Run the application:**
```bash
   python run.py
```

6. **Open in browser:**
```
   http://localhost:8000
```

## Project Structure
```
app/
├── config.py          # Configuration management
├── database.py        # Database setup
├── main.py           # FastAPI application
├── models/           # SQLAlchemy models
├── routes/           # API routes
├── templates/        # Jinja2 templates
│   └── components/   # Reusable template macros
└── utils/            # Helper functions
    └── security.py   # JWT & password hashing
```

## Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite (development) / PostgreSQL (production)
- **Auth:** JWT tokens with httponly cookies
- **Templates:** Jinja2 with Tailwind CSS
- **Password Hashing:** bcrypt

## Security Notes

⚠️ **Important:** Always change the `SECRET_KEY` in your `.env` file before deploying to production!

## License

MIT License - feel free to use for personal or commercial projects.