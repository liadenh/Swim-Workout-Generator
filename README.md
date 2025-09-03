# Swim Workout Generator

An AI-powered web app that generates customized NCAA-style swim workouts using Dash and OpenAI GPT-5.  
This project demonstrates full-stack development skills: interactive UI design, API integration, secure environment configuration, database design, and a deployment-ready structure.  
Currently adopted by the Johns Hopkins varsity swim team during preseason training (6k–8k yard practices).

---

## Features

- Interactive dashboard: select practice type, pool type (SCY/LCM/SCM), and total volume  
- AI-generated workouts: formatted with warmup → kick → drill → main set → pull/other  
- Adaptive recommendations: SQLite database stores swimmer profiles & past times to tailor send-offs and pacing  
- Race Pace handling: adjusts automatically for high-intensity training  
- Error handling: graceful feedback for invalid API calls  
- Scalable design: extendable with new training types or export options  

---

## Demo

<img width="1508" height="803" alt="image" src="https://github.com/user-attachments/assets/683a55cf-d9ef-4637-a933-a8900bf4be6b" />
<img width="604" height="210" alt="image" src="https://github.com/user-attachments/assets/8bf9c21e-ea10-4b36-ae03-a092bd79c3b2" />
<img width="701" height="166" alt="image" src="https://github.com/user-attachments/assets/aa04e6cd-3839-4f91-8933-0331ea12c188" />


---

---

## Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API key

### Installation with uv

```bash
# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/swim-workout-generator.git
cd swim-workout-generator

# 2. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies
uv sync

# 4. Create a .env file with your API key
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 5. Initialize the database (creates swim.db with swim_times table)
uv run python -c "import swimapp; swimapp.init_db()"

# 6. Run the app
uv run python swimapp.py
```


## Project Structure
```
├── swimapp.py          # Main Dash app and callbacks
├── db.py               # Database init and helper functions (if separated)
├── pyproject.toml      # Project dependencies (uv/hatch)
├── .env.example        # Example environment config (no secrets)
├── swim.db             # SQLite database (auto-created on first run)
├── README.md           # Documentation
```

## Technologies Used
---

- Python 3.9+  
- Plotly Dash (UI framework)  
- dash-bootstrap-components (Bootstrap/Bootswatch styling)  
- SQLite (swimmer profiles & workout history)  
- OpenAI Python SDK (chat completions)  
- python-dotenv (loads .env config)  
- uv (dependency management & runner)  

## Roadmap
---

- Deploy live version (Render/Heroku/Fly.io)  
- Save and visualize workout history in the dashboard  
- Add dark mode styling with Dash Bootstrap Components  
- Export workouts to PDF/CSV for athletes/coaches  
- Extend DB schema for meet results and long-term progression tracking  

## License
---

Distributed under the MIT License. Free to use, modify, and share.

