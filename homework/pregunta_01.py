# pylint: disable=line-too-long
"""
Escriba el código que ejecute la accion solicitada.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Ruta de salida
OUTPUT_DIR = "docs"


def load_data():
    """Carga el archivo CSV con la información de envíos."""
    path = "files/input/shipping-data.csv"
    return pd.read_csv(path)


def ensure_output_directory():
    """Crea la carpeta de salida si no existe."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_visual_for_shipping_per_warehouse(df):
    """Gráfico de barras: envíos por bloque de bodega."""
    plt.figure()
    counts = df.Warehouse_block.value_counts()
    counts.plot.bar(
        title="Shipping per Warehouse",
        xlabel="Warehouse block",
        ylabel="Record Count",
        color="tab:blue",
        fontsize=8,
    )

    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.savefig(os.path.join(OUTPUT_DIR, "shipping_per_warehouse.png"), dpi=300)
    plt.close()


def create_visual_for_mode_of_shipment(df):
    """Gráfico de torta: proporción de modos de envío."""
    plt.figure()
    counts = df.Mode_of_Shipment.value_counts()
    counts.plot.pie(
        title="Mode of shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"],
    )

    plt.savefig(os.path.join(OUTPUT_DIR, "mode_of_shipment.png"), dpi=300)
    plt.close()


def create_visual_for_average_customer_rating(df):
    """Gráfico de barras horizontales: calificación promedio del cliente por modo de envío."""
    plt.figure()
    summary = (
        df[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    summary.columns = summary.columns.droplevel()
    summary = summary[["mean", "min", "max"]]

    # Fondo gris de rango min-max
    plt.barh(
        y=summary.index,
        width=summary["max"] - 1,
        left=summary["min"],
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )

    # Barra central de media
    colors = ["tab:green" if val >= 3.0 else "tab:orange" for val in summary["mean"]]
    plt.barh(
        y=summary.index,
        width=summary["mean"] - 1,
        left=summary["min"],
        color=colors,
        height=0.5,
        alpha=1.0,
    )

    plt.title("Average Customer Rating")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("gray")
    ax.spines["bottom"].set_color("gray")

    plt.savefig(os.path.join(OUTPUT_DIR, "average_customer_rating.png"), dpi=300)
    plt.close()


def create_visual_for_weight_distribution(df):
    """Histograma: distribución de peso de los envíos."""
    plt.figure()
    df.Weight_in_gms.plot.hist(
        title="Shipped Weight Distribution",
        color="tab:orange",
        edgecolor="white",
    )

    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.savefig(os.path.join(OUTPUT_DIR, "weight_distribution.png"), dpi=300)
    plt.close()


def create_html_dashboard():
    """Genera el archivo HTML estático con el dashboard."""
    html = """<!DOCTYPE html>
<html>
    <body>
        <h1>Shipping Dashboard Example</h1>
        <div style="width: 45%; float: left;">
            <img src="shipping_per_warehouse.png" alt="Shipping per Warehouse">
            <img src="mode_of_shipment.png" alt="Mode of Shipment">
        </div>
        <div style="width: 45%; float: right;">
            <img src="average_customer_rating.png" alt="Customer Rating">
            <img src="weight_distribution.png" alt="Weight Distribution">
        </div>
    </body>
</html>"""
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(html)


def pregunta_01():
    """
    Crea un dashboard HTML con visualizaciones de:

    - Warehouse_block
    - Mode_of_Shipment
    - Customer_rating
    - Weight_in_gms

    Guarda todos los gráficos y el HTML en la carpeta `docs`.
    """
    ensure_output_directory()
    df = load_data()

    create_visual_for_shipping_per_warehouse(df)
    create_visual_for_mode_of_shipment(df)
    create_visual_for_average_customer_rating(df)
    create_visual_for_weight_distribution(df)
    create_html_dashboard()


# Ejecutar si se corre directamente
if __name__ == "__main__":
    pregunta_01()

    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """