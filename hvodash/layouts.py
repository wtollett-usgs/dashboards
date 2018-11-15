# -*- coding: utf-8 -*-
import dash_core_components as dcc

from dash_html_components import Div, A, H3, Iframe, Img, Table
from dash_table_experiments import DataTable

from .components import Col, Row, Header, RefreshButton
from .constants import STREAM_CAM, LINKS, PERIODS
from .server import server


"""Contains layouts suitable for being the value of the 'layout' attribute of
Dash app instances."""


def main_layout_header():
    """Dash layout with a top-header"""
    return Div([
        Div(
            id="header",
            children=[
                Header(),
                Div(id=server.config['NAVBAR_CONTAINER_ID']),
            ]
        ),
        Div(
            className='container-fluid',
            children=Row(
                Col(id=server.config['CONTENT_CONTAINER_ID'])
            )
        ),
        dcc.Location(id='url', refresh=False),
        Div(DataTable(rows=[{}]), style={'display': 'none'})
    ])


def section_header(section, title):
    return [
        Row(Col(H3(f'{title}', style=dict(textAlign='center')))),
        Row([
            Col(dcc.Dropdown(
                id=f'{section}-{title.lower()}-time-dropdown',
                options=[{'label': i.split('_')[1], 'value': PERIODS[i]}
                         for i in sorted(list(PERIODS.keys()))],
                value=28800000,
                searchable=False,
                clearable=False
            ), bp='md', size=2, **dict(className='offset-md-4')),
            Col(RefreshButton(btnid=f'{section}-refresh-{title.lower()}-btn'),
                **dict(className='offset-md-0.5')
            )
        ])
    ]


def youtube_container():
    return Col(
        Div(Iframe(src=STREAM_CAM, width=560, height=315)),
        bp='md',
        size=8,
        **dict(className='text-center')
    )


def cams_container():
    return Col([
        Div(id='slideshow-img'),
        dcc.Interval(id='slideshow-interval', interval=5000)
    ], bp='md', size=8, **dict(className='text-center'))


def links_list():
    return Col(
        [Row(A(href=LINKS[i],
               children=i.split('_')[1],
               target='_blank'
               )) for i in sorted(list(LINKS.keys()),
                                  key=lambda x: int(x.split('_')[0]))],
        bp='md',
        size=3
    )


def ash3d():
    return Col([
        Row(
            Col([
                H3('Ash3d'),
                RefreshButton(btnid='refresh-ash3d-btn')
            ], **dict(className='text-center'))
        ),
        Row(Col(Img(id='ash3d-img', src='', width='100%')))
    ], size=5)


def logs():
    return Col([
        Row(
            Col([
                H3('Logs'),
                RefreshButton(btnid='kism-refresh-logs-btn')
            ], **dict(className='text-center'))
        ),
        Row(
            Col(Table(className='table', id='kism-logs-table'))
        )
    ])


#
# Summit Containers
#
def summit_rsam():
    return Col(section_header('kism', 'RSAM') +
    [
        Row([
            Col('UWE', **dict(style=dict(textAlign='center'))),
            Col('RIMD', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='uwe-rsam-graph', animate=True)),
            Col(dcc.Graph(id='rimd-rsam-graph', animate=True)),
        ]),
        Row([
            Col('AHUD', **dict(style=dict(textAlign='center'))),
            Col('SDH', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='ahud-rsam-graph', animate=True)),
            Col(dcc.Graph(id='sdh-rsam-graph', animate=True)),
        ])
    ], bp='md', size=12)


def summit_tilt():
    return Col(section_header('kism', 'Tilt') +
    [
        Row([
            Col('SMC', **dict(style=dict(textAlign='center'))),
            Col('SDH', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='smc-tilt-graph', animate=True)),
            Col(dcc.Graph(id='sdh-tilt-graph', animate=True)),
        ]),
        Row([
            Col('UWE', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='uwe-tilt-graph', animate=True)),
        ])
    ], bp='md', size=12)


