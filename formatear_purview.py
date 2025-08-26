# formatear_purview.py — versión robusta: aplanado de JSON (AuditData / AppAccessContext) + Excel
import pandas as pd
import json
import pytz
from pathlib import Path

CSV_IN = "simple.csv"            # <— cambia si tu archivo tiene otro nombre
XLSX_OUT = Path(CSV_IN).with_suffix(".limpio.xlsx")

# ============ utilidades básicas ============

def read_csv_safely(path: str) -> pd.DataFrame:
    """
    Lee el CSV intentando UTF-8-SIG y UTF-8 con separador coma.
    No restringe columnas y normaliza encabezados (quita BOM/espacios).
    """
    last_err = None
    for enc in ("utf-8-sig", "utf-8"):
        try:
            df = pd.read_csv(
                path,
                encoding=enc,
                sep=",",
                engine="python",
                dtype=str,
                on_bad_lines="skip",
            )
            df.columns = [c.strip().lstrip("\ufeff") for c in df.columns]
            return df
        except Exception as e:
            last_err = e
    raise last_err

def looks_like_json(s: str) -> bool:
    if not isinstance(s, str):
        return False
    s = s.strip()
    return (len(s) >= 2) and ((s[0] == "{" and s[-1] == "}") or (s[0] == "[" and s[-1] == "]"))

def safe_json_load(s):
    """
    Convierte string JSON a dict/list. Si no es JSON válido, devuelve {}.
    """
    if not isinstance(s, str):
        return {}
    s = s.strip()
    if not looks_like_json(s):
        return {}
    try:
        return json.loads(s)
    except Exception:
        # segundo intento con pequeñas reparaciones
        try:
            return json.loads(s.replace("\r\n", "\n"))
        except Exception:
            return {}

def expand_one_json_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Aplana una columna JSON (dict/list) y crea columnas prefijadas con 'col.'.
    Mantiene la columna original también (para referencia).
    """
    parsed = df[col].apply(safe_json_load)

    # Pasar todo a dicts para pd.json_normalize
    normalized_input = []
    for v in parsed:
        if isinstance(v, dict):
            normalized_input.append(v)
        elif isinstance(v, list):
            normalized_input.append({"_list": v})
        else:
            normalized_input.append({})

    if not any(normalized_input):
        # Nada que aplanar
        return df

    jdf = pd.json_normalize(normalized_input, max_level=6)
    # Prefijar
    jdf.columns = [f"{col}.{c}" for c in jdf.columns]
    # Concatenar
    return pd.concat([df, jdf], axis=1)

def expand_all_json_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detecta automáticamente columnas que contengan JSON y las aplana.
    Fuerza el intento en 'AuditData' y 'AppAccessContext' si existen.
    """
    df = df.copy()

    # Candidatas por heurística (>10% de valores con pinta de JSON)
    candidates = set()
    for c in df.columns:
        ser = df[c].dropna().astype(str)
        if not ser.empty:
            ratio = ser.str.strip().apply(looks_like_json).mean()
            if ratio > 0.10:
                candidates.add(c)

    # Forzar intento sobre estas si existen
    for force_col in ("AuditData", "AppAccessContext"):
        if force_col in df.columns:
            candidates.add(force_col)

    # Aplanar cada una
    for c in sorted(candidates):
        try:
            df = expand_one_json_column(df, c)
        except Exception:
            # no fallamos el proceso completo por una columna problemática
            pass

    # Caso especial: si 'AuditData' traía dentro otro objeto 'AppAccessContext',
    # tras expandir 'AuditData' tendrás 'AuditData.AppAccessContext.*'.
    # Si además existe una columna de texto 'AppAccessContext', ya quedó expandida aparte.
    return df

def add_fecha_local(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea 'FechaLocal' (America/Santiago) desde alguna columna UTC-like:
    CreationTime, CreationDate, AuditData.CreationTime, etc.
    """
    df = df.copy()
    cand = []

    # candidatos obvios
    for c in df.columns:
        lc = c.lower()
        if lc in {"creationtime", "creationdate", "fechautc"}:
            cand.append(c)

    # si no, heurística
    if not cand:
        for c in df.columns:
            lc = c.lower()
            if ("creation" in lc and ("time" in lc or "date" in lc)) or lc.endswith("utc"):
                cand.append(c)

    # intenta sobre el primero que funcione
    cl = pytz.timezone("America/Santiago")
    for base in cand:
        ts = pd.to_datetime(df[base], utc=True, errors="coerce")
        if ts.notna().any():
            try:
                df["FechaLocal"] = ts.dt.tz_convert(cl).dt.strftime("%Y-%m-%d %H:%M:%S")
                return df
            except Exception:
                continue
    return df

def best_sort(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ordena, si es posible, por una fecha razonable.
    """
    for candidate in ["CreationTime", "CreationDate", "AuditData.CreationTime", "FechaUTC"]:
        if candidate in df.columns:
            try:
                return df.sort_values(candidate, ascending=False, na_position="last")
            except Exception:
                pass
    return df

# ============ pipeline ============

def main():
    df = read_csv_safely(CSV_IN)

    if df.empty:
        raise SystemExit("El CSV se leyó pero no tiene filas. Revisa filtros en la exportación.")

    # Aplanar todas las columnas que contengan JSON (incluye AuditData / AppAccessContext)
    df = expand_all_json_columns(df)

    # Campos "útiles" derivados (opcionales): IP/Usuario/Actividad/Workload/UA/CorrelationId
    # Intentamos buscarlos tanto "planos" como salidos del JSON expandido.
    def pick(*names):
        for n in names:
            if n in df.columns:
                return df[n]
        return pd.Series([pd.NA] * len(df))

    # Construimos una tabla "principal" sin perder el resto de columnas aplanadas
    principal = pd.DataFrame({
        "FechaUTC": pick("CreationTime", "CreationDate", "AuditData.CreationTime"),
        "Usuario": pick("UserId", "AuditData.UserId"),
        "DireccionIP": pick("ClientIP", "ClientIp", "AuditData.ClientIP", "AuditData.ClientIp"),
        "Tipo registro": pick("RecordType", "AuditData.RecordType"),
        "Actividad": pick("Operation", "AuditData.Operation"),
        "Workload": pick("Workload", "AuditData.Workload"),
        "Resultado": pick("ResultStatus", "AuditData.ResultStatus"),
        "UserAgent": pick("UserAgent", "AuditData.UserAgent"),
        "CorrelationId": pick("CorrelationId", "AuditData.CorrelationId"),
    })

    # Agregar FechaLocal (si se puede inferir)
    principal = pd.concat([principal, add_fecha_local(principal).get("FechaLocal")], axis=1)

    # Unimos: primero campos principales y luego TODAS las columnas originales + expandidas
    # (sin duplicar nombres ya presentes en 'principal')
    rest_cols = [c for c in df.columns if c not in principal.columns]
    out = pd.concat([principal, df[rest_cols]], axis=1)

    # Orden sugerido de columnas "clave" al inicio
    preferred_order = [
        "FechaUTC", "FechaLocal", "DireccionIP", "Usuario",
        "Tipo registro", "Actividad", "Workload", "Resultado",
        "UserAgent", "CorrelationId",
    ]
    # Reordenar: primero las preferidas (las que existan), luego el resto
    ordered = [c for c in preferred_order if c in out.columns] + \
              [c for c in out.columns if c not in preferred_order]

    out = out[ordered]
    out = best_sort(out)

    # Exportar a Excel
    out.to_excel(XLSX_OUT, index=False)
    print(f"[✓] Generado: {XLSX_OUT.resolve()}")

if __name__ == "__main__":
    main()
