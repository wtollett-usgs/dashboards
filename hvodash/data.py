# -*- coding: utf-8 -*-
import pandas as pd
import plotly.graph_objs as go
import requests

from base64 import b64encode as be
from dash_html_components import Th, Tr, Td, A
from datetime import datetime, timedelta
from flask import request
from folium import Map
from operator import itemgetter
from os.path import join, dirname, realpath
from random import randint
from requests.auth import HTTPBasicAuth
from .maputils import create_dcircle_marker, create_tcircle_marker
from .utils import (
    api_request_to_json,
    json_to_dataframe,
    starttime_str_to_seconds,
)

TMP = join(dirname(realpath(__file__)), '../tmp/')
LCL = join(dirname(realpath(__file__)), '../images/')


def get_rsam(ch, st):
    j = api_request_to_json(f'rsam?channel={ch}&starttime={st}')
    data = []
    d = pd.DataFrame(j['records'][ch])
    if not d.empty:
        d.set_index('date', inplace=True)
        data = [go.Scatter(
            x=d.index,
            y=d.rsam,
            mode='markers',
            marker=dict(size=4)
        )]
    return {
        'data': data,
        'layout': {
            'margin': {
                't': 30
            },
            'xaxis': {
                'range': [d.index.min(), d.index.max()]
            },
            'yaxis': {
                'range': [d.rsam.min() - 20, 2 * d.rsam.mean()]
            }
        }
    }


def get_tilt(ch, st):
    j = api_request_to_json(f'tilt?channel={ch}&starttime={st}')
    d = pd.DataFrame(j['records'][ch])
    traces = []
    if not d.empty:
        d.set_index('date', inplace=True)
        traces.append({
            'x': d.index,
            'y': d['radial'],
            'name': f"radial {j['used_azimuth']:.1f}"
        })
        traces.append({
            'x': d.index,
            'y': d['tangential'],
            'name': f"tangential {j['tangential_azimuth']:.1f}"
        })
    return {
        'data': traces,
        'layout': {
            'margin': {
                't': 30
            }
        }
    }


def get_rtnet(ch, st):
    j = api_request_to_json(f'rtnet?channel={ch}&starttime={st}')
    d = pd.DataFrame(j['records'][ch])
    traces = []
    if not d.empty:
        d.set_index('date', inplace=True)
        traces.append({
            'x': d.index,
            'y': d.east,
            'name': 'East',
            'mode': 'markers',
            'marker': dict(
                size=4
            )
        })
        traces.append({
            'x': d.index,
            'y': d.north,
            'name': 'North',
            'mode': 'markers',
            'marker': dict(
                size=4
            )
        })
        traces.append({
            'x': d.index,
            'y': d.up,
            'name': 'Up',
            'mode': 'markers',
            'marker': dict(
                size=4
            )
        })
    return {
        'data': traces,
        'layout': {
            'margin': {
                't': 30
            }
        }
    }


def get_and_store_hypos(geo, st, current_data):
    if is_data_needed(st, current_data):
        return get_hypos(geo, st).to_json()
    else:
        return current_data


def is_data_needed(st, data):
    if not data:
        return True
    now = datetime.now()
    olddata = pd.read_json(data)
    mindate = olddata.date.min()
    maxdate = olddata.date.max()
    td = now - mindate
    # Requested more than is currently stored?
    seconds = starttime_str_to_seconds(st)
    if seconds > (td.days * 86400 + td.seconds):
        return True
    # Data is old
    td = now - maxdate
    if (td.seconds / 60) > 10:
        return True
    return False


def get_hypos(geo, st):
    j = api_request_to_json(f'hypocenter?geo={geo}&starttime={st}')
    d = pd.DataFrame(j['records'])
    if not d.empty:
        d['date'] = d['date'].str.slice(stop=-2)
        d['date'] = pd.to_datetime(d['date'])
        d.reset_index(drop=True, inplace=True)
    return d