def summit_rtnet():
    return Col(section_header('kism', 'RTNet') +
    [
        Row([
            Col('UWEV', **dict(style=dict(textAlign='center'))),
            Col('CALS', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='uwev-rtnet-graph', animate=True)),
            Col(dcc.Graph(id='cals-rtnet-graph', animate=True)),
        ])
    ], bp='md', size=12)


def summit_hypos():
    return Col([
        Row(Col(H3('Seismicity', style=dict(textAlign='center')))),
        Row([
            Col(dcc.RadioItems(
                id='kism-hypos-radio',
                options=[
                    {'label': 'Time', 'value': 'T'},
                    {'label': 'Depth', 'value': 'A'}
                ],
                value='A'
            ), bp='md', size=6, **dict(className='text-center')),
            Col(dcc.Dropdown(
                id='kism-seismic-time-dropdown',
                options=[{'label': i.split('_')[1], 'value': PERIODS[i]}
                         for i in sorted(list(PERIODS.keys()))],
                value=28800000,
                searchable=False,
                clearable=False
            ), bp='md', size=2)
        ]),
        Row([
            Col(
                Col([
                    Iframe(id='kism-hypos-plot',
                           srcDoc='',
                           width='100%',
                           height=400),
                    Img(id='kism-hypos-legend', src='', width='100%')
                ], bp='md', size=11, **dict(className='offset-md-1')
            )),
            Col(
                Col(
                    DataTable(
                        rows=[{}],
                        columns=('date', 'lat', 'lon', 'depth', 'prefMag'),
                        column_widths=[None, 125, 125, 75, 75],
                        filterable=True,
                        sortable=True,
                        id='kism-datatable-hypos'
                    ), bp='md', size=11
                )
            )
        ])
    ], bp='md', size=12)


def summit_counts():
    return Col(section_header('kism', 'Counts') +
    [
        Row(
            Col(dcc.Graph(id='kism-counts-graph'),
                bp='md', size=10, **dict(className='offset-md-1'))
        )
    ], bp='md', size=12)


def summit_spectrograms():
    return Col([
        Row(
            Col([
                H3('Spectrograms'),
                RefreshButton(btnid='kism-refresh-spectrograms-btn')
            ], **dict(className='text-center'))
        ),
        Row([
            Col(Img(id='kism-pensive-plot', src=''), size=5,
                **dict(className='offset-md-1')),
            Col(Img(id='kism-ipensive-plot', src=''), size=5),
        ])
    ], bp='md', size=12)


def summit_helicorder():
    return Col([
        Row(
            Col([
                H3('RIMD'),
                RefreshButton(btnid='kism-refresh-helicorder-btn')
            ], **dict(className='text-center'))
        ),
        Row(Col(Img(id='kism-helicorder-plot', src='', width='100%')))
    ])


def summit_tiltv():
    return Col([
        Row(
            Col([
                H3('Tilt Vectors'),
                RefreshButton(btnid='kism-refresh-tiltv-btn')
            ], **dict(className='text-center'))
        ),
        Row(Col(Img(id='kism-tiltv-plot', src='', width='100%')))
    ])


def summit_gas():
    return Col(section_header('kism', 'SO2') +
    [
        Row(Col('SUMDFW SO2 Emissions', **dict(className='text-center'))),
        Row(
            Col(dcc.Graph(id='sumdfw-so2-graph'),
                bp='md', size=10, **dict(className='offset-md-1'))
        ),
        Row([
            Col('HAVO_KVC Avg SO2', **dict(style=dict(textAlign='center'))),
            Col('HAVO_KVC Wind', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='kvc-so2-graph', animate=True)),
            Col(dcc.Graph(id='kvc-wind-graph', animate=True)),
        ])
    ], bp='md', size=12)


