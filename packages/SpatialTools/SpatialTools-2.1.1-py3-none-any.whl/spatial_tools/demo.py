import dash_bootstrap_components as dbc
from dash import html
import dash
from jupyter_dash import JupyterDash

app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

spinners = html.Div(
    [
        dbc.Button(
            dbc.Spinner(size="sm"),
            color="primary",
            disabled=True,
            className="me-1",
        ),

        dbc.Spinner([
            dbc.Button(color='success', size='sm')
        ]),

        dbc.Button(
            [dbc.Spinner(size="sm"), " Loading..."],
            color="primary",
            disabled=True,
        ),

    ]
)

app.layout = spinners

app.run_server(debug=True)