def get_hypos_map(st, kind, data, region):
    filename = f'{TMP}hypos{randint(0,9999):04d}.html'
    d = json_to_dataframe(st, data)
    m = None
    if region == 'kism':
        m = Map(location=[19.41, -155.27], min_zoom=12, max_zoom=15,
                zoom_start=13, tiles='Stamen Terrain')
    elif region == 'lerz':
        m = Map(location=[19.43, -154.88], min_zoom=11, max_zoom=15,
                zoom_start=11, tiles='Stamen Terrain')
    if kind == 'T':
        mid = d.date.min()
        mad = d.date.max()
        d.apply(create_tcircle_marker, arg=(m, mid, mad), axis=1)
    elif kind == 'A':
        d.apply(create_dcircle_marker, args=(m,), axis=1)
    m.save(filename)
    return open(filename, 'r').read()


def get_hypos_legend(kind):
    encoded_img = None
    if kind == 'A':
        encoded_img = be(open(f'{LCL}dlegend.png', 'rb').read())
    elif kind == 'T':
        encoded_img = be(open(f'{LCL}tlegend.png', 'rb').read())
    return f"data:image/jpg;base64,{encoded_img.decode('utf8')}"


def get_hypos_table(st, data):
    d = json_to_dataframe(st, data)
    if not d.empty:
        d.sort_values('date', inplace=True)
    return d.to_dict('records')


def get_hypo_counts(st, data):
    d = json_to_dataframe(st, data)
    data = []
    if not d.empty:
        d.sort_values('date', inplace=True)
        d['moment'] = d.prefMag.apply(lambda x:
                                      pow(10.0, 16.0 + ((3.0 * x)/2.0)))
        d['cmoment'] = d.moment.cumsum()
        bins = d.groupby(pd.Grouper(freq='60min', key='date')).count()
        data = [go.Bar(
                {
                    'x': bins.index,
                    'y': bins.depth,
                    'name': 'Count'
                }), go.Scatter(
                {
                    'x': d.date,
                    'y': d.cmoment,
                    'name': 'Moment',
                    'yaxis': 'y2'
                })]
    return {
        'data': data,
        'layout': {
            'margin': {
                't': 30
                },
            'showlegend': False,
            'yaxis': {
                'title': 'Earthquakes per Hour'
            },
            'yaxis2': {
                'title': 'Cumulative Moment (dyn-cm)',
                'showgrid': False,
                'overlaying': 'y',
                'side': 'right'
            }
        }
    }


def get_spectrogram(src):
    now = datetime.utcnow()
    d = now.timetuple().tm_yday
    tm = now - timedelta(minutes=now.minute % 10, seconds=now.second,
                         microseconds=now.microsecond)
    if 'ipensive' in src:
        t = '%d%s%s-%s%s' % (now.year, str(now.month).zfill(2),
                             str(now.day).zfill(2), str(tm.hour).zfill(2),
                             str(tm.minute).zfill(2))
    else:
        t = '%d%s-%s%s' % (now.year, str(d).zfill(3), str(tm.hour).zfill(2),
                           str(tm.minute).zfill(2))
    return src.format(now.year, d, t)


def get_helicorder(ch):
    url = f'a=plot&o=png&tz=Pacific/Honolulu&w=900&h=636&n=1&x.0=75&y.0=20' \
          f'&w.0=750&h.0=576&mh.0=900&chCnt.0=1' \
          f'&src.0=hvo_seismic_winston_helicorders&st.0=-28800000&et.0=N' \
          f'&chNames.0={ch}&dataTypes.0=275.000000&tc.0=15&barMult.0=3' \
          f'&sc.0=T&plotSeparately.0=false'
    encoded_img = be(open(get_valve_plot(url), 'rb').read())
    return f"data:image/jpg;base64,{encoded_img.decode('utf8')}"