#
# LERZ Containers
#
def lerz_rsam():
    return Col(section_header('lerz', 'RSAM') +
    [
        Row([
            Col('KIND', **dict(style=dict(textAlign='center'))),
            Col('KLUD', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='kind-rsam-graph', animate=True)),
            Col(dcc.Graph(id='klud-rsam-graph', animate=True)),
        ]),
        Row([
            Col('ERZ3', **dict(style=dict(textAlign='center'))),
            Col('ERZ4', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='erz3-rsam-graph', animate=True)),
            Col(dcc.Graph(id='erz4-rsam-graph', animate=True)),
        ])
    ], bp='md', size=12)


def lerz_rtnet():
    return Col(section_header('lerz', 'RTNet') +
    [
        Row([
            Col('KIND', **dict(style=dict(textAlign='center'))),
            Col('NANT', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='kind-rtnet-graph', animate=True)),
            Col(dcc.Graph(id='nant-rtnet-graph', animate=True)),
        ]),
        Row([
            Col('ERZ3', **dict(style=dict(textAlign='center'))),
            Col('ERZ4', **dict(style=dict(textAlign='center'))),
        ]),
        Row([
            Col(dcc.Graph(id='erz3-rtnet-graph', animate=True)),
            Col(dcc.Graph(id='erz4-rtnet-graph', animate=True)),
        ])
    ], bp='md', size=12)


def lerz_hypos():
    return Col([
        Row(Col(H3('Seismicity', style=dict(textAlign='center')))),
        Row([
            Col(dcc.RadioItems(
                id='lerz-hypos-radio',
                options=[
                    {'label': 'Time', 'value': 'T'},
                    {'label': 'Depth', 'value': 'A'}
                ],
                value='A'
            ), bp='md', size=6, **dict(className='text-center')),
            Col(dcc.Dropdown(
                id='lerz-seismic-time-dropdown',
                options=[{'label': i.split('_')[1], 'value': PERIODS[i]}
                         for i in sorted(list(PERIODS.keys()))],
                value=28800000,
                searchable=False,
                clearable=False
            ), bp='md', size=2)
        ]),
        Row([
            Col(
                Col([
                    Iframe(id='lerz-hypos-plot',
                           srcDoc='',
                           width='100%',
                           height=400),
                    Img(id='lerz-hypos-legend', src='', width='100%')
                ], bp='md', size=11, **dict(className='offset-md-1')
            )),
            Col(
                Col(
                    DataTable(
                        rows=[{}],
                        columns=('date', 'lat', 'lon', 'depth', 'prefMag'),
                        column_widths=[None, 125, 125, 75, 75],
                        filterable=True,
                        sortable=True,
                        id='lerz-datatable-hypos'
                    ), bp='md', size=11
                )
            )
        ])
    ], bp='md', size=12)


def lerz_counts():
    return Col(section_header('lerz', 'Counts') +
    [
        Row(
            Col(dcc.Graph(id='lerz-counts-graph'),
                bp='md', size=10, **dict(className='offset-md-1'))
        )
    ], bp='md', size=12)


def lerz_spectrograms():
    return Col([
        Row(
            Col([
                H3('Spectrograms'),
                RefreshButton(btnid='lerz-refresh-spectrograms-btn')
            ], **dict(className='text-center'))
        ),
        Row([
            Col(Img(id='lerz-pensive-plot', src=''), size=5,
                **dict(className='offset-md-1')),
            Col(Img(id='lerz-ipensive-plot', src=''), size=5),
        ])
    ], bp='md', size=12)


def lerz_helicorder():
    return Col([
        Row(
            Col([
                H3('KLUD'),
                RefreshButton(btnid='lerz-refresh-helicorder-btn')
            ], **dict(className='text-center'))
        ),
        Row(Col(Img(id='lerz-helicorder-plot', src='', width='100%')))
    ])


def lerz_gas():
    return Col([
        Row(
            Col([
                H3('LERZ SO2 Emissions'),
                RefreshButton(btnid='lerz-refresh-so2-btn')
            ], **dict(className='text-center'))
        ),
        Row(Col(dcc.Graph(id='lerz-so2-graph'),
                bp='md', size=10, **dict(className='offset-md-1')))
    ])
