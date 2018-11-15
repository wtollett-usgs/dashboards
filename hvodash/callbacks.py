# -*- coding: utf-8 -*-
import dash_html_components as html

from dash.dependencies import Output, Input, State

from . import data
from .constants import (
    API_PERIODS,
    LERZ_IPENSIVE,
    LERZ_PENSIVE,
    SUMMIT_IPENSIVE,
    SUMMIT_PENSIVE,
)
from .server import app


#
# RSAM
#
@app.callback(
    Output('uwe-rsam-graph', 'figure'),
    [Input('kism-refresh-rsam-btn', 'n_clicks'),
     Input('kism-rsam-time-dropdown', 'value')]
)
def update_uwe_rsam(nclicks, st):
    return data.get_rsam('uwe$hhz$hv', API_PERIODS[str(st)])


@app.callback(
    Output('rimd-rsam-graph', 'figure'),
    [Input('kism-refresh-rsam-btn', 'n_clicks'),
     Input('kism-rsam-time-dropdown', 'value')]
)
def update_rimd_rsam(nclicks, st):
    return data.get_rsam('rimd$hwz$hv', API_PERIODS[str(st)])


@app.callback(
    Output('ahud-rsam-graph', 'figure'),
    [Input('kism-refresh-rsam-btn', 'n_clicks'),
     Input('kism-rsam-time-dropdown', 'value')]
)
def update_ahud_rsam(nclicks, st):
    return data.get_rsam('ahud$ewz$hv', API_PERIODS[str(st)])


@app.callback(
    Output('sdh-rsam-graph', 'figure'),
    [Input('kism-refresh-rsam-btn', 'n_clicks'),
     Input('kism-rsam-time-dropdown', 'value')]
)
def update_sdh_rsam(nclicks, st):
    return data.get_rsam('sdh$hwz$hv', API_PERIODS[str(st)])


@app.callback(
    Output('kind-rsam-graph', 'figure'),
    [Input('lerz-refresh-rsam-btn', 'n_clicks'),
     Input('lerz-rsam-time-dropdown', 'value')]
)
def update_kind_rsam(nclicks, st):
    return data.get_rsam('kind$hwz$hv', API_PERIODS[str(st)])


@app.callback(
    Output('klud-rsam-graph', 'figure'),
    [Input('lerz-refresh-rsam-btn', 'n_clicks'),
     Input('lerz-rsam-time-dropdown', 'value')]
)
def update_klud_rsam(nclicks, st):
    return data.get_rsam('klud$ewz$hv', API_PERIODS[str(st)])


@app.callback(
    Output('erz3-rsam-graph', 'figure'),
    [Input('lerz-refresh-rsam-btn', 'n_clicks'),
     Input('lerz-rsam-time-dropdown', 'value')]
)
def update_erz3_rsam(nclicks, st):
    return data.get_rsam('erz3$hwz$hv', API_PERIODS[str(st)])


@app.callback(
    Output('erz4-rsam-graph', 'figure'),
    [Input('lerz-refresh-rsam-btn', 'n_clicks'),
     Input('lerz-rsam-time-dropdown', 'value')]
)
def update_erz4_rsam(nclicks, st):
    return data.get_rsam('erz4$hwz$hv', API_PERIODS[str(st)])


#
# Tilt
#
@app.callback(
    Output('smc-tilt-graph', 'figure'),
    [Input('kism-refresh-tilt-btn', 'n_clicks'),
     Input('kism-tilt-time-dropdown', 'value')]
)
def update_smc_tilt(nclicks, st):
    return data.get_tilt('smc', API_PERIODS[str(st)])


@app.callback(
    Output('sdh-tilt-graph', 'figure'),
    [Input('kism-refresh-tilt-btn', 'n_clicks'),
     Input('kism-tilt-time-dropdown', 'value')]
)
def update_sdh_tilt(nclicks, st):
    return data.get_tilt('sdh', API_PERIODS[str(st)])


@app.callback(
    Output('uwe-tilt-graph', 'figure'),
    [Input('kism-refresh-tilt-btn', 'n_clicks'),
     Input('kism-tilt-time-dropdown', 'value')]
)
def update_uwe_tilt(nclicks, st):
    return data.get_tilt('uwe', API_PERIODS[str(st)])


#
# RTNet
#
@app.callback(
    Output('uwev-rtnet-graph', 'figure'),
    [Input('kism-refresh-rtnet-btn', 'n_clicks'),
     Input('kism-rtnet-time-dropdown', 'value')]
)
def update_uwev_rtnet(nclicks, st):
    return data.get_rtnet('uwev', API_PERIODS[str(st)])


@app.callback(
    Output('cals-rtnet-graph', 'figure'),
    [Input('kism-refresh-rtnet-btn', 'n_clicks'),
     Input('kism-rtnet-time-dropdown', 'value')]
)
def update_cals_rtnet(nclicks, st):
    return data.get_rtnet('cals', API_PERIODS[str(st)])


