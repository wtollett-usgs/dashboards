# -*- coding: utf-8 -*-
import dash_html_components as html

from . import layouts
from .components import Row

kisum = [
            Row([
                layouts.youtube_container(),
                layouts.links_list()
            ], **dict(className='spacer')),
            Row(layouts.summit_rsam(), **dict(className='spacer')),
            Row(layouts.summit_tilt(), **dict(className='spacer')),
            Row(layouts.summit_rtnet(), **dict(className='spacer')),
            Row(layouts.summit_hypos(), **dict(className='spacer')),
            Row(layouts.summit_counts(), **dict(className='spacer')),
            Row(layouts.summit_spectrograms(), **dict(className='spacer')),
            Row([
               layouts.summit_helicorder(),
               layouts.summit_tiltv()
            ], **dict(className='spacer')),
            Row(layouts.summit_gas(), **dict(className='spacer')),
            Row([
               layouts.ash3d(),
               layouts.logs()
            ], **dict(className='spacer')),
            html.Div(id='kism-hypos-storage', style={'display': 'none'}),
            html.Div(id='kism-counts-storage', style={'display': 'none'})
        ]
kmerz = html.Div("MERZ")
klerz = [
            Row([
                layouts.cams_container(),
                layouts.links_list()
            ], **dict(className='spacer')),
            Row(layouts.lerz_rsam(), **dict(className='spacer')),
            Row(layouts.lerz_rtnet(), **dict(className='spacer')),
            Row(layouts.lerz_hypos(), **dict(className='spacer')),
            Row(layouts.lerz_counts(), **dict(className='spacer')),
            Row(layouts.lerz_spectrograms(), **dict(className='spacer')),
            Row(layouts.lerz_gas(), **dict(className='spacer')),
            Row([
                layouts.lerz_helicorder(),
                layouts.logs()
            ], **dict(className='spacer')),
            html.Div(id='lerz-hypos-storage', style={'display': 'none'}),
            html.Div(id='lerz-counts-storage', style={'display': 'none'})
        ]


def page_not_found(pathname):
    return html.P("No page '{}'".format(pathname))
