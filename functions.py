def env_data():

    import pandas as pd
    import plotly
    from plotly.subplots import make_subplots
    import plotly.graph_objs as go
    import json
    import thingspeak

    ch = thingspeak.Channel(1880870)

    df = pd.DataFrame(json.loads(ch.get({'results': 24*60*60/30*3}))['feeds'])
    df.columns = ['time','entry_id','temperature', 'humidity', 'pressure']
    df = df.dropna()
    df = df[df["humidity"].str.contains("nan") == False]
    df = df[df["temperature"].str.contains("nan") == False]
    df = df[df["pressure"].str.contains("nan") == False]

    df['time'] = pd.to_datetime(df['time'])

    df['temperature'] = pd.to_numeric(df['temperature'])
    df['humidity'] = pd.to_numeric(df['humidity'])
    df['pressure'] = pd.to_numeric(df['pressure'])

    df['temperature'] = df['temperature'].rolling(20,min_periods=1).mean()
    df['humidity'] = df['humidity'].rolling(20,min_periods=1).mean()

    #df = pd.read_csv("app/data/evn_data.csv",  names=cnames,index_col=False)
    #df["time"] = [datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')+ timedelta(hours = 2) for x in df["time"]]
    fig = make_subplots(rows=1, cols=3,
                        shared_yaxes=False,
                        horizontal_spacing = 0.1
                        #vertical_spacing=0.02,
                        #subplot_titles=("Temperature","Humidity", "Pressure")
                        )

    trace1 = go.Scatter(
        x=df['time'],
        y=df['temperature'],
        name = "Temperature",
        marker_color = 'white',
        marker_line_width=8,
        )
    trace2 = go.Scatter(
        x=df['time'],
        y=df['humidity'],
        name = "Humidity",
        marker_color = 'white',
        marker_line_width=8,
        )
    trace3 = go.Scatter(
        x=df['time'],
        y=df['pressure'],
        name = "Pressure",
        marker_color = 'white',
        marker_line_width=8)
    
    fig.add_trace(trace1,
                    row=1, col=1)
    fig.add_trace(trace2,
                    row=1, col=2)
    fig.add_trace(trace3,
                    row=1, col=3)
    
    fig.update_layout(
        width=1150, 
        height=250, 
        showlegend=False,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white",
        font_size=16,
        margin=dict(
            l=1,
            r=5,
            b=0,
            t=0,
            pad=0
        ),
        annotations=[
        dict(
            x=list(df['time'])[-1], y=list(df['humidity'])[-1], # annotation point
            xref='x2', 
            yref='y2',
            text=str(int(list(df['humidity'])[-1])),
            showarrow=True,
            arrowhead=7,
            arrowcolor="white",
            arrowwidth = 2,
            ax=0,
            ay=-70,
            arrowsize=0.3,
            standoff = 10,
            font = dict(size = 18, family="Arial Black")
        ),
        dict(
            x=list(df['time'])[-1], y=list(df['temperature'])[-1], # annotation point
            xref='x1', 
            yref='y1',
            text=str(round(list(df['temperature'])[-1],1)),
            showarrow=True,
            arrowhead=7,
            arrowcolor="white",
            arrowwidth = 2,
            ax=0,
            ay=-70,
            arrowsize=0.3,
            standoff = 10,
            font = dict(size = 18, family="Arial Black")
        ),
        dict(
            x=list(df['time'])[-1], y=list(df['pressure'])[-1], # annotation point
            xref='x3', 
            yref='y3',
            text=str(int(list(df['pressure'])[-1])),
            showarrow=True,
            arrowhead=7,
            arrowcolor="white",
            arrowwidth = 2,
            ax=0,
            ay=-70,
            arrowsize=0.3,
            standoff = 10,
            font = dict(size = 18, family="Arial Black")
        )
        ]
        )
    fig.update_traces(line=dict(color="white", width=5)
            
        )
    fig.for_each_xaxis(lambda x: x.update(showgrid=True, linecolor="white"))
    fig.for_each_yaxis(lambda x: x.update(showgrid=False,linecolor="white"))
    fig.update_xaxes(tickfont_family="Arial Black")
    fig.update_xaxes(tickformat="%d.%m")
    #fig["layout"]['xaxis3']['linecolor']="white"
    fig["layout"]['yaxis']['title'] = 'Temperature [°C]'
    fig["layout"]['yaxis']['title']["standoff"]= 20
    fig["layout"]['yaxis2']['title'] = 'Humidiy [%]'
    fig["layout"]['yaxis2']['title']["standoff"]= 5
    fig["layout"]['yaxis3']['title'] = 'Pressure [hPa]'
    fig["layout"]['yaxis3']['title']["standoff"]= 5

    


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def news():
    import feedparser
    from bs4 import BeautifulSoup
    feed = feedparser.parse('https://www.tagesschau.de/xml/rss2')
    result = []
    for entry in feed.entries:
        try:
            html = BeautifulSoup(entry.content[0]['value'])
            result.append(
                {
                "title": entry.title,
                "summary": entry['summary'],
                "image" : html.find_all('img')[0]
                }
            )
        except:
            result.append(
                {
                "title": entry.title,
                "summary": entry['summary'],
                "image" : ""
                }
            )
    return(result)
