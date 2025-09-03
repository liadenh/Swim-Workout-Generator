from dash import Dash, html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv
from openai import OpenAI
import sqlite3

# ------------------------ Setup ------------------------
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

DB_NAME = "swim.db"

def init_db():
    """Create the table and a unique index for (firstName,lastName,event)."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS swim_times (
                firstName TEXT NOT NULL,
                lastName  TEXT NOT NULL,
                event     TEXT NOT NULL,
                time      TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_swim_unique
            ON swim_times(firstName, lastName, event)
        """)
        conn.commit()

def _to_seconds(s: str) -> float:
    """Parse 'm:ss.xx' or 'mm:ss' → total seconds (float)."""
    s = s.strip()
    if ":" not in s:
        # Try raw seconds like '62.2'
        return float(s)
    m, sec = s.split(":")
    return int(m)*60 + float(sec)

def load_swimmer_summary(first: str, last: str) -> str:
    """Return a compact text summary of DB times for the swimmer."""
    if not (first and last):
        return "No swimmer name provided."
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT event, time
            FROM swim_times
            WHERE firstName = ? AND lastName = ?
            ORDER BY event
        """, (first.strip(), last.strip()))
        rows = cur.fetchall()
    if not rows:
        return "No stored times for this swimmer."
    lines = []
    for e, t in rows:
        try:
            lines.append(f"{e}: {t} ({_to_seconds(t):.2f} s)")
        except Exception:
            lines.append(f"{e}: {t}")
    return "Past times:\n" + "\n".join(lines)

# ------------------------ App ------------------------
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

log_form_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Log a Swim Time", className="card-title mb-3"),
            dbc.Row(
                [
                    dbc.Col(dbc.Input(id="first-name", placeholder="First name", type="text"), md=6),
                    dbc.Col(dbc.Input(id="last-name", placeholder="Last name", type="text"), md=6),
                ],
                className="g-2 mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Input(id="event-input", placeholder='Event (e.g., "100 Freestyle")', type="text"), md=8),
                    dbc.Col(dbc.Input(id="time-input", placeholder='Time (e.g., "1:02.22")', type="text"), md=4),
                ],
                className="g-2 mb-2",
            ),
            dbc.Button("Save Time", id="save-btn", color="success", className="mt-1"),
            dbc.Alert(id="save-status", is_open=False, duration=3500, className="mt-3"),
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
                dbc.Row(
                    [
                        dbc.Col(log_form_card, lg=6),
                    ],
                    className="g-4 mb-5",
                ),
            ],
            fluid=True,
        ),
    ]
)

# ------------------------ Callbacks ------------------------

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
    State("first-name", "value"),
    State("last-name", "value"),
    State("event-input", "value"),
    State("time-input", "value"),
    prevent_initial_call=True,
)
def on_generate(n, ptype, pool, volume, first, last, event_name, time_str):
    if not n:
        return "Click the button to generate."

    summary = load_swimmer_summary(first, last)

    #fallback
    fallback_line = ""
    try:
        if summary.startswith("No stored times") and event_name and time_str:
            secs = _to_seconds(time_str)
            fallback_line = f"\nRecent (unsaved) entry: {event_name}: {time_str} ({secs:.2f} s)"
    except Exception:
        fallback_line = "\nRecent (unsaved) entry present but could not parse."

    user_prompt = (
        f"Generate a {ptype} swimming workout in a {pool} pool with a total volume of {volume} yards.\n\n"
        f"{summary}{fallback_line}\n"
        "Use these times to choose realistic send-offs and pacing."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": user_prompt},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[Error] {e}"

#update/save swimmer time
@app.callback(
    Output("save-status", "children"),
    Output("save-status", "color"),
    Output("save-status", "is_open"),
    Input("save-btn", "n_clicks"),
    State("first-name", "value"),
    State("last-name", "value"),
    State("event-input", "value"),
    State("time-input", "value"),
    prevent_initial_call=True,
)
def save_time(n, first, last, event_name, time_str):
    for v in (first, last, event_name, time_str):
        if not (v and str(v).strip()):
            return ("Please fill in all fields.", "warning", True)

    first = first.strip()
    last = last.strip()
    event_name = event_name.strip()
    time_str = time_str.strip()

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE swim_times
                SET time = ?
                WHERE firstName = ? AND lastName = ? AND event = ?
                """,
                (time_str, first, last, event_name),
            )
            updated = (cur.rowcount > 0)
            if not updated:
                cur.execute(
                    """
                    INSERT INTO swim_times (firstName, lastName, event, time)
                    VALUES (?, ?, ?, ?)
                    """,
                    (first, last, event_name, time_str),
                )
            conn.commit()

        msg = "Updated time." if updated else "Saved new time."
        color = "info" if updated else "success"
        return (msg, color, True)

    except Exception as e:
        return (f"Error: {e}", "danger", True)


if __name__ == "__main__":
    init_db()  
    app.run(host="0.0.0.0", port=8051, debug=True)