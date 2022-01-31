import dash
from dash import dcc, html, Input, Output, no_update
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

data_path = 'cross_validation_10fold_evaluation.csv'

df = pd.read_csv(data_path)
df = df.sort_values(by="Label")

colors = {
    'background': '#FFFAFA',
    'text': '#000000'
}

fig = go.Figure(data=[
    go.Scatter(
        x=df["Label"],
        y=df["EV"],
        mode="markers",
        marker=dict(
            colorscale='plasma',
            color=df["EV"],
            size=12,
            line=dict(width=0.7, color='Black'),
            colorbar={"title": "Explained<br>Variance"},
            reversescale=True,
            opacity=0.8,
        )
    )
])

# turn off native plotly.js hover effects - make sure to use
# hoverinfo="none" rather than "skip" which also halts events.
fig.update_traces(hoverinfo="none", hovertemplate=None)

fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

fig.update_layout(
    xaxis=dict(title='ROI', showticklabels=False),
    yaxis=dict(title='Explained Variance (EV)', showgrid=True),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    autosize=False,
    width=1600,
    height=800
)

app = dash.Dash(__name__)

server = app.server

app.title = 'Explained Variance in Full Controls Test Set (10 fold resampling)'

app.layout = html.Div([
    dcc.Graph(id="graph", figure=fig, clear_on_unhover=True),
    dcc.Tooltip(id="graph-tooltip"),
])


@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("graph", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    # demo only shows the first point, but other points may also be available
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = df.iloc[num]
    img_src = df_row['IMG_URL']
    name = df_row['Label']
    ev = "Explained Variance = " + df_row['EV'].round(3).astype(str)


    children = [
        html.Div(children=[
            html.Img(src=img_src, style={"width": "100%"}),
            html.H2(f"{name}", style={"color": "darkblue"}),
            html.P(f"{ev}"),
        ],
        style={'width': '350px', 'white-space': 'normal'})
    ]

    return True, bbox, children


if __name__ == "__main__":
    app.run_server(debug=True)
