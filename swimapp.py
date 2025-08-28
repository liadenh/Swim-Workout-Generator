from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
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

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.CERULEAN, dbc.icons.BOOTSTRAP],
    title="Swim Workout Generator",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("🏊 Swim Workout Generator", className="fw-bold"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href="#")),
                    dbc.NavItem(dbc.NavLink("About", href="#")),
                ],
                className="ms-auto",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
    sticky="top",
)

controls_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Setup", className="card-title mb-3"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Practice Type"),
                            dcc.Dropdown(
                                id="practice-type",
                                options=[
                                    {"label": "Freestyle", "value": "Free"},
                                    {"label": "Individual-Medley", "value": "IM"},
                                    {"label": "Backstroke", "value": "Back"},
                                    {"label": "Breaststroke", "value": "Breast"},
                                    {"label": "Butterfly", "value": "Fly"},
                                    {"label": "Race Pace", "value": "Race Pace"},
                                ],
                                value="Free",
                                clearable=False,
                                className="mb-3",
                            ),
                        ],
                        md=6,
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Pool Type"),
                            dbc.RadioItems(
                                id="pool-type",
                                options=[{"label": x, "value": x} for x in ("SCY", "LCM", "SCM")],
                                value="SCY",
                                inline=True,
                                className="mb-3",
                            ),
                        ],
                        md=6,
                    ),
                ],
                className="g-3",
            ),
            dbc.Label("Total Yardage (N.A. for Race Pace)"),
            dcc.Slider(
                id="volume",
                min=2000, max=8000, step=500, value=4000,
                marks={
                    i: (f"{i//1000}k" if i % 1000 == 0 else f"{i/1000:.1f}k")
                    for i in range(2000, 8001, 500)
                },
                tooltip={"placement": "bottom", "always_visible": True},
            ),
            html.Small(id="yardage-out", className="text-muted d-block mt-1"),
            dbc.Button("Generate Workout", id="go", n_clicks=0, color="primary", className="mt-3"),
        ]
    ),
    className="shadow-sm",
)

result_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Result", className="card-title"),
            html.Hr(),
            html.Pre(id="result", className="mb-0", style={"whiteSpace": "pre-wrap"}),
        ]
    ),
    className="shadow-sm",
)



app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(controls_card, lg=5),
                        dbc.Col(result_card, lg=7),
                    ],
                    className="g-4 my-4",
                ),
            ],
            fluid=True,
        ),
    ]
)



@app.callback(Output("yardage-out", "children"), Input("volume", "value"))
def echo_yard(v):
    return f"Selected: {int(v):,} yards ({v/1000:.1f}k)" if v else ""

@app.callback(
    Output("volume", "disabled"),
    Output("yardage-out", "style"),
    Input("practice-type", "value"),
)
def toggle_volume(ptype):
    disabled = (ptype == "Race Pace")
    style = {"fontSize": "12px", "opacity": (0.3 if disabled else 0.7), "marginTop": "4px"}
    return disabled, style

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
                {"role": "user", "content": f"Generate a {ptype} swimming workout in a {pool} pool with a total volume of {volume} yards."},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[Error] {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8051, debug=True)
