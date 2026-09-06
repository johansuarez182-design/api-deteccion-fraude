"""
API — Sistema de Detección de Fraude en Pagos
Expone como servicios web 3 de las consultas JOIN desarrolladas en la Parte 1.
"""

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

app = FastAPI(
    title="API — Sistema de Detección de Fraude",
    description="Expone consultas JOIN sobre el modelo de base de datos de fraude en pagos.",
    version="1.0.0",
)


@app.get("/")
def raiz():
    """Endpoint de salud básico: confirma que la API está corriendo."""
    return {"mensaje": "API de detección de fraude activa. Ver /docs para la documentación interactiva."}


# ---------------------------------------------------------------------
# Endpoint 1 — Consulta 1: INNER JOIN (transacciones con usuario/comercio)
# ---------------------------------------------------------------------
@app.get("/transacciones-detalle")
def transacciones_detalle(db: Session = Depends(get_db)):
    """
    Detalle de cada transacción con el titular de la cuenta y el comercio
    donde se realizó. Combina Transaccion, Cuenta, Usuario y Comerciante
    mediante INNER JOIN.
    """
    resultado = db.execute(text("""
        SELECT
            t.transaccion_id,
            u.nombre || ' ' || u.apellido AS titular,
            c.numero_cuenta,
            m.nombre_comercial AS comercio,
            t.monto,
            t.moneda,
            t.fecha_hora,
            t.tipo_transaccion,
            t.estado
        FROM Transaccion t
        INNER JOIN Cuenta      c ON t.cuenta_id      = c.cuenta_id
        INNER JOIN Usuario     u ON c.usuario_id     = u.usuario_id
        INNER JOIN Comerciante m ON t.comerciante_id = m.comerciante_id
        ORDER BY t.fecha_hora DESC
    """))
    return [dict(fila._mapping) for fila in resultado]


# ---------------------------------------------------------------------
# Endpoint 2 — Consulta 2: LEFT JOIN (alertas sin analista asignado)
# ---------------------------------------------------------------------
@app.get("/alertas-sin-asignar")
def alertas_sin_asignar(db: Session = Depends(get_db)):
    """
    Alertas de fraude que aún no han sido asignadas a ningún analista.
    Usa LEFT JOIN contra AlertaAnalista para detectar la ausencia de asignación.
    """
    resultado = db.execute(text("""
        SELECT
            a.alerta_id,
            a.nivel_severidad,
            a.estado,
            a.fecha_generacion,
            a.descripcion
        FROM Alerta a
        LEFT JOIN AlertaAnalista aa ON a.alerta_id = aa.alerta_id
        WHERE aa.analista_id IS NULL
        ORDER BY a.nivel_severidad DESC, a.fecha_generacion ASC
    """))
    return [dict(fila._mapping) for fila in resultado]


# ---------------------------------------------------------------------
# Endpoint 3 — Consulta 4: JOIN + GROUP BY/HAVING (comercios de score alto)
# ---------------------------------------------------------------------
@app.get("/comercios-riesgo-alto")
def comercios_riesgo_alto(db: Session = Depends(get_db)):
    """
    Comercios cuyo score de riesgo promedio en sus transacciones supera 50,
    candidatos a revisión manual o reclasificación de nivel_riesgo.
    """
    resultado = db.execute(text("""
        SELECT
            m.comerciante_id,
            m.nombre_comercial,
            m.nivel_riesgo,
            COUNT(t.transaccion_id)      AS num_transacciones,
            SUM(t.monto)                 AS monto_total,
            ROUND(AVG(t.score_riesgo),2) AS score_promedio
        FROM Transaccion t
        INNER JOIN Comerciante m ON t.comerciante_id = m.comerciante_id
        GROUP BY m.comerciante_id, m.nombre_comercial, m.nivel_riesgo
        HAVING AVG(t.score_riesgo) > 50
        ORDER BY score_promedio DESC
    """))
    return [dict(fila._mapping) for fila in resultado]
