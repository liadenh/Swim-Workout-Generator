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

<img width="1024" height="321" alt="App header and controls" src="https://github.com/user-attachments/assets/60c40647-02ec-450e-b6c6-65c991b29c07" />

<img width="985" height="652" alt="Generated workout output" src="https://github.com/user-attachments/assets/328d06ad-6026-45cb-8268-2fe6af892dc1" />

---

## Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API key  

### Installation

Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/swim-workout-generator.git
cd swim-workout-generator
```

Set up a virtual environment:
```bash
python -m venv venv
```

Activate the environment:
```bash
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file with:
```bash
OPENAI_API_KEY=your_api_key_here
```

Run the app:
```bash
python app.py
```

Visit in your browser: http://127.0.0.1:8050/

---

## Project Structure
```
├── app.py              # Main Dash app and callbacks
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment config (no secrets)
├── README.md           # Documentation
```

---

## Technologies Used

- Python (Dash, dotenv)  
- Plotly Dash for interactive UI  
- OpenAI GPT-5 for workout generation  
- Environment variables for secure API key handling  

---

## Roadmap

- Deploy live version (Render/Heroku)  
- Save workout history to database or CSV  
- Add dark mode styling with Dash Bootstrap Components  
- Export workouts to PDF for athletes/coaches  

---

## License

Distributed under the MIT License. Free to use, modify, and share.
