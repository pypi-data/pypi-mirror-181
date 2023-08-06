
from logging import getLogger
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
import kaleido
from nazca4sdk.sdk import SDK
from datetime import datetime
from datetime import date
import warnings
from elasticsearch import Elasticsearch

warnings.filterwarnings("ignore")
import requests
from nazca4sdk.datahandling.data_mod import Data
import pywebhdfs
from pywebhdfs.webhdfs import PyWebHdfsClient


async def execute(request, loggerName):
    logger = getLogger(loggerName)
    sdk = SDK(True)

    # STAŁE
    kolor1 = 'rgb(0,91,247)'
    kolor2 = 'rgb(75,200,230)'
    kolor3 = 'rgb(98,106,245)'
    alert = 'rgb(245,112,110)'
    wiodacy = 'rgb(160,211,247)'

    client = Elasticsearch("http://34.116.131.198:9200", basic_auth=("elastic", "lKunlGRVLiW1zWq9sQ6i"))
    opendata_url = 'https://opendata:5001'
    jasper_url = "https://34.116.131.198:10094"
    hdfs = PyWebHdfsClient(host='datahub', port='9870', user_name='nazca')

    # PRZYGOTOWANIE
    today = date.today()
    start = str(today + pd.DateOffset(days=7 * (-1))).replace(' ', 'T') + 'Z'
    stop = str(today + pd.DateOffset(seconds=(-1))).replace(' ', 'T') + 'Z'
    start_date = int((datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1000))
    stop_date = int((datetime.strptime(stop, "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1000))

    # DETALE
    param = {"size": 0, "query": {"bool": {
        "filter": [{"range": {"startTime": {"gte": start_date, "lte": stop_date, "format": "epoch_millis"}}},
                   {"query_string": {"analyze_wildcard": True, "query": "module:II"}}]}}, "aggs": {"2": {
        "date_histogram": {"field": "startTime", "min_doc_count": 0,
                           "extended_bounds": {"min": start_date, "max": stop_date}, "format": "epoch_millis",
                           "interval": "1d"}, "aggs": {}}}}
    resp = client.search(index="events", body=param)

    x = []
    y = []

    for hit in resp['aggregations']['2']['buckets']:
        y.append(hit['doc_count'])
        x.append(datetime.strptime(datetime.fromtimestamp(hit['key'] / 1000).strftime("%d-%m-%Y"), '%d-%m-%Y'))

    srednia = np.mean(y)
    y = np.array(y)
    x = np.array(x)
    x_up = x[[i for i in range(len(y)) if y[i] >= srednia]]
    x_down = x[[i for i in range(len(y)) if y[i] < srednia]]
    y_up = y[[i for i in range(len(y)) if y[i] >= srednia]]
    y_down = y[[i for i in range(len(y)) if y[i] < srednia]]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=x_up, y=y_up, text=y_up, textfont=dict(color='green'), textposition='outside', marker_color=kolor1,
               showlegend=False))
    fig.add_trace(
        go.Bar(x=x_down, y=y_down, text=y_down, textfont=dict(color=alert), textposition='outside', marker_color=alert,
               showlegend=False))
    # fig.add_trace(go.Scatter(x=[x[0],x[-1]],y=[srednia,srednia],mode='lines',line = dict(color='rgb(0,255,0)', width=4, dash='dash'), showlegend = False,marker_color='rgb(0,91,247)'))
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    fig.update_layout(title=dict(text='Liczba wyprodukowanych detali', xanchor='center', x=0.5),
                      xaxis_tickformat='%d-%m<br>%Y', font=dict(size=32, color='black'))

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=False)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=False, autorange=False,
                     range=[0, max(y) + 0.2 * max(y)])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.add_hline(y=srednia, line_color='black', line_width=4, line_dash='dash')
    fig.write_image("/internal/reports/detale.png", format='png', engine='kaleido', width=1800, height=800)
    logger.info('WYKRES ZAPISANY')
    # JASPER
    payload = {'j_username': 'jasperadmin', 'j_password': 'jasperadmin'}
    response = requests.get(f'''{jasper_url}/jasperserver/rest_v2/reports/reports/Energy.pdf''', payload, verify=False)
    logger.info(response.status_code)
    with open('/internal/reports/test.pdf', 'wb') as f:
        f.write(response.content)
    # model = hdfs.read_file("reports/sample.pdf")
    hdfs.create_file('reports/test11.pdf', file_data=response.content, overwrite=True)
    my_data = "b'01010101010101010101010101010101'"
    hdfs.create_file('reports/testy.txt', my_data, overwrite=True)