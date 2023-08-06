import logging

from dash import Dash, html, dcc, Input, Output, dash_table
from dash.exceptions import PreventUpdate

import collections
import pandas as pd
import jsonpickle
import dash_bootstrap_components as dbc
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
from jupyter_dash import JupyterDash

app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
import dash_uploader as du


class TestDash:
    meta_data = None

    @classmethod
    def dash_app(cls):
        du.configure_upload(app, "./__cache__")

        app.layout = html.Div([

            dcc.Store(id='memory-output'),
            dcc.Store(id='memory-output-meta'),
            dcc.Dropdown(id='memory-countries'),
            du.Upload(
                id='upload_spatial_tools',
                text='SpatialTools obj',
                filetypes=['pickle', 'gz', 'pkl', 'csv']
            )
        ])

        @du.callback(
            Output('memory-output', 'data'),
            id='upload_spatial_tools',
        )
        def load_up(status: du.UploadStatus):
            logging.info(cls.meta_data)
            cls.meta_data = pd.read_csv(str(status.latest_file))

            return str(status.latest_file)

        # @app.callback(
        #     Output('memory-output-meta', 'data'),
        #     Input('memory-output', 'data')
        # )
        # def get_meta_data(meta_data):
        #
        #     return meta_data

        @app.callback(
            Output('memory-countries', 'options'),
            Input('memory-output', 'data')
        )
        def show_countries(meta_data):
            # print('meta_data ---> {}'.format(meta_data))
            # meta_data = jsonpickle.decode(meta_data)
            # assert obj.name == meta_data.name
            logging.info(cls.meta_data)
            return cls.meta_data.columns

        app.run_server(debug=True, threaded=True, port=10450)


if __name__ == '__main__':
    TestDash.dash_app()