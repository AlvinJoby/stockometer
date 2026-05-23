import pandas as pd

def calculate_rmi(data):
    length=14
    momentum=5
    data["diff_momentum"] = data["Close"]-data['Close'].shift(momentum)

    data["positive_momentum"] = data["diff_momentum"].where(data["diff_momentum"]>0,0)
    data["negative_momentum"] = -(data["diff_momentum"].where(data["diff_momentum"]<0,0))

    data["avg_gain_rmi"] = data["positive_momentum"].ewm(span=length,adjust=False).mean()
    data["avg_loss_rmi"] = data["negative_momentum"].ewm(span=length,adjust=False).mean()

    data["RMI"] = 100*(data["avg_gain_rmi"]/(data["avg_gain_rmi"]+data["avg_loss_rmi"]))

    data.drop(columns=[
    "diff_momentum",
    "positive_momentum",
    "negative_momentum",
    "avg_gain_rmi",
    "avg_loss_rmi"
    ], inplace=True)

    return data