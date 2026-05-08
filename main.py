from fastapi import FastAPI
from pydantic import BaseModel
from math import sqrt


app = FastAPI()

# BASE TEMPORAL
reportes = []
usuarios = []

# MODELO
class Reporte(BaseModel):
    tipo: str
    latitud: float
    longitud: float

# GUARDAR REPORTE
@app.post("/reportar")
def reportar(reporte: Reporte):

    reportes.append(reporte)

    return {
        "mensaje": "Reporte guardado",
        "total": len(reportes)
    }

# OBTENER REPORTES
@app.get("/reportes")
def obtener_reportes():

    return reportes


@app.get("/ruta_segura")
def ruta_segura(
    origen_lat: float,
    origen_lon: float,
    destino_lat: float,
    destino_lon: float
):

    ruta = []

    # PUNTO INICIAL
    ruta.append({
        "lat": origen_lat,
        "lon": origen_lon
    })

    # EVITAR ZONAS PELIGROSAS
    for reporte in reportes:

        distancia = sqrt(
            (reporte.latitud - origen_lat) ** 2 +
            (reporte.longitud - origen_lon) ** 2
        )

        # SI HAY RIESGO CERCA
        if distancia < 0.001:

            # DESVIAR RUTA
            ruta.append({
                "lat": reporte.latitud + 0.001,
                "lon": reporte.longitud + 0.001
            })

    # DESTINO FINAL
    ruta.append({
        "lat": destino_lat,
        "lon": destino_lon
    })

    return ruta

@app.post("/registro")
def registro(usuario: dict):

    usuarios.append(usuario)

    return {
        "mensaje": "Usuario registrado"
    }


@app.post("/login")
def login(usuario: dict):

    for u in usuarios:

        if (
            u["username"] == usuario["username"]
            and
            u["password"] == usuario["password"]
        ):

            return {
                "success": True
            }

    return {
        "success": False
    }