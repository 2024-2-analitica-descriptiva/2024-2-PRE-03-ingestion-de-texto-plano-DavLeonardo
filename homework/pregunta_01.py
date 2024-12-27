"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    ruta = "files/input/clusters_report.txt"

    with open(ruta, "r") as file:
        lineas = file.readlines()

    aux = []
    current_keywords = ""
    for linea in lineas[4:]:
        if linea.strip():

            if linea[:5].strip().isdigit():

                if current_keywords:
                    aux[-1][-1] += f" {current_keywords.strip()}"
                    current_keywords = ""

                cluster = linea[:5].strip()
                cantidad = linea[5:20].strip()
                porcentaje = linea[20:40].strip()
                keywords = linea[40:].strip()
                aux.append([cluster, cantidad, porcentaje, keywords])
            else:

                current_keywords += f" {linea.strip()}"

    if current_keywords:
        aux[-1][-1] += f" {current_keywords.strip()}"

    data = pd.DataFrame(
        aux,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )

    data["cluster"] = (
        pd.to_numeric(data["cluster"], errors="coerce").fillna(0).astype(int)
    )
    data["cantidad_de_palabras_clave"] = (
        pd.to_numeric(data["cantidad_de_palabras_clave"], errors="coerce")
        .fillna(0)
        .astype(int)
    )
    data["porcentaje_de_palabras_clave"] = (
        data["porcentaje_de_palabras_clave"]
        .str.replace(",", ".")
        .str.rstrip("%")
        .astype(float)
    )

    data["principales_palabras_clave"] = (
        data["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r",\s+", ", ", regex=True)
        .str.strip()
        .str.rstrip(".")
    )

    data.columns = [col.lower().replace(" ", "_") for col in data.columns]

    return data
