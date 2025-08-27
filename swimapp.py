from dash import Dash, html, dcc, Input, Output, State
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_INSTRUCTIONS = """
    You are an NCAA Swim Coach.
    Create a detailed swimming workout based on the user's inputs.
    Write it in plain text, formatted by set type
    (Warmup, Drill, Main Set, Cool Down, etc).
    Include yardages for each set and an optional rationale at the end.
    Do not return JSON or code, just regular text.
    Most workouts should follow this order:
    warmup set -> kick set -> drill/prep -> main set -> pull and/or other
    Do not include race pace unless specified
    Main set should be at least half of the volume.
    Options:
        Warmup + kick set should be roughly 1/3. Main Set anywhere from 1/3 to 2/3 of the volume of the workout. Other less than 1/3. Pull can be mixed into the main set optionally.
    Other can include:
    underwater kick set, racks, dives, turns, parachutes, Fast stuff
"""

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Swim Workout Generator"),

    html.Label("Practice Type"),
    dcc.Dropdown(
        id="practice-type",
        options=[
            {"label": "Freestyle",          "value": "Free"},
            {"label": "Individual-Medley",  "value": "IM"},
            {"label": "Backstroke",         "value": "Back"},
            {"label": "Breaststroke",       "value": "Breast"},
            {"label": "Butterfly",          "value": "Fly"},
            {"label": "Race Pace",          "value": "Race Pace"}
        ],
        value="Free",
    ),

    html.Br(),
    html.Label("Pool Type"),
    dcc.RadioItems(
        id="pool-type",
        options=[
            {"label": "SCY", "value": "SCY"},
            {"label": "LCM", "value": "LCM"},
            {"label": "SCM", "value": "SCM"}
        ],
        value="SCY",
        inline=True
    ),

    html.Br(),
    html.Label("Total Yardage (N.A. for Race Pace)"),
    dcc.Slider(2000, 8000, step=250, value=4000, id="volume", marks={i: str(i) for i in range(2000, 8001, 250)}),
    html.Div(id="yardage-out", style={"fontSize": "12px", "opacity": 0.7, "marginTop": "4px"}),

    html.Br(),
    html.Button("Generate Workout", id="go", n_clicks=0),

    html.Hr(),
    html.Div(id="result", style={"whiteSpace": "pre-wrap"}),
])

@app.callback(Output("yardage-out", "children"), Input("volume", "value"))
def echo_yard(v):
    return f"Selected: {int(v)} yards" if v else ""

@app.callback(
    Output("result", "children"),
    Input("go", "n_clicks"),
    State("practice-type", "value"),
    State("pool-type", "value"),
    State("volume", "value"),
    prevent_initial_call=True,
)
def on_generate(n, ptype, pool, volume):
    if not n:
        return "Click the button to generate."
    try:
        completion = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": f"Generate a {ptype} swimming workout in a {pool} pool with a total volume of {volume} yards."}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating workout: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8051, debug=True)