def get_tiltv(region):
    chs = ''
    if region == 'kism':
        chs = '18,20'
    elif region == 'merz':
        chs = '15,16'
    url = f'a=plot&o=png&tz=Pacific/Honolulu&w=900&h=1740&n=1&x.0=75&y.0=20' \
          f'&w.0=750&h.0=240&mh.0=900&chCnt.0=7&src.0=hvo_def_tilt' \
          f'&st.0=-28800000&et.0=N&lg.0=true&ch.0={chs}' \
          f'&dataTypes.0=NaN&plotType.0=tv&rk.0=1&ds.0=None&dsInt.0=&sdt.0=' \
          f'&az.0=n&azval.0=&linetype.0=l&ysLMin.0=&ysLMax.0=&ysRMin.0=' \
          f'&ysRMax.0=&despike_period.0=&filter_arg1.0=&filter_arg2.0=' \
          f'&despike.0=F&detrend.0=F&dmo_fl.0=0&filter_arg3.0=' \
          f'&dmo_arithmetic.0=None&dmo_arithmetic_value.0=&dmo_db.0=0' \
          f'&debias_period.0=&radial.0=T&tangential.0=T&xTilt.0=F&yTilt.0=F' \
          f'&magnitude.0=F&azimuth.0=F&holeTemp.0=F&boxTemp.0=F&instVolt.0=F' \
          f'&rainfall.0=F&vs.0=&plotSeparately.0=false'
    encoded_img = be(open(get_valve_plot(url), 'rb').read())
    return f"data:image/jpg;base64,{encoded_img.decode('utf8')}"


def get_valve_plot(itm):
    filename = f'{TMP}valve{randint(0,9999):04d}.jpg'
    url = f'https://hvovalve.wr.usgs.gov/valve3/valve3.jsp?{itm}'
    u = request.authorization.username
    p = request.authorization.password
    r = requests.get(url, auth=HTTPBasicAuth(u, p))
    with open(filename, 'wb') as f:
        f.write(r.content)
    return filename


def get_ash3d_img():
    url = ('https://volcanoes.usgs.gov/vsc/captures/ash3d/'
           '332010_1008443_D_deposit.gif')
    return url


def get_logs(max_rows=20):
    p = api_request_to_json('logs')['posts']
    headers = ['Post', 'Author', 'Date']
    d = sorted(p, key=itemgetter('date'), reverse=True)
    link = 'https://hvointernal.wr.usgs.gov/hvo_logs/read?id={}'
    return [[Tr([Th(col) for col in headers])] +
            [Tr([
               Td(A(href=link.format(d[i]['id']),
                    children='%s' % d[i]['subject'],
                    target='_blank')),
               Td(children='%s' % d[i]['user']),
               Td(children='%s' % d[i]['date'])
            ]) for i in range(0, max_rows)]]


def get_so2emissions(ch, st):
    j = api_request_to_json(f'so2emissions?channel={ch}&starttime={st}')
    data = []
    d = pd.DataFrame(j['records'][ch])
    if not d.empty:
        d.set_index('date', inplace=True)
        data = [go.Scatter(
            x=d.index,
            y=d.so2,
            mode='markers',
            marker=dict(size=10)
        )]
    return {
        'data': data,
        'layout': {
            'margin': {
                't': 30
            }
        }
    }


def get_nps_so2(ch, st):
    j = api_request_to_json(f'npsadvisory?channel={ch}&starttime={st}')
    data = []
    d = pd.DataFrame(j['records'][ch])
    if not d.empty:
        d.set_index('date', inplace=True)
        data = [go.Scatter(
            x=d.index,
            y=d.avgso2,
            mode='markers',
            marker=dict(size=6)
        )]
    return {
        'data': data,
        'layout': {
            'margin': {
                't': 30
            },
            'yaxis': {
                'exponentformat': 'none'
            }
        }
    }


def get_nps_wind(ch, st):
    url = (f'npsadvisory?channel={ch}&starttime={st}&series=windspeed,winddir')
    j = api_request_to_json(url)
    data = []
    d = pd.DataFrame(j['records'][ch])
    if not d.empty:
        d.set_index('date', inplace=True)
        data = [go.Scatter(
            x=d.index,
            y=d.windspeed,
            name='Wind Speed',
            mode='markers',
            marker=dict(size=6)
        ), go.Scatter(
            x=d.index,
            y=d.winddir,
            name='Wind Dir',
            yaxis='y2',
            mode='markers',
            marker=dict(size=6)
        )]
    return {
        'data': data,
        'layout': {
            'margin': {
                't': 30
            },
            'yaxis': {
                'title': 'Windspeed (m/s)'
            },
            'yaxis2': {
                'title': 'Wind Direction (deg)',
                'showgrid': False,
                'overlaying': 'y',
                'side': 'right'
            }
        }
    }
