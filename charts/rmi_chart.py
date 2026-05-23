import plotly.graph_objects as go

def add_rmi(fig, data, rows):

    rmi_data = data.dropna(subset=["RMI"])

    fig.add_trace(
        go.Scatter(
            x=rmi_data.index,
            y=rmi_data["RMI"],
            mode="lines",
            name="RMI",
            line=dict(
                color="#3b82f6",
                width=3
            ),
            fill="tozeroy"
        ),
        row=rows,
        col=1
    )

    fig.add_hrect(
        y0=70,
        y1=100,
        fillcolor="red",
        opacity=0.08,
        line_width=0,
        row=rows,
        col=1
    )

    # Oversold zone
    fig.add_hrect(y0=0,y1=30,fillcolor="green",opacity=0.08,line_width=0,row=rows,col=1)

    # Reference lines
    fig.add_hline(y=70,line_dash="dash",line_color="red",row=rows,col=1)
    fig.add_hline(y=30,line_dash="dash",line_color="green",row=rows,col=1)
    fig.add_hline(y=50,line_dash="dot",line_color="gray",row=rows,col=1)
    fig.update_yaxes(range=[0, 100],row=rows,col=1)