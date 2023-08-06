#!/share/nas2/genome/biosoft/Python//3.7.3/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/12/5 16:57
# @Author : jmzhang
# @Email : zhangjm@biomarker.com.cn

# !/share/nas2/genome/biosoft/Python//3.7.3/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/10/21 11:27
# @Author : jmzhang
# @Email : zhangjm@biomarker.com.cn
import time

from matplotlib.axes._axes import _log as matplotlib_axes_logger
import matplotlib.pyplot as plt
from matplotlib import image
import _pickle as cPickle
from pathlib import Path
import seaborn as sns
import anndata as ad
import pickle, gzip
import pandas as pd
import scanpy as sc
import numpy as np
import warnings
import argparse
import logging
import anndata
import json
import math
import re

import spatial_tools

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

matplotlib_axes_logger.setLevel('ERROR')
warnings.filterwarnings("ignore")

sc.set_figure_params(facecolor="white", figsize=(8, 8))
sc.settings.verbosity = 3


class SpatialApp:
    styles = {
        'pre': {
            'border': 'thin lightgrey solid',
            'overflowX': 'scroll'
        }
    }
    TOKEN = None

    _meta_data = None
    _spatial_tools_object = None
    _adata = None

    _feature_info = None
    _color_by_info = None

    _adata_container = {}

    @classmethod
    def color_by_dropdown(cls):
        from dash import dcc, html

        if cls._color_by_info is None:
            return [html.Label('Color by'),
                    dcc.Dropdown(id='color_by')]

        else:
            return [html.Label('Color by'),
                    dcc.Dropdown(cls._color_by_info, id='color_by')]

    @classmethod
    def density_by_dropdown(cls):
        from dash import dcc, html

        if cls._color_by_info is None:
            return [html.Label('density by'),
                    dcc.Dropdown(id='density_by')]

        else:
            return [html.Label('density by'),
                    dcc.Dropdown(cls._color_by_info, id='density_by')]

    @classmethod
    def feature_dropdown(cls):
        from dash import dcc, html

        if cls._feature_info is None:
            return [html.Label('Feature'),
                    dcc.Dropdown(id='feature')]
        else:
            return [html.Label('Feature'),
                    dcc.Dropdown(cls._feature_info, id='feature')]

    @classmethod
    def WHITEHOLE_store(cls):
        from dash import dcc

        if cls._spatial_tools_object is None:
            return dcc.Store(id='WHITEHOLE')
        else:
            return dcc.Store(data='from kwargs', id='WHITEHOLE')

    @staticmethod
    def return_text_replace_figure(text, size):
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": text,
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": size
                        }
                    }
                ]
            }
        }

    @staticmethod
    def layout_figure(figure):
        figure.update_layout(width=1000,
                             height=1000,
                             autosize=True,
                             margin=dict(l=5, r=5, t=5, b=5))

        return figure

    @classmethod
    def run_dash(cls, spatial_tools_obj=None, adata=None, port=30000, debug=False):
        from dash import Input, Output, dcc, html, exceptions, ctx, State
        import dash_loading_spinners as dls
        import plotly.express as px
        import dash_uploader as du
        import uuid
        # import dash_daq as daq
        import dash_bootstrap_components as dbc

        from jupyter_dash import JupyterDash

        app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        du.configure_upload(app, "./__cache__")
        cls.TOKEN = JupyterDash._token
        color_scales = px.colors.named_colorscales() + [i + '_r' for i in px.colors.named_colorscales()]

        def resolve_selected_data(selectedData):
            barcodes_list = [i['text'] if 'barcode' not in i['text'] else re.search('L[0-9]+_[0-9]+', i['text']).group()
                             for i in selectedData['points']]
            return barcodes_list

        if isinstance(spatial_tools_obj, spatial_tools.SpatialTools):
            cls._spatial_tools_object = spatial_tools_obj

        if isinstance(adata, pd.DataFrame):
            cls._adata = adata
            cls._meta_data = adata
            cls._feature_info = adata.columns
            cls._color_by_info = adata.columns

        elif isinstance(adata, anndata.AnnData):
            cls._adata = adata
            cls._meta_data = adata.obs
            cls._feature_info = adata.var.index
            cls._color_by_info = adata.obs.columns

        controls = html.Div(

            [
                dcc.Store(id='BLACKHOLE'),
                cls.WHITEHOLE_store(),
                dbc.Accordion([
                    dbc.AccordionItem([
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("Welcome to spatial tools vision", className="card-title"),
                                # html.H6("Card subtitle", className="card-subtitle"),
                                html.P("Analysis and visualization of data from the S1000 sequencing platform.\n"
                                       "If you have any suggestions please contact zhangjm@biomarker.com, \nthank you!",
                                       className="card-text", style={"width": "100%"}
                                       ),
                                dbc.CardLink("about us", href="http://www.biomarker.com.cn/about-us"),
                                dbc.CardLink("more tools", href="https://international.biocloud.net/zh/user/login"),
                                dbc.CardLink("developer", href="https://github.com/jmzhang1911"),
                            ], style={"width": "25rem"})
                        ])
                    ], title="about"),
                    dbc.AccordionItem([
                        dbc.Row([
                            dbc.Col([
                                du.Upload(
                                    id='upload_spatial_tools',
                                    text='SpatialTools-object\n(.len)',
                                    filetypes=['pickle', 'gz', 'pkl', 'len']
                                ),

                            ], md=5),
                            dbc.Col([
                                du.Upload(
                                    id='upload_adata',
                                    text='data\n(.h5ad, .loom, .xls, .csv)',
                                    max_files=20,
                                    filetypes=['csv', 'h5ad', 'loom', 'xls'],

                                ),

                            ], md=7)
                        ], align='center'),
                        dbc.Row([
                            dbc.Col([
                                html.Div(id='callback-output'),
                            ]),
                            dbc.Col([
                                html.Div(id='callback-output2')
                            ])
                        ]
                        )
                    ], title="Upload object"),
                    dbc.AccordionItem([
                        dbc.Row([
                            html.Div([
                                html.Label('Select data'),
                                dcc.Dropdown(
                                    id='selected_adata')
                            ], style={'display': 'inline-block',
                                      'width': '95%'}),
                        ]),

                        html.Br(),

                        dbc.Row([

                            html.Div([
                                html.Label('set He'),
                                dcc.Dropdown(
                                    ['low He', 'no He', 'hire He', 'only He'],
                                    'low He',
                                    id='pic_data')
                            ], style={'display': 'inline-block',
                                      'width': '30%',
                                      "margin-left": "2px"}),

                            html.Div([
                                html.Label('Point size'),
                                dbc.Input(
                                    id='point_size',
                                    type="number",
                                    placeholder="point size",
                                    min=0.000001,
                                    value=1
                                )
                            ], style={'display': 'inline-block',
                                      'width': '30%'}),

                            html.Div([
                                dcc.Slider(
                                    min=0,
                                    max=1,
                                    value=1,
                                    id='alpha',
                                    marks={0: {'label': 'min', 'style': {'color': '#77b0b1'}},
                                           0.5: {'label': 'point alpha'},
                                           1: {'label': 'max', 'style': {'color': '#f50'}}},
                                    tooltip={"placement": "top", "always_visible": True})
                            ], style={'display': 'inline-block',
                                      'width': '30%', })

                        ], align='center')

                    ], title='Basic setting'),
                    dbc.AccordionItem([
                        html.Div(cls.color_by_dropdown(),
                                 style={'display': 'inline-block',
                                        'width': '32%',
                                        "margin-left": "0px"}),
                        html.Div([
                            html.Label('Multi-Select groups'),
                            dcc.Dropdown(id='groups',
                                         multi=True)
                        ], style={'display': 'inline-block',
                                  'width': '60%',
                                  "margin-left": "18px"})
                    ], title='Discrete variables'),
                    dbc.AccordionItem([
                        html.Div(cls.feature_dropdown(),
                                 style={'display': 'inline-block',
                                        'width': '40%'}),
                        html.Div([html.Label("Feature color Scale"),
                                  dcc.Dropdown(
                                      id='cmap',
                                      options=color_scales,
                                      value='viridis'
                                  )],
                                 style={'display': 'inline-block',
                                        'width': '40%',
                                        "margin-left": "18px"})
                    ], title='Continuous variables'),
                    dbc.AccordionItem([
                        html.Div(cls.density_by_dropdown(),
                                 style={'display': 'inline-block',
                                        'width': '50%'}),

                        dcc.Graph(id='gene_number_density',
                                  style={'width': '40vh',
                                         'height': '25vh',
                                         "margin-left": "0px"})
                    ], title='Density plotting'),
                    dbc.AccordionItem([
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(id="x1", type="number", placeholder="x1", debounce=True, style={'width': 85},
                                          min=1, max=9999),
                            ], md=2),
                            dbc.Col([
                                dbc.Input(id="x2", type="number", placeholder="x2", debounce=True, style={'width': 85},
                                          min=1, max=9999)
                            ], md=2, style={'margin-left': '15px'}),
                            dbc.Col([
                                dbc.Input(id="y1", type="number", placeholder="y1", debounce=True, style={'width': 85},
                                          min=1, max=9999)
                            ], md=2, style={'margin-left': '15px'}),
                            dbc.Col([
                                dbc.Input(id="y2", type="number", placeholder="y2", debounce=True, style={'width': 85},
                                          min=1, max=9999),
                            ], md=2, style={'margin-left': '15px'}),
                        ])
                    ], title='Cropping coord'),
                    dbc.AccordionItem([
                        dbc.Tabs([
                            dbc.Tab(dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Button("Download selected", id="selected_barcodes", className="me-1"),
                                        dcc.Download(id="download-text-index"),
                                        html.Br(),
                                        html.Br(),
                                        html.Div(id='selected-data',
                                                 style=cls.styles['pre'],
                                                 children='Please using lasso or box select ...')
                                    ]
                                ),
                                className="mt-3",
                            ), label="get barcodes"),

                            dbc.Tab(dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    html.Label('cluster labels'),
                                                    dbc.Input(id='cluster-labels',
                                                              type="text",
                                                              placeholder="cluster lable",
                                                              value='cluster')
                                                ], style={'display': 'inline-block',
                                                          'width': '90%'})
                                            ], width="auto"),

                                            dbc.Col([
                                                html.Label('cluster-method'),
                                                dcc.Dropdown(['leiden', 'louvain'], 'leiden', id='cluster-method')
                                            ],
                                                style={'display': 'inline-block',
                                                       # 'margin-left': '1px',
                                                       'width': '30%'}, width="auto"),
                                        ], className="g-0"),

                                        html.Br(),

                                        dbc.Row([
                                            html.Div([
                                                html.Label('n_neighbors'),
                                                dbc.Input(id='n_neighbors',
                                                          type="number",
                                                          placeholder="point size",
                                                          min=2,
                                                          max=100,
                                                          value=15)
                                            ], style={'display': 'inline-block',
                                                      'width': '30%'}),

                                            html.Div([
                                                html.Label('resolution'),
                                                dbc.Input(id='resolution',
                                                          type="number",
                                                          placeholder="resolution",
                                                          min=0.001,
                                                          max=5,
                                                          value=0.5)

                                            ], style={'display': 'inline-block',
                                                      'width': '30%'})
                                        ], style={'no_gutters': True}),

                                        html.Br(),

                                        dbc.Row([

                                            html.Div([
                                                html.Label('highly-variable genes'),
                                                dbc.Input(id='n_top_genes',
                                                          type="number",
                                                          placeholder="point size",
                                                          min=1,
                                                          value=2000)
                                            ], style={'display': 'inline-block',
                                                      'width': '50%'}),

                                            html.Div([
                                                html.Label('n_PCAs'),
                                                dbc.Input(id='n_PCAs',
                                                          type="number",
                                                          placeholder="n_PCAs",
                                                          min=15,
                                                          value=50)

                                            ], style={'display': 'inline-block',
                                                      'width': '25%'})

                                        ]),

                                        html.Br(),

                                        dbc.Button("re-clustering",
                                                   id="Re-cluster",
                                                   className="me-1",
                                                   color='success',
                                                   external_link=True,
                                                   style={'width': 120}
                                                   ),

                                        dcc.Download(id='down-load-re-clustered-h5ad'),

                                        html.Br(),

                                        dcc.Loading(
                                            children=[html.Div([html.Div(id="loading-clustering")])],
                                            type="circle",
                                            # fullscreen=True,
                                        ),

                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),

                                    ]
                                ),
                                className="mt-3",
                            ), label="re-clustering")
                        ]),

                        html.Br(),
                        dbc.Row([

                        ])
                    ], title='Selected barcodes'),
                    dbc.AccordionItem([
                        dbc.Tabs([
                            dbc.Tab(dbc.Card(
                                dbc.CardBody([
                                    dcc.Store(id='mtx_dir_path'),
                                    du.Upload(
                                        id='make_h5ad_file',
                                        text='upload barcodes.tsv.gz, features.tsv.gz and matrix.mtx.gz',
                                        filetypes=['gz'],
                                        max_files=3
                                    ),

                                    html.Br(),

                                    html.Div([
                                        html.Label('sample name'),
                                        dbc.Input(id='sample_name',
                                                  required=True,
                                                  value='sample',
                                                  type="text",
                                                  placeholder="sample name")
                                    ], style={'display': 'inline-block',
                                              'width': '90%'}),

                                    html.Br(),
                                    html.Br(),

                                    dbc.Button("making .h5ad",
                                               id="run_make_h5ad",
                                               className="me-1",
                                               color='success',
                                               external_link=True,
                                               style={'width': 120}
                                               ),
                                    dcc.Download(id='download-h5ad'),
                                    dcc.Loading(
                                        children=[html.Div([html.Div(id="making h5ad")])],
                                        type="circle",
                                    ),

                                    html.Br(),
                                    html.Br(),
                                    html.Br()

                                ]), className="mt-3"
                            ), label="make .h5ad"),

                            dbc.Tab(dbc.Card(
                                dbc.CardBody([
                                    dcc.Store(id='upload_tiff_file'),
                                    dcc.Store(id='upload_png_file'),
                                    dcc.Store(id='upload_pos_files'),

                                    dbc.Row([
                                        html.Div([
                                            du.Upload(
                                                id='tiff_file',
                                                text='upload he_roi.tif',
                                                filetypes=['tiff', 'tif'],
                                                max_files=1,
                                            )
                                        ], style={'width': 150}),

                                        html.Div([
                                            du.Upload(
                                                id='png_file',
                                                text='upload he_roi_small.png',
                                                filetypes=['png'],
                                                max_files=1
                                            )
                                        ], style={'width': 150}),

                                        html.Div([
                                            du.Upload(
                                                id='pos_files',
                                                text='upload barcodes_pos.tsv.gz',
                                                filetypes=['gz', 'tsv'],
                                                max_files=10
                                            )
                                        ], style={'width': 150})
                                    ]),

                                    html.Br(),
                                    html.Br(),

                                    dbc.Button("making .len",
                                               id="run_make_len",
                                               className="me-1",
                                               color='success',
                                               external_link=True,
                                               style={'width': 120}
                                               ),
                                    dcc.Download(id='download-len'),
                                    dcc.Loading(
                                        children=[html.Div([html.Div(id="making-len")])],
                                        type="circle",
                                    ),

                                    html.Br(),
                                    html.Br(),
                                    html.Br()

                                ], className="mt-3")
                            ), label='make .len'),

                            dbc.Tab(dbc.Card(
                                dbc.CardBody([

                                    dbc.Row([
                                        html.Label("choice .h5ad"),
                                        dcc.Dropdown(
                                            id='choice-h5ad',
                                        )
                                    ]),
                                    html.Br(),
                                    dbc.Row([
                                        html.Label("choice .xls"),
                                        dcc.Dropdown(
                                            id='choice-others'
                                        )
                                    ]),
                                    html.Br(),
                                    dbc.Button("merge",
                                               id="run_merge",
                                               className="me-1",
                                               color='success',
                                               external_link=True,
                                               style={'width': 120}
                                               ),
                                    dcc.Download(id='download-merge'),
                                    dcc.Loading(
                                        children=[html.Div([html.Div(id="making merge")])],
                                        type="circle",
                                    ),

                                    html.Br(),
                                    html.Br(),
                                    html.Br()

                                ], className="mt-3"),
                            ), label="merge data")
                        ]),

                    ], title='Small tools')
                ], always_open=True),

            ],
            # body=True, style={"padding": "10px", "font_color": "white", 'bg_color': '#85002D'}
        )

        app.layout = dbc.Container(
            [
                dbc.Navbar([
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                                dbc.Col(dbc.NavbarBrand("SpatialTools v2.1.1"),
                                        style={"margin-left": "20px", 'fontsize': '10px'}),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="https://plotly.com",
                        style={"textDecoration": "none"},
                    )
                ], color="dark", dark=True, style={'height': '60px'}),

                # html.H1("Spatial Tools For Vision beta v0.1.5", style={'textAlign': 'center', 'color': '#20B2AA'}),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(controls,
                                md=3,
                                # style={'height': '80vh'}
                                ),
                        dbc.Col([
                            dcc.Loading([

                                dcc.Graph(id="cluster-graph")], style={'width': 100})
                            # html.Div([
                            #     dcc.Loading(
                            #         children=[html.Div([html.Div(id="holding")])],
                            #         type="circle",
                            #     )
                            # ]
                            # )
                            # dls.Hash(dcc.Graph(id="cluster-graph",
                            #                    # style={'width': '65vh', 'height': '65vh'}
                            #                    ),
                            #
                            #         # x='',
                            #          color="#E50B0B",
                            #          speed_multiplier=2,
                            #          size=100)

                        ]

                            , md=6)
                    ],
                    align="center",
                ),
            ],
            fluid=True,
        )

        @du.callback(
            Output('BLACKHOLE', 'data'),
            id='upload_adata',
        )
        def upload_adata(status: du.UploadStatus):
            logging.info('upload adata {} done'.format(str(status.latest_file)))
            return [str(_) for _ in status.uploaded_files]

        @du.callback(
            [Output('WHITEHOLE', 'data'),
             Output('callback-output', 'children')],
            id='upload_spatial_tools'
        )
        def upload_spatial_tools_obj(status: du.UploadStatus):
            logging.info('upload  spatial_tools.SpatialTools {} done'.format(str(status.latest_file)))
            cls._spatial_tools_object = SpatialTools.load_from(str(status.latest_file))
            level_info = 'levels: ' + ', '.join(list(cls._spatial_tools_object.container.keys()))

            return str(status.latest_file), level_info

        @app.callback(
            [Output('selected_adata', 'options'),
             Output('callback-output2', 'children')],
            Input('BLACKHOLE', 'data')
        )
        def list_adata(adata_list):
            if not adata_list:
                cls._adata_container = {}
                raise exceptions.PreventUpdate

            for file in adata_list:
                if Path(file).suffix in ['.xls', '.csv']:
                    _adata = pd.read_csv(str(file), sep='\t')

                    logging.info('reading upload data as Pandas')
                else:
                    if Path(file).suffix == '.loom':
                        _adata = sc.read_loom(file)
                    else:
                        _adata = ad.read_h5ad(file)

                cls._adata_container[Path(file).name] = _adata

            for_options = list(cls._adata_container.keys())

            return for_options, 'uploaded: {} files'.format(len(for_options))

        @app.callback(
            [Output('color_by', 'options'),
             Output('density_by', 'options'),
             Output('feature', 'options')],
            Input('selected_adata', 'value')
        )
        def get_adata(selected_adata):

            if not selected_adata:
                raise exceptions.PreventUpdate

            _adata = cls._adata_container[selected_adata]

            if isinstance(_adata, pd.DataFrame):
                cls._adata = _adata
                cls._meta_data = _adata
                cls._feature_info = _adata.columns
                cls._color_by_info = _adata.columns
                logging.info('reading upload data as Pandas')

            else:

                cls._adata = _adata
                cls._meta_data = _adata.obs
                cls._feature_info = _adata.var.index
                cls._color_by_info = _adata.obs.columns
                logging.info('reading upload data as anndata')

            return cls._color_by_info, cls._color_by_info, cls._feature_info

        @app.callback(
            Output('download-text-index', 'data'),
            [
                Input('selected_barcodes', 'n_clicks'),
                Input('cluster-graph', 'selectedData')
            ],
            prevent_initial_call=True,
        )
        def download_barcodes(n_clicks, selectedData):
            logging.info('--> in download_barcodes')

            if n_clicks is None:
                logging.info('--> in download_barcodes1')
                raise exceptions.PreventUpdate

            elif ctx.triggered_id == 'selected_barcodes' and selectedData:
                logging.info('--> in download_barcodes2')
                info = json.dumps(resolve_selected_data(selectedData))
                return dict(content=info, filename="selected_barcodes.json")

            else:
                logging.info('--> in download_barcodes3')
                raise exceptions.PreventUpdate

        @app.callback(
            [Output('down-load-re-clustered-h5ad', 'data'),
             Output('loading-clustering', 'children')
             ],
            [Input('Re-cluster', 'n_clicks'),
             Input('cluster-graph', 'selectedData'),
             Input('cluster-labels', 'value'),
             Input('cluster-method', 'value'),
             Input('n_PCAs', 'value'),
             Input('resolution', 'value'),
             Input('n_top_genes', 'value'),
             Input('n_neighbors', 'value')
             ],
            prevent_initial_call=True,

        )
        def re_cluster(n_clicks,
                       selectedData,
                       cluster_labels, method, n_PCAs, resolution, n_top_genes, n_neighbors):
            output_data = '__cache__/results.h5ad'
            SpatialTools.check_dir_exists(output_data)

            if n_clicks is None:
                logging.info('---- >  tmp 1')
                raise exceptions.PreventUpdate

            if not cluster_labels and not method and not n_PCAs and \
                    not resolution and not n_top_genes and not n_neighbors:

                raise exceptions.PreventUpdate

            elif ctx.triggered_id == 'Re-cluster' and selectedData and isinstance(cls._adata, anndata.AnnData):
                logging.info('doing re-clustered')

                # TODO re-clustered
                with open(output_data, 'w') as f:
                    f.write('hello dash!\n')

                # sc.pp.normalize_total(adata, inplace=True)
                # sc.pp.log1p(adata)
                # sc.pp.highly_variable_genes(adata, flavor="seurat", n_top_genes=2000)
                # sc.pp.pca(adata, n_comps)

                seleceted_barcodes = resolve_selected_data(selectedData)
                _adata = cls._adata[seleceted_barcodes, :].copy()

                sc.pp.normalize_total(_adata, inplace=True)
                sc.pp.log1p(_adata)
                sc.pp.highly_variable_genes(_adata, flavor="seurat", n_top_genes=n_top_genes)
                sc.pp.pca(_adata, n_comps=n_PCAs)
                sc.pp.neighbors(_adata, n_neighbors=n_neighbors)

                if method == 'leiden':
                    sc.tl.leiden(_adata, key_added=cluster_labels, resolution=resolution)

                else:
                    sc.tl.louvain(_adata, key_added=cluster_labels, resolution=resolution)

                _adata.write_h5ad(output_data)

                return dcc.send_file(output_data), None

            else:
                raise exceptions.PreventUpdate

        @du.callback(
            Output('mtx_dir_path', 'data'),
            id='make_h5ad_file',
        )
        def h5ad_upload_file_path(status: du.UploadStatus):
            return str(Path([str(_) for _ in status.uploaded_files][0]).parent)

        @app.callback(
            [Output('download-h5ad', 'data'),
             Output('making h5ad', 'children')],
            [Input('mtx_dir_path', 'data'),
             Input('run_make_h5ad', 'n_clicks'),
             Input('sample_name', 'value')]
        )
        def make_h5ad(mtx_dir_path, n_clicks, sample_name):
            if n_clicks is None:
                raise exceptions.PreventUpdate

            if ctx.triggered_id == 'run_make_h5ad' and mtx_dir_path is not None:
                logging.info('making h5ad ...')
                output_data = '__cache__/results.h5ad'
                SpatialTools.check_dir_exists(output_data)

                _adata = sc.read_10x_mtx(path=mtx_dir_path, cache=False)
                _adata.var_names_make_unique()

                _adata.obs['sample'] = sample_name

                sc.pp.filter_cells(_adata, min_genes=0)
                sc.pp.filter_cells(_adata, min_counts=0)

                _adata.write(output_data)

                return dcc.send_file(output_data), None

            else:
                raise exceptions.PreventUpdate

        @du.callback(
            Output('upload_tiff_file', 'data'),
            id='tiff_file',
        )
        def upload_tiff(status: du.UploadStatus):
            return str(status.latest_file)

        @du.callback(
            Output('upload_png_file', 'data'),
            id='png_file',
        )
        def upload_png(status: du.UploadStatus):
            return str(status.latest_file)

        @du.callback(
            Output('upload_pos_files', 'data'),
            id='pos_files',
        )
        def uplaod_pos(status: du.UploadStatus):
            logging.info('++++++ {}'.format(status.uploaded_files))
            return [str(_) for _ in status.uploaded_files]

        @app.callback(
            [Output('download-len', 'data'),
             Output('making-len', 'children')],
            [Input('run_make_len', 'n_clicks'),
             Input('upload_tiff_file', 'data'),
             Input('upload_png_file', 'data'),
             Input('upload_pos_files', 'data')],
        )
        def making_len(n_clicks, upload_tiff_file, upload_png_file, upload_pos_files):

            if n_clicks is None:
                raise exceptions.PreventUpdate

            if ctx.triggered_id == 'run_make_len' and upload_tiff_file is not None and \
                    upload_png_file is not None and upload_pos_files is not None:
                logging.info('making len file .... ')
                logging.info(upload_tiff_file)
                logging.info(upload_png_file)
                logging.info(upload_pos_files)

                output_data = '__cache__/results'

                len_file = SpatialTools(pic=upload_tiff_file,
                                        low_pic=upload_png_file,
                                        barcodes_pos=upload_pos_files)

                len_file.save_to(output_data)

                logging.info('done making len file .... ')
                logging.info(str(output_data + '.len'))
                return dcc.send_file(output_data + '.len'), None
            else:
                raise exceptions.PreventUpdate

        @app.callback(
            [Output('choice-h5ad', 'options'),
             Output('choice-others', 'options')],
            Input('BLACKHOLE', 'data')
        )
        def for_choice_h5ad(BLACKHOLE):
            time.sleep(3)
            if BLACKHOLE is not None:
                logging.info(cls._adata_container.keys())
                for_h5ad = [_ for _ in cls._adata_container.keys() if str(_).endswith('.h5ad')]
                for_others = [_ for _ in cls._adata_container.keys() if not str(_).endswith('.h5ad')]

                return for_h5ad, for_others

            else:
                raise exceptions.PreventUpdate

        @app.callback(
            [Output('download-merge', 'data'),
             Output('making merge', 'children')],
            [Input('choice-h5ad', 'value'),
             Input('choice-others', 'value'),
             Input('run_merge', 'n_clicks')]
        )
        def merge_data(h5ad_data, other_data, n_clicks):
            if n_clicks is None:
                raise exceptions.PreventUpdate

            elif ctx.triggered_id == 'run_merge' and h5ad_data is not None and other_data is not None:
                logging.info('doing merge data ....')

                output_data = '__cache__/merged_data.h5ad'
                SpatialTools.check_dir_exists(output_data)

                _h5ad_data = cls._adata_container[h5ad_data].copy()
                _other_data = cls._adata_container[other_data].copy()

                if 'barcode' not in _other_data.columns:
                    _other_data['barcode'] = _other_data.index

                if 'barcode' not in _h5ad_data.obs.columns:
                    _h5ad_data.obs['barcode'] = _h5ad_data.obs.index

                logging.info('----> doing merging')
                logging.info(_h5ad_data.obs)
                logging.info(_other_data)
                tmp_obs = _h5ad_data.obs.merge(_other_data, how='left', on='barcode')
                tmp_obs = tmp_obs.set_index('barcode')
                tmp_obs.index.name = None
                _h5ad_data.obs = tmp_obs

                logging.info('----> saving ')

                _h5ad_data.write_h5ad(output_data)

                return dcc.send_file(output_data), None

            else:
                raise exceptions.PreventUpdate

        @app.callback(
            Output('groups', 'options'),
            Input('color_by', 'value')
        )
        def set_groups_value(color_by):
            if cls._meta_data is None or color_by is None:
                raise exceptions.PreventUpdate
            return [str(_) for _ in cls._meta_data[color_by].unique()]

        @app.callback(
            Output('selected-data', 'children'),
            Input('cluster-graph', 'selectedData'))
        def display_selected_data(selectedData):
            if selectedData:
                return json.dumps(resolve_selected_data(selectedData))
            else:
                return json.dumps('Please using lasso or box select ...')

        @app.callback(
            Output('gene_number_density', 'figure'),
            Input('density_by', 'value'),
            Input("color_by", 'value'),
            Input('groups', 'value'),
            Input('cluster-graph', 'selectedData')

        )
        def make_density(density_by, color_by, groups, selectedData):
            # logging.info('density_by: {}'.format(density_by))
            # logging.info('color_by: {}'.format(color_by))
            # logging.info('groups: {}'.format(groups))
            # logging.info('selectedData: {}'.format(selectedData))

            try:
                df = cls._meta_data
                if groups:
                    df = cls._meta_data.query('{} in {}'.format(color_by, groups))

                if selectedData and selectedData['points']:
                    df = cls._meta_data.filter(items=resolve_selected_data(selectedData), axis=0)

                fig = px.histogram(df[density_by])
                fig.update_layout(
                    xaxis_title=None,
                    yaxis_title=None,
                )

                return fig

            except:

                return cls.return_text_replace_figure(text='Please select density value', size=20)

        @app.callback(
            Output("cluster-graph", "figure"),
            [
                Input('selected_adata', 'value'),
                Input('WHITEHOLE', 'data'),
                Input('BLACKHOLE', 'data'),
                Input("color_by", 'value'),
                Input('alpha', 'value'),
                Input('feature', 'value'),
                Input("pic_data", "value"),
                Input('cmap', 'value'),
                Input("point_size", "value"),
                Input('groups', 'value'),
                Input('x1', 'value'),
                Input('x2', 'value'),
                Input('y1', 'value'),
                Input('y2', 'value'),
            ],
        )
        def make_graph(selected_adata, WHITEHOLE, BLACKHOLE, color_by,
                       alpha, feature, pic_data,
                       cmap, point_size, groups,
                       x1, x2, y1, y2):
            logging.info('----> ')
            logging.info('plotting =={}'.format(WHITEHOLE))
            logging.info('plotting =={}'.format(BLACKHOLE))

            if pic_data == 'no He':
                draw_pic = False
                low_pic = False
            else:
                draw_pic = True

                if pic_data == 'low He':
                    low_pic = True
                else:
                    low_pic = False

            if pic_data == 'only He':
                pic_only = True
                low_pic = False
            else:
                pic_only = False

            if (x1 and x2 and y1 and y2) and WHITEHOLE is not None:
                logging.info('1')
                x1, x2, y1, y2 = math.ceil(x1), math.ceil(x2), math.ceil(y1), math.ceil(y2)
                crop_coord = [y1, y2, x1, x2]

                return_low_pic = cls._spatial_tools_object.__dict__['_low_pic'][y1:y2, x1:x2, :]
                return_hire_pic = cls._spatial_tools_object.__dict__['_pic'][y1:y2, x1:x2, :]
            else:
                if WHITEHOLE is not None:
                    logging.info('2')
                    return_low_pic = cls._spatial_tools_object.__dict__['_low_pic']
                    return_hire_pic = cls._spatial_tools_object.__dict__['_pic']
                    crop_coord = False
                else:
                    return cls.return_text_replace_figure(text='Please upload a SpatialTools object', size=25)

            logging.info('color_by={}'.format(color_by))
            logging.info('feature={}'.format(feature))
            logging.info('WHITEHOLE={}'.format(WHITEHOLE))
            if (str(color_by) == 'None' and str(feature) == 'None') or WHITEHOLE is None:
                logging.info('4')
                if pic_data == 'hire He':

                    return cls.layout_figure(px.imshow(return_hire_pic,
                                                       binary_string=True,
                                                       binary_compression_level=5))
                else:

                    return cls.layout_figure(px.imshow(return_low_pic,
                                                       binary_string=True,
                                                       binary_compression_level=5))

            if str(feature) == 'None':
                feature = False

            logging.info('plotting')

            try:
                if point_size is None:
                    raise exceptions.PreventUpdate

                pic = cls._spatial_tools_object.s1000_spatial_plot(adata=cls._adata,
                                                                   color=color_by,
                                                                   feature=feature,
                                                                   size=float(point_size),
                                                                   cmap=cmap,
                                                                   groups=list(groups) if groups else groups,
                                                                   crop_coord=crop_coord,
                                                                   draw_pic=draw_pic,
                                                                   low_pic=low_pic,
                                                                   pic_only=pic_only,
                                                                   alpha=alpha,
                                                                   interactive=True)

                logging.info('end')
                pic.update_layout(uirevision=True)

                return pic

            except:

                return cls.return_text_replace_figure(text='Please chose right parameter', size=25)

        logging.info('listen: http://127.0.0.1:{}/'.format(port))
        app.run_server(debug=debug, mode='external', port=port, host='127.0.0.1')

    @classmethod
    def terminate_server_for_port(cls):
        import requests

        shutdown_url = "http://{host}:{port}/_shutdown_{token}".format(
            host='127.0.0.1', port='30000', token=cls.TOKEN
        )
        try:
            response = requests.get(shutdown_url)
        except Exception as e:
            pass

    @staticmethod
    def plotly_plot_save(to_save, fig):
        import plotly

        if not Path(to_save).parent.exists():
            Path(to_save).parent.mkdir(exist_ok=True, parents=True)

        plotly.offline.plot(fig, filename=to_save + '.html')

    @classmethod
    def interact_pic_discrete(cls,
                              plot_data_grouped,
                              pic,
                              color,
                              alpha,
                              size,
                              color_dict,
                              to_save,
                              figsize=(8, 8),
                              draw_pic=True,
                              pic_only=False):

        import plotly.graph_objects as go
        import plotly.express as px

        if pic_only:
            return px.imshow(pic, binary_string=True, binary_compression_level=5)

        if draw_pic:
            fig = px.imshow(pic, binary_string=True, binary_compression_level=5)
        else:
            fig = go.Figure()

        if len(color_dict) > 100:
            raise 'too much value'

        for key, group in plot_data_grouped:
            fig.add_trace(
                go.Scattergl(x=group['__x'],
                             y=group['__y'],
                             mode='markers',
                             opacity=alpha,
                             marker=dict(color=group[plot_data_grouped.keys].map(color_dict),
                                         size=size),
                             text=group['barcode'],
                             name=key
                             ))

        fig.update_layout(
            legend=dict(yanchor="top",
                        itemsizing='constant',
                        font=dict(
                            size=14,
                            color="black"
                        ),
                        y=0.8),
            title={
                'text': 'color by : {}'.format(color),
                'x': 0.45,
                'xanchor': 'center',
                'yanchor': 'top'},
            activeshape_opacity=0.9,
            width=float(figsize[0]) * 125,
            height=float(figsize[1]) * 125,
            margin=dict(l=5, r=5, t=5, b=5),
        )

        if not draw_pic:
            fig['layout']['yaxis']['autorange'] = "reversed"

        if to_save:
            cls.plotly_plot_save(to_save=to_save, fig=fig)

        return fig

    @classmethod
    def interact_pic_continuous(cls,
                                plot_data,
                                pic,
                                alpha,
                                feature,
                                size,
                                to_save,
                                cmap,
                                figsize=(8, 8),
                                draw_pic=True,
                                pic_only=False):

        import plotly.graph_objects as go
        import plotly.express as px

        if pic_only:
            return px.imshow(pic, binary_string=True, binary_compression_level=5)

        if draw_pic:
            fig = px.imshow(pic, binary_string=True, binary_compression_level=5)
        else:
            fig = go.Figure()

        info_list = list(zip(plot_data['barcode'], plot_data[feature]))

        fig.add_trace(
            go.Scattergl(x=plot_data['__x'],
                         y=plot_data['__y'],
                         mode='markers',
                         opacity=alpha,
                         marker=dict(size=size,
                                     color=plot_data[feature],
                                     colorscale=cmap,
                                     showscale=True),
                         text=['barcode:{} \n value:{}'.format(str(i[0]), str(i[1])) for i in info_list]  # ,
                         )
        )

        fig.update_layout(
            title={
                'text': 'feature: {}'.format(feature),
                # 'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},

            autosize=True,
            width=float(figsize[0]) * 125,
            height=float(figsize[1]) * 125,
            margin=dict(l=5, r=5, t=5, b=5)
        )

        if not draw_pic:
            fig['layout']['yaxis']['autorange'] = "reversed"

        if to_save:
            cls.plotly_plot_save(to_save=to_save, fig=fig)

        return fig


class SpatialTools:

    def __init__(self, pic, barcodes_pos, low_pic=None):
        self._pic = image.imread(pic)

        if low_pic:
            self._low_pic = image.imread(low_pic)
            self._low_contain = True
            self.low_scalar = self._cal_zoom_rate(self._low_pic.shape[0], self._low_pic.shape[1])
        else:
            self._low_pic = None
            self._low_contain = False

        self.container = self._make_container(barcodes_pos)
        self.scalar = self._cal_zoom_rate(self._pic.shape[0], self._pic.shape[1])

        self._adata_type = None
        self._facet_pos_list = None

    def __str__(self):
        info = 'low pic: {}\nlevel: {}\nscalar: {}'. \
            format('True' if self._low_contain else 'False',
                   list(self.container.keys()), self.scalar)
        return info

    def _make_container(self, barcodes_pos):
        """{"level2": {obsm: "", point_size: ""}, "level3":{obsm: "", point_size: ""}}"""
        container_dict = {}

        if not isinstance(barcodes_pos, list):
            barcodes_pos = [barcodes_pos]

        for i in barcodes_pos:
            obsm = pd.read_csv(i, '\t', names=['barcode', '__x', '__y'])
            point_size = self._auto_cal_radius(obsm)
            level = str(obsm['barcode'][0]).split('_')[0]
            container_dict[level] = {'obsm': obsm, 'point_size': point_size}

        return container_dict

    @staticmethod
    def _get_adata_level(input_adata):
        return str(input_adata['barcode'][0]).split('_')[0]

    @property
    def pic(self):
        return plt.imshow(self._pic)

    @property
    def low_pic(self):
        if not self._low_contain:
            raise ValueError('no low pic in SpatialTools')
        else:
            return plt.imshow(self._low_pic)

    @staticmethod
    def check_dir_exists(filename):
        if not Path(filename).parent.exists():
            Path(filename).parent.mkdir(exist_ok=True, parents=True)

    def save_to(self, filename='S1000'):
        self.check_dir_exists(filename)
        with gzip.open(filename + '.len', 'wb') as f:
            cPickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_from(filename):
        with gzip.open(filename, 'rb') as f:
            data = cPickle.load(f)

        return data

    @staticmethod
    def _cal_zoom_rate(width, height):
        """from litt@biomarker.com.cn SpatialCluster_split"""
        std_width = 1000
        std_height = std_width / (46 * 31) * (46 * 36 * np.sqrt(3) / 2.0)
        if std_width / std_height > width / height:
            scale = width / std_width
        else:
            scale = height / std_height
        return scale

    @staticmethod
    def _auto_cal_radius(cluster_pos_df):
        """from litt@biomarker.com.cn SpatialCluster_split"""
        radius = 999999
        pref_pos = [0, 0]
        for index, item in cluster_pos_df.iterrows():
            if index != 0:
                curr_pos = [item['__y'], item['__x']]
                center_dist = np.sqrt((curr_pos[0] - pref_pos[0]) ** 2 + (curr_pos[1] - pref_pos[1]) ** 2)
                if center_dist < radius:
                    radius = center_dist
            pref_pos = [item['__y'], item['__x']]
            if index > 1000:
                break
        radius = round(radius * 0.618 / 2)
        if radius < 1:
            radius = 1

        return radius

    def _plot_save(self, fig: plt, to_save, dpi):
        self.check_dir_exists(to_save)

        fig.savefig('{}.png'.format(to_save), bbox_inches='tight', dpi=dpi)
        fig.savefig('{}.pdf'.format(to_save), bbox_inches='tight')

    @staticmethod
    def resolve_para_to_list_tuple_dict(input_str, instance_type, element_type=None):
        if instance_type == dict:
            res = {str(_[0]).strip(): str(_[1]).strip() for _ in
                   [i.split(':') for i in input_str.replace('{', '').replace('}', '').split(',')]}

        else:
            res = instance_type(
                [element_type(i.strip()) for i in input_str.replace(')', '').replace('(', '').split(',')])

        return res

    @staticmethod
    def _lighten_color(color, amount=0.5):
        """
        Lightens the given color by multiplying (1-luminosity) by the given amount.
        Input can be matplotlib color string, hex string, or RGB tuple.
        Examples:
        >> lighten_color('g', 0.3)
        >> lighten_color('#F034A3', 0.6)
        >> lighten_color((.3,.55,.1), 0.5)
        """
        import matplotlib.colors as mc
        import colorsys
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

    def _facet_pos(self, length, ncol):
        nrow = math.ceil(length / ncol)
        facet_pos_list = []
        for i in range(nrow):
            for x in range(ncol):
                facet_pos_list.append((i, x))

        self._facet_pos_list = facet_pos_list

        return nrow, ncol

    @staticmethod
    def _change_para_dict(origin: dict, changed: dict):
        for k, v in changed.items():
            if k not in origin.keys():
                raise ValueError('wrong para_dict key value : {}'.format(k))

            origin[k] = v

        return origin

    def _discrete_scatter_plot(self, ax, para_dict: dict, color_dict):
        plot_para_dict = {'title': '', 'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                          'legend_scale': 1.2, 'legend_ncol': math.ceil(len(color_dict) / 17),
                          'show_ticks_and_labels': True}

        if para_dict:
            plot_para_dict = self._change_para_dict(plot_para_dict, para_dict)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.99, box.height * 0.99])

        ax.legend(
            loc='center left',
            markerscale=float(plot_para_dict['legend_scale']),
            bbox_to_anchor=(1, 0.5), ncol=int(plot_para_dict['legend_ncol']),
            fontsize=16, frameon=False, handletextpad=0.3)

        plt.title(plot_para_dict['title'])
        plt.xlabel(plot_para_dict['xlabel'])
        plt.ylabel(plot_para_dict['ylabel'])

        if not plot_para_dict['show_ticks_and_labels'] or plot_para_dict['show_ticks_and_labels'] == 'False':
            plt.xticks([])
            plt.yticks([])
            ax.xaxis.set_ticklabels([])
            ax.yaxis.set_ticklabels([])

    def _continuous_scatter_plot(self):
        pass

    def _crop_coord(self, plot_data, crop_coord: list, low_pic=False):
        x1, x2, y1, y2 = [int(_) for _ in crop_coord]
        pic = self._low_pic if low_pic else self._pic
        pic = pic[x1:x2, y1:y2, :]

        plot_data = plot_data.query('{} <= __x <= {} & {} <= __y <= {}'.format(y1, y2, x1, x2))
        plot_data2 = plot_data.copy()

        plot_data2['__y'] = plot_data2['__y'] - x1
        plot_data2['__x'] = plot_data2['__x'] - y1

        return pic, plot_data2

    def s1000_spatial_plot(self, adata: anndata,
                           color='seurat_clusters',
                           groups=None,
                           size=1,
                           alpha=1,
                           alpha_map_to_value=False,
                           cmap='viridis',
                           value_limits=None,
                           figsize=(10, 10),
                           crop_coord=None,
                           to_save=None,
                           darken=None,
                           return_fig=False,
                           return_table=False,
                           feature=None,
                           split=False,
                           ncol=2,
                           color_dict: dict = None,
                           hspace=None,
                           dpi=500,
                           wspace=None,
                           para_dict=None,
                           draw_pic=True,
                           low_pic=False,
                           interactive=False,
                           pic_only=False,
                           run_dash=False):
        """
        - adata:
        - color:
        - para_dict:
            - discrete_scatter_plot:
                {'title': '', 'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                 'legend_scale': 1.2, 'legend_ncol': math.ceil(len(self.color_dict) / 17),
                 'show_ticks_and_labels': True}
                - title: 标题
                - xlabel: x轴标题
                - ylabel: y轴标题
                - legend_scale: 图例图形大小
                - legend_ncol: 图例列数，默认一列17个元素
                - show_ticks_and_labels: 是否展示刻度

            - continuous_scatter_plot
                {'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                 'show_ticks_and_labels': True, 'shrink': 0.4, 'pad': 0.05}

        """
        if color == 'class':
            raise 'please change columns of class'

        if low_pic:
            if not self._low_contain:
                raise ValueError('no low pic in SpatialTools')

        if isinstance(adata, sc.AnnData):
            adata = adata.copy()
            adata.obs.index.name = None
            adata.obs['barcode'] = adata.obs.index
            self._adata_type = 'AnnData'

            obsm = self.container[self._get_adata_level(adata.obs)]['obsm']
            point_size = self.container[self._get_adata_level(adata.obs)]['point_size']

            plot_data = obsm.merge(adata.obs, on='barcode')

        elif isinstance(adata, pd.DataFrame):
            adata = adata.copy()
            adata.index.name = None

            if 'barcode' not in adata.columns:
                adata['barcode'] = adata.index

            self._adata_type = 'DataFrame'

            obsm = self.container[self._get_adata_level(adata)]['obsm']
            point_size = self.container[self._get_adata_level(adata)]['point_size']

            plot_data = obsm.merge(adata, on='barcode')

        else:
            raise 'wrong adata, should be AnnData and DataFrame'

        if plot_data.shape[0] == 0:
            raise ValueError('barcodes of pic and matrix are inconsistent ...')

        if not feature:

            plot_data[color] = plot_data[color].astype(str)

            # 离散型散点图
            prob = list(plot_data[color].value_counts().index)

            if not color_dict:
                number_col = len(prob)
                if number_col <= 12:
                    selected_col = list(sns.color_palette("Paired", number_col))
                else:
                    selected_col = list(sns.color_palette(None, number_col))

                color_dict = dict(zip(prob, selected_col))

            if groups:

                for i in groups:
                    if i not in plot_data[color].unique():
                        raise 'groups not in column of color'

                plot_data = plot_data.query('{} in {}'.format(color, groups))
                plot_data[color] = plot_data[color].astype("category")
                plot_data[color] = plot_data[color].cat.set_categories(groups, ordered=True)
                prob = groups

            if darken:
                color_dict = {k: self._lighten_color(v, darken) for k, v in color_dict.items()}

            if not low_pic:
                plot_data['__x'] = np.round(plot_data['__x'] * self.scalar, 2)
                plot_data['__y'] = np.round(plot_data['__y'] * self.scalar, 2)

            else:
                plot_data['__x'] = np.round(plot_data['__x'] * self.low_scalar, 2)
                plot_data['__y'] = np.round(plot_data['__y'] * self.low_scalar, 2)

            if crop_coord:
                plot_pic, plot_data = self._crop_coord(plot_data=plot_data, low_pic=low_pic, crop_coord=crop_coord)
            else:
                plot_pic = self._low_pic if low_pic else self._pic

            size = point_size ** 2 if size == 1 else point_size ** 2 * size

            grouped = plot_data.groupby(color)

            # 执行交互
            if interactive or run_dash:
                fig = SpatialApp.interact_pic_discrete(plot_data_grouped=grouped,
                                                       pic=plot_pic,
                                                       color=color,
                                                       color_dict=dict(
                                                           zip(prob, sns.color_palette(None, len(prob)).as_hex())),
                                                       size=size,
                                                       alpha=alpha,
                                                       figsize=figsize,
                                                       pic_only=pic_only,
                                                       draw_pic=draw_pic,
                                                       to_save=to_save)

                return fig

            fig, ax = plt.subplots(constrained_layout=True, figsize=figsize)

            start = 0
            for key, group in grouped:

                if key in prob:
                    if split:
                        grid_dim = self._facet_pos(length=len(prob), ncol=ncol)
                        ax = plt.subplot2grid(grid_dim, self._facet_pos_list[start])
                        plt.tight_layout()
                        start += 1

                    group.plot(ax=ax, kind='scatter', x='__x', y='__y',
                               label=key,
                               c=color_dict[key],
                               s=size,
                               alpha=alpha)

                    self._discrete_scatter_plot(ax=ax,
                                                para_dict=para_dict,
                                                color_dict=color_dict)

                    if wspace:
                        plt.subplots_adjust(hspace=int(wspace))
                    if hspace:
                        plt.subplots_adjust(hspace=int(hspace))

                    if draw_pic:
                        plt.imshow(plot_pic)

            if not draw_pic:
                plt.gca().invert_yaxis()

            # plot_data = plot_data2

            # handles, labels = plt.gca().get_legend_handles_labels()
            # if self.levels:
            #     legend_order = [labels.index(i) for i in self.levels]
            # else:
            #     legend_order = [labels.index(i) for i in labels]
            #
            # ax.legend([handles[idx] for idx in legend_order], [labels[idx] for idx in legend_order])

        else:
            # 连续型散点图
            if not isinstance(feature, list):
                feature = [feature]

            if self._adata_type == 'AnnData':
                # in Anndata
                adata.var['symbol'] = adata.var.index
                prob = [i for i in feature if i in adata.obs.columns]

                if 'gene_ids' not in adata.var.columns:
                    adata.var['gene_ids'] = adata.var.index

                if 'symbol' not in adata.var.columns:
                    adata.var['symbol'] = adata.var.index

                symbol = list(adata.var.query('gene_ids in {} or symbol in {}'.format(feature, feature)).index)
                if not len(symbol) == 0:
                    gene_df = adata[:, symbol].to_df()
                    gene_df['barcode'] = gene_df.index
                    plot_data = plot_data.merge(gene_df, on='barcode')
                    prob += symbol

            else:
                prob = [i for i in feature if i in adata.columns]

            if len(prob) == 0:
                raise ValueError('wrong feature')

            size = point_size ** 2 if size == 1 else point_size ** 2 * size

            plot_para_dict = {'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                              'show_ticks_and_labels': True, 'shrink': 0.4, 'pad': 0.05}

            if para_dict:
                plot_para_dict = self._change_para_dict(plot_para_dict, para_dict)

            if not low_pic:
                plot_data['__x'] = plot_data['__x'] * self.scalar
                plot_data['__y'] = plot_data['__y'] * self.scalar

            else:
                plot_data['__x'] = plot_data['__x'] * self.low_scalar
                plot_data['__y'] = plot_data['__y'] * self.low_scalar

            if crop_coord:
                plot_pic, plot_data = self._crop_coord(plot_data=plot_data, low_pic=low_pic, crop_coord=crop_coord)
            else:
                plot_pic = self._low_pic if low_pic else self._pic

            if interactive or run_dash:
                fig = SpatialApp.interact_pic_continuous(plot_data=plot_data,
                                                         pic=plot_pic,
                                                         feature=prob[0],
                                                         size=size,
                                                         alpha=alpha,
                                                         cmap=cmap,
                                                         to_save=to_save,
                                                         pic_only=pic_only,
                                                         figsize=figsize,
                                                         draw_pic=draw_pic)

                return fig

            fig, ax = plt.subplots(constrained_layout=True, figsize=figsize)

            start = 0

            for feature in prob:
                if len(prob) > 1:
                    grid_dim = self._facet_pos(length=len(prob), ncol=ncol)
                    ax = plt.subplot2grid(grid_dim, self._facet_pos_list[start])
                    plt.tight_layout()
                    start += 1

                if alpha_map_to_value:
                    from sklearn.preprocessing import MinMaxScaler
                    scalar_alpha = MinMaxScaler(feature_range=(0, 1))
                    alpha = [i[0] for i in scalar_alpha.fit_transform(pd.DataFrame(np.array(plot_data[feature])))]

                if value_limits:
                    from sklearn.preprocessing import MinMaxScaler
                    scalar_value = MinMaxScaler(feature_range=value_limits)
                    value = [i[0] for i in scalar_value.fit_transform(pd.DataFrame(np.array(plot_data[feature])))]
                else:
                    value = plot_data[feature]

                plt.scatter(x=plot_data['__x'],
                            y=plot_data['__y'],
                            alpha=alpha,
                            s=size, cmap=cmap,
                            c=value)

                plt.title(feature)
                plt.xlabel(plot_para_dict['xlabel'])
                plt.ylabel(plot_para_dict['ylabel'])
                plt.colorbar(shrink=float(plot_para_dict['shrink']), pad=float(plot_para_dict['pad']))

                if draw_pic:
                    plt.imshow(plot_pic)
                else:
                    plt.gca().invert_yaxis()

                if not plot_para_dict['show_ticks_and_labels'] or plot_para_dict['show_ticks_and_labels'] == 'False':
                    plt.xticks([])
                    plt.yticks([])
                    ax.xaxis.set_ticklabels([])
                    ax.yaxis.set_ticklabels([])

                if wspace:
                    plt.subplots_adjust(hspace=float(wspace))
                if hspace:
                    plt.subplots_adjust(hspace=float(hspace))

        if to_save:
            self._plot_save(fig, to_save=to_save, dpi=dpi)

        if return_fig and return_table:
            return fig, plot_data

        if return_fig:
            return fig

        if return_table:
            return plot_data


if __name__ == '__main__':
    desc = """
    Version: Version v2.1.1 beta
    Contact: zhangjm <zhangjm@biomarker.com.cn>
    Program Date: 2022.10.25
    Description: spatial tools
    """

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--pic', type=str, help='seurat_obj')
    parser.add_argument('--barcodes_pos', type=str, help='barcodes pos')
    parser.add_argument('--adata', type=str, help='pd.DataFrame or AnnData')
    parser.add_argument('--color', type=str, help='seurat_clusters')
    parser.add_argument('--feature', type=str, help='feature', default=None)
    parser.add_argument('--dpi', type=int, help='dpi', default=500)
    parser.add_argument('--groups', type=str, help='groups', default=None)
    parser.add_argument('--size', type=float, help='dot size', default=1)
    parser.add_argument('--alpha', type=float, help='alpha', default=1)
    parser.add_argument('--figsize', type=str, help='figsize', default='(10, 10)')
    parser.add_argument('--to_save', type=str, help='to_save', default=None)
    parser.add_argument('--darken', type=float, help='darken the color', default=None)
    parser.add_argument('--return_fig', type=bool, help='return_fig', default=False)
    parser.add_argument('--return_table', type=bool, help='return_table', default=False)
    parser.add_argument('--split', type=bool, help='colnames of groups', default=False)
    parser.add_argument('--ncol', type=int, help='ncol', default=2)
    parser.add_argument('--color_dict', type=str, help='color_dict', default=None)
    parser.add_argument('--hspace', type=float, help='hspace', default=None)
    parser.add_argument('--wspace', type=float, help='wspace', default=None)
    parser.add_argument('--para_dict', type=str, help='para_dict', default=None)
    input_args = parser.parse_args()

    st_data = SpatialTools(pic=input_args.pic, barcodes_pos=input_args.barcodes_pos)

    if input_args.groups:
        input_args.groups = st_data.resolve_para_to_list_tuple_dict(input_args.groups, list, str)

    if input_args.figsize:
        input_args.figsize = st_data.resolve_para_to_list_tuple_dict(input_args.figsize, tuple, float)

    if input_args.feature:
        input_args.feature = st_data.resolve_para_to_list_tuple_dict(input_args.feature, list, str)

    if input_args.color_dict:
        input_args.color_dict = st_data.resolve_para_to_list_tuple_dict(input_args.color_dict, dict)

    if input_args.para_dict:
        input_args.para_dict = st_data.resolve_para_to_list_tuple_dict(input_args.para_dict, dict)

    logging.info('input args: {}'.format(input_args))

    if str(input_args.adata).endswith('.xls'):
        logging.info('reading xls')
        adata = pd.read_csv(input_args.adata, sep='\t')
        if 'barcode' not in adata.columns:
            raise ValueError('xls file must contains barcode column')
        else:
            adata.index = adata['barcode']
            adata.index.name = None

    elif str(input_args.adata).endswith('.loom'):
        logging.info('reading loom file ...')
        adata = sc.read_loom(input_args.adata)

    else:
        raise ValueError('wrong adata args!')

    logging.info('plotting ...')
    st_data.s1000_spatial_plot(
        adata=adata,
        color=input_args.color,
        groups=input_args.groups,
        size=input_args.size,
        alpha=input_args.alpha,
        figsize=input_args.figsize,
        to_save=input_args.to_save,
        darken=input_args.darken,
        dpi=input_args.dpi,
        return_fig=input_args.return_fig,
        return_table=input_args.return_table,
        feature=input_args.feature,
        split=input_args.split,
        ncol=input_args.ncol,
        color_dict=input_args.color_dict,
        hspace=input_args.hspace,
        wspace=input_args.wspace,
        para_dict=input_args.para_dict)

    logging.info('done!')
