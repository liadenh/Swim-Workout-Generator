# Swim Workout Generator

An AI-powered web app that generates customized NCAA-style swim workouts using Dash and OpenAI GPT-5.  
This project demonstrates full-stack development skills: interactive UI design, API integration, secure environment configuration, and a deployment-ready structure. Currently used by our varsity team during preseason to plan 6k–8k practices.

---

## Features

- Interactive dashboard: select practice type, pool type (SCY/LCM/SCM), and total volume  
- AI-generated workouts: formatted with warmup → kick → drill → main set → pull/other  
- Race Pace handling: adjusts automatically for high-intensity training  
- Error handling: graceful feedback for invalid API calls  
- Scalable design: extendable with new training types or export options  

---

## Demo

<img width="1508" height="803" alt="image" src="https://github.com/user-attachments/assets/683a55cf-d9ef-4637-a933-a8900bf4be6b" />

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

# 5. Run the app
uv run python swimapp.py
```


## Project Structure
```
├── swimapp.py          # Main Dash app and callbacks
├── pyproject.toml      # Project dependencies (uv)
├── .env.example        # Example environment config (no secrets)
├── README.md           # Documentation
```


## Technologies Used

- Python 3.9+
- Plotly Dash (UI framework)
- dash-bootstrap-components (Bootstrap/Bootswatch styling)
- OpenAI Python SDK (chat completions)
- python-dotenv (loads .env config)
- uv (dependency management & runner)

---

## Roadmap

- Deploy live version (Render/Heroku)  
- Save workout history to database or CSV  
- Add dark mode styling with Dash Bootstrap Components  
- Export workouts to PDF for athletes/coaches  

---

## License

Distributed under the MIT License. Free to use, modify, and share.
