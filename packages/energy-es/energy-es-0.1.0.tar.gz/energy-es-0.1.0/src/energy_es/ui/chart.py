"""Energy-ES - User Interface - Chart."""

from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from userconf import UserConf

from energy_es.data.prices import PricesManager


# UserConf application ID
UC_APP_ID = "energy_es"

MESSAGE_HTML = (
    '<!DOCTYPE html>'
    '<html>'
    '<head>'
    '</head>'
    '<body>'
    '<div style="font-family: sans-serif; font-weight: bold;">{{TITLE}}</div>'
    '<p>{{MESSAGE}}</p>'
    '</body>'
    '</html>'
)


def get_message_html(title: str, message: str = "") -> str:
    """Return a message HTML code.

    :param title: Title.
    :param message: Message.
    :return: HTML code.
    """
    return (
        MESSAGE_HTML
        .replace("{{TITLE}}", title)
        .replace("{{MESSAGE}}", message)
    )


def _write_chart(unit: str, path: str):
    """Generate and write the chart HTML page with updated data.

    :param unit: Prices unit. It must be "k" to have the prices in €/kWh or "m"
    to have them in €/MWh.
    :param path: Destination file path.
    """
    # Get data
    pm = PricesManager()
    prices = pm.get_prices(unit)

    updated = prices["updated"]
    price_unit = prices["price_unit"]
    data = prices["data"]

    # Title and source
    dt = datetime.fromtimestamp(updated).astimezone(ZoneInfo("Europe/Madrid"))
    dt = dt.strftime(f"%A {dt.day} %B %Y (%Z)")

    title = f"Electricity price ({price_unit}) in Spain for {dt}"
    source = "Data source: Red Eléctrica de España"

    # Create dataframe
    prices_df = pd.DataFrame(data)

    text = ["<b>MIN</b>", "<b>MAX</b>"]
    text_pos = ["bottom center", "top center"]

    for c in ("spot_market", "pvpc_pcb", "pvpc_cm"):
        cond = [
            prices_df[c] == prices_df[c].min(),
            prices_df[c] == prices_df[c].max()
        ]

        prices_df[f"{c}_text"] = np.select(cond, text, default=None)

        prices_df[f"{c}_text_position"] = (
            np.select(cond, text_pos, default="top center")
        )

    # Create chart
    fig = go.Figure()

    fig.update_layout(
        title={
            "text":
                f'{title}<br><span style="font-size: 14px">{source}</span>',
            "yref": "paper",
            "y": 1,
            "yanchor": "bottom",
            "pad": {"l": 77, "b": 40},
            "x": 0,
            "xanchor": "left"
        },
        plot_bgcolor="white",
        xaxis={
            "title": "Time",
            "fixedrange": True,
            "showline": True,
            "mirror": True,
            "linecolor": "black",
            "gridcolor": "lightgrey",
            "ticks": "outside",
            "tickangle": 45
        },
        yaxis={
            "title": price_unit,
            "fixedrange": True,
            "showline": True,
            "mirror": True,
            "linecolor": "black",
            "gridcolor": "lightgrey",
            "ticks": "outside"
        },
        legend={"itemdoubleclick": False},
        margin={"t": 65}
    )

    hover_tem = "Time: &nbsp;%{x}<br>Price: &nbsp;%{y} " + price_unit
    spot_hover_tem = "<b>Spot Market</b><br>" + hover_tem

    pvpc_pcb_hover_tem = (
        "<b>PVPC (Peninsula, Canarias and Baleares)</b><br>" + hover_tem
    )

    pvpc_cm_hover_tem = "<b>PVPC (Ceuta and Melilla)</b><br>" + hover_tem

    # Spot market prices
    spot_sca = go.Scatter(
        x=prices_df["time"],
        y=prices_df["spot_market"],
        mode="lines+markers+text",
        text=prices_df["spot_market_text"],
        line={"width": 3, "color": "#2077b4"},
        marker={"size": 12, "color": "#2077b4"},
        textposition=prices_df["spot_market_text_position"],
        textfont={"color": "#2077b4"},
        name="Spot Market price",
        hovertemplate=spot_hover_tem,
        hoverlabel={"namelength": 0}
    )

    # PVPC prices (Peninsula, Canarias and Baleares)
    pvpc_pcb_sca = go.Scatter(
        x=prices_df["time"],
        y=prices_df["pvpc_pcb"],
        mode="lines+markers+text",
        text=prices_df["pvpc_pcb_text"],
        line={"width": 3, "color": "#ff8c00"},
        marker={"size": 12, "color": "#ff8c00"},
        textposition=prices_df["pvpc_pcb_text_position"],
        textfont={"color": "#ff8c00"},
        name="PVPC price<br>(Peninsula, Canarias<br>and Baleares)",
        hovertemplate=pvpc_pcb_hover_tem,
        hoverlabel={"namelength": 0}
    )

    # PVPC prices (Ceuta and Melilla)
    pvpc_cm_sca = go.Scatter(
        x=prices_df["time"],
        y=prices_df["pvpc_cm"],
        mode="lines+markers+text",
        text=prices_df["pvpc_cm_text"],
        line={"width": 3, "color": "#00a002"},
        marker={"size": 12, "color": "#00a002"},
        textposition=prices_df["pvpc_cm_text_position"],
        textfont={"color": "#00a002"},
        name="<br>PVPC price<br>(Ceuta and Melilla)<br>",
        hovertemplate=pvpc_cm_hover_tem,
        hoverlabel={"namelength": 0}
    )

    fig.add_traces([spot_sca, pvpc_cm_sca, pvpc_pcb_sca])
    conf = {"displayModeBar": False}

    # Write chart
    fig.write_html(path, config=conf)


def get_chart_path(unit: str = "m") -> str:
    """Generate and write the chart HTML page with updated data and get its
    path.

    :param unit: Prices unit. It must be "k" to have the prices in €/kWh or "m"
    (default) to have them in €/MWh.
    :return: Absolute path of the chart file.
    """
    uc = UserConf(UC_APP_ID)

    path = uc.files.get_path("chart.html")
    _write_chart(unit, path)

    return path