@app.callback(
    Output('kind-rtnet-graph', 'figure'),
    [Input('lerz-refresh-rtnet-btn', 'n_clicks'),
     Input('lerz-rtnet-time-dropdown', 'value')]
)
def update_kind_rtnet(nclicks, st):
    return data.get_rtnet('kind', API_PERIODS[str(st)])


@app.callback(
    Output('nant-rtnet-graph', 'figure'),
    [Input('lerz-refresh-rtnet-btn', 'n_clicks'),
     Input('lerz-rtnet-time-dropdown', 'value')]
)
def update_nant_rtnet(nclicks, st):
    return data.get_rtnet('nant', API_PERIODS[str(st)])


@app.callback(
    Output('erz3-rtnet-graph', 'figure'),
    [Input('lerz-refresh-rtnet-btn', 'n_clicks'),
     Input('lerz-rtnet-time-dropdown', 'value')]
)
def update_erz3_rtnet(nclicks, st):
    return data.get_rtnet('erz3', API_PERIODS[str(st)])


@app.callback(
    Output('erz4-rtnet-graph', 'figure'),
    [Input('lerz-refresh-rtnet-btn', 'n_clicks'),
     Input('lerz-rtnet-time-dropdown', 'value')]
)
def update_erz4_rtnet(nclicks, st):
    return data.get_rtnet('erz4', API_PERIODS[str(st)])


#
# Hypocenters
#
@app.callback(
    Output('kism-hypos-storage', 'children'),
    [Input('kism-seismic-time-dropdown', 'value')],
    [State('kism-hypos-storage', 'children')]
)
def update_summit_hypo_data(val, olddata=None):
    return data.get_and_store_hypos('kilauea_summit',
                                    API_PERIODS[str(val)],
                                    olddata)


@app.callback(
    Output('kism-hypos-plot', 'srcDoc'),
    [Input('kism-hypos-storage', 'children'),
     Input('kism-hypos-radio', 'value')],
    [State('kism-seismic-time-dropdown', 'value')]
)
def update_summit_hypos_plot(olddata, kind, val):
    return data.get_hypos_map(API_PERIODS[str(val)], kind, olddata, 'kism')


@app.callback(
    Output('kism-hypos-legend', 'src'),
    [Input('kism-hypos-radio', 'value')]
)
def update_summit_hypos_legend(kind):
    return data.get_hypos_legend(kind)


@app.callback(
    Output('kism-datatable-hypos', 'rows'),
    [Input('kism-hypos-storage', 'children')],
    [State('kism-seismic-time-dropdown', 'value')]
)
def update_summit_hypos_table(olddata, val):
    return data.get_hypos_table(API_PERIODS[str(val)], olddata)


@app.callback(
    Output('lerz-hypos-storage', 'children'),
    [Input('lerz-seismic-time-dropdown', 'value')],
    [State('lerz-hypos-storage', 'children')]
)
def update_lerz_hypo_data(val, olddata=None):
    return data.get_and_store_hypos('kilauea_lerz',
                                    API_PERIODS[str(val)],
                                    olddata)


@app.callback(
    Output('lerz-hypos-plot', 'srcDoc'),
    [Input('lerz-hypos-storage', 'children'),
     Input('lerz-hypos-radio', 'value')],
    [State('lerz-seismic-time-dropdown', 'value')]
)
def update_lerz_hypos_plot(olddata, kind, val):
    return data.get_hypos_map(API_PERIODS[str(val)], kind, olddata, 'lerz')


@app.callback(
    Output('lerz-hypos-legend', 'src'),
    [Input('lerz-hypos-radio', 'value')]
)
def update_lerz_hypos_legend(kind):
    return data.get_hypos_legend(kind)


@app.callback(
    Output('lerz-datatable-hypos', 'rows'),
    [Input('lerz-hypos-storage', 'children')],
    [State('lerz-seismic-time-dropdown', 'value')]
)
def update_lerz_hypos_table(olddata, val):
    return data.get_hypos_table(API_PERIODS[str(val)], olddata)


#
# Counts
#
@app.callback(
    Output('kism-counts-storage', 'children'),
    [Input('kism-refresh-counts-btn', 'n_clicks'),
     Input('kism-counts-time-dropdown', 'value')],
    [State('kism-counts-storage', 'children')]
)
def update_summit_counts_data(click, val, olddata=None):
    return data.get_and_store_hypos('kilauea_summit',
                                    API_PERIODS[str(val)],
                                    olddata)


@app.callback(
    Output('kism-counts-graph', 'figure'),
    [Input('kism-counts-storage', 'children')],
    [State('kism-counts-time-dropdown', 'value')]
)
def update_summit_counts_plot(olddata, val):
    return data.get_hypo_counts(API_PERIODS[str(val)], olddata)


@app.callback(
    Output('lerz-counts-storage', 'children'),
    [Input('lerz-refresh-counts-btn', 'n_clicks'),
     Input('lerz-counts-time-dropdown', 'value')],
    [State('lerz-counts-storage', 'children')]
)
def update_lerz_counts_data(click, val, olddata=None):
    return data.get_and_store_hypos('kilauea_lerz',
                                    API_PERIODS[str(val)],
                                    olddata)


@app.callback(
    Output('lerz-counts-graph', 'figure'),
    [Input('lerz-counts-storage', 'children')],
    [State('lerz-counts-time-dropdown', 'value')]
)
def update_lerz_counts_plot(olddata, val):
    return data.get_hypo_counts(API_PERIODS[str(val)], olddata)


#
# Gas plots
#
@app.callback(
    Output('sumdfw-so2-graph', 'figure'),
    [Input('kism-refresh-so2-btn', 'n_clicks'),
     Input('kism-so2-time-dropdown', 'value')]
)
def update_sumdfw_so2_plot(click, st):
    return data.get_so2emissions('sumdfw', '-1y')


@app.callback(
    Output('kvc-so2-graph', 'figure'),
    [Input('kism-refresh-so2-btn', 'n_clicks'),
     Input('kism-so2-time-dropdown', 'value')]
)
def update_kvc_so2_plot(click, st):
    return data.get_nps_so2('havo_kvc', API_PERIODS[str(st)])


@app.callback(
    Output('kvc-wind-graph', 'figure'),
    [Input('kism-refresh-so2-btn', 'n_clicks'),
     Input('kism-so2-time-dropdown', 'value')]
)
def update_kvc_wind_plot(click, st):
    return data.get_nps_wind('havo_kvc', API_PERIODS[str(st)])


@app.callback(
    Output('lerz-so2-graph', 'figure'),
    [Input('lerz-refresh-so2-btn', 'n_clicks')]
)
def update_lerz_so2_plot(click):
    return data.get_so2emissions('lerz', '-1y')


#
# Images/Valve Plots
#
@app.callback(
    Output('kism-pensive-plot', 'src'),
    [Input('kism-refresh-spectrograms-btn', 'n_clicks')]
)
def update_summit_pensive_plot(val):
    return data.get_spectrogram(SUMMIT_PENSIVE)


@app.callback(
    Output('kism-ipensive-plot', 'src'),
    [Input('kism-refresh-spectrograms-btn', 'n_clicks')]
)
def update_summit_ipensive_plot(val):
    return data.get_spectrogram(SUMMIT_IPENSIVE)


@app.callback(
    Output('kism-helicorder-plot', 'src'),
    [Input('kism-refresh-helicorder-btn', 'n_clicks')]
)
def update_summit_helicorder_plot(val):
    return data.get_helicorder('RIMD$HWZ$HV')


@app.callback(
    Output('kism-tiltv-plot', 'src'),
    [Input('kism-refresh-tiltv-btn', 'n_clicks')]
)
def update_summit_tiltv_plot(val):
    return data.get_tiltv('kism')


@app.callback(
    Output('ash3d-img', 'src'),
    [Input('refresh-ash3d-btn', 'n_clicks')]
)
def update_ash3d_img(val):
    return data.get_ash3d_img()


@app.callback(
    Output('kism-logs-table', 'children'),
    [Input('kism-refresh-logs-btn', 'n_clicks')]
)
def update_summit_logs(val):
    return data.get_logs()[0]


@app.callback(
    Output('lerz-pensive-plot', 'src'),
    [Input('lerz-refresh-spectrograms-btn', 'n_clicks')]
)
def update_lerz_pensive_plot(val):
    return data.get_spectrogram(LERZ_PENSIVE)


@app.callback(
    Output('lerz-ipensive-plot', 'src'),
    [Input('lerz-refresh-spectrograms-btn', 'n_clicks')]
)
def update_lerz_ipensive_plot(val):
    return data.get_spectrogram(LERZ_IPENSIVE)


@app.callback(
    Output('lerz-helicorder-plot', 'src'),
    [Input('lerz-refresh-helicorder-btn', 'n_clicks')]
)
def update_lerz_helicorder_plot(val):
    return data.get_helicorder('KLUD$EWZ$HV')


@app.callback(
    Output('slideshow-img', 'children'),
    [Input('slideshow-interval', 'n_intervals')]
)
def update_slideshow_image(n):
    url = 'https://hvovalve.wr.usgs.gov/cams/data/{}/images/M.jpg'
    if n is None or n % 6 == 1:
        cam = 'LPcam'
    elif n % 6 == 2:
        cam = 'LQcam'
    elif n % 6 == 3:
        cam = 'LScam'
    elif n % 6 == 4:
        cam = 'LTcam'
    elif n % 6 == 5:
        cam = 'L3cam'
    elif n % 6 == 0:
        cam = 'L8cam'
    return html.Img(src=url.format(cam), width='50%')
