import pandas as pd
import sys
import os
import json
import re

# Importar desde el mismo directorio Business
from json_parser import extraer_y_aplanar_audit_data, obtener_campos_unicos, normalizar_registro

def extraer_correlation_id_desde_json_parcial(json_string):
    """Extraer CorrelationId desde solo la parte inicial del JSON"""
    
    if not json_string or json_string == 'N/A':
        return 'N/A'
    
    try:
        # Limpiar JSON: reemplazar comillas dobles por simples
        json_limpio = json_string.replace('""', '"')
        
        # Remover comillas del inicio y final si existen
        if json_limpio.startswith('"') and json_limpio.endswith('"'):
            json_limpio = json_limpio[1:-1]
        
        # Buscar AppAccessContext usando regex para extraer solo esa parte
        pattern = r'"AppAccessContext":\s*\{[^}]*"CorrelationId":\s*"([^"]+)"'
        match = re.search(pattern, json_limpio)
        
        if match:
            correlation_id = match.group(1)
            return correlation_id
        
        # Si no encuentra con regex, intentar parsear solo hasta donde se pueda
        # Buscar el inicio de AppAccessContext
        start_pos = json_limpio.find('"AppAccessContext":')
        if start_pos != -1:
            # Buscar el inicio del objeto AppAccessContext
            brace_start = json_limpio.find('{', start_pos)
            if brace_start != -1:
                # Contar llaves para encontrar el cierre
                brace_count = 0
                for i in range(brace_start, min(brace_start + 200, len(json_limpio))):
                    if json_limpio[i] == '{':
                        brace_count += 1
                    elif json_limpio[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            # Encontramos el cierre del AppAccessContext
                            app_context_json = json_limpio[brace_start:i+1]
                            try:
                                app_context_dict = json.loads(app_context_json)
                                if 'CorrelationId' in app_context_dict:
                                    return app_context_dict['CorrelationId']
                            except:
                                pass
                            break
        
        return 'N/A'
        
    except Exception as e:
        return 'N/A'

def extraer_usuarios_sharepoint_system(archivo_csv, num_filas=5):
    """
    Extrae campos específicos del CSV para USUARIOS SHAREPOINT SYSTEM
    
    CAMPOS ESPECÍFICOS PARA SHAREPOINT SYSTEMS:
    1. Campos base del CSV (5): RecordId, CreationDate, RecordType, Operation, UserId
    2. Campos básicos del JSON: CorrelationId, EventSource, GeoLocation, ItemType, etc.
    3. Campos finales del CSV (2): AssociatedAdminUnits, AssociatedAdminUnitsNames
    
    Args:
        archivo_csv (str): Ruta al archivo CSV fuente
        num_filas (int): Número de filas a procesar
        
    Returns:
        tuple: (lista_registros_normalizados, campos_unicos)
    """
    print(f"USUARIOS SHAREPOINT SYSTEM - Leyendo archivo CSV: {archivo_csv}")
    print("=" * 80)
    
    # Leer el archivo CSV
    df = pd.read_csv(
        archivo_csv,
        encoding='utf-8',
        sep=',',
        quotechar='"',
        escapechar='\\'
    )
    
    print(f"Total de filas en el archivo: {len(df)}")
    print(f"Columnas del CSV: {list(df.columns)}")
    
    # Filtrar solo usuarios SharePoint system
    usuarios_sharepoint = df[df['UserId'].str.contains('SHAREPOINT', case=False, na=False)]
    
    print(f"Usuarios SharePoint system encontrados: {len(usuarios_sharepoint)}")
    
    # Tomar las primeras x filas de usuarios SharePoint
    filas_a_revisar = usuarios_sharepoint.head(num_filas)
    
    print(f"Procesando {len(filas_a_revisar)} usuarios SharePoint system...")
    print("=" * 80)
    
    # Lista para almacenar resultados
    lista_registros = []
    
    # Procesar cada fila
    for i, (index, row) in enumerate(filas_a_revisar.iterrows(), 1):
        print(f"Procesando usuario SharePoint {i}/{len(filas_a_revisar)}: {row.get('UserId', 'N/A')}")
        
        # BLOQUE 1: Campos base del CSV (5 campos)
        registro = {
            'RecordId': row.get('RecordId', 'N/A'),
            'CreationDate': row.get('CreationDate', 'N/A'),
            'RecordType': row.get('RecordType', 'N/A'),
            'Operation': row.get('Operation', 'N/A'),
            'UserId': row.get('UserId', 'N/A'),
        }
        
        # BLOQUE 2: Solo CorrelationId desde AppAccessContext (columna F)
        audit_data = row.get('AuditData', 'N/A')
        
        if pd.notna(audit_data) and audit_data != 'N/A':
            correlation_id = extraer_correlation_id_desde_json_parcial(str(audit_data))
        else:
            correlation_id = 'N/A'
        
        # Agregar solo CorrelationId (columna F)
        registro['CorrelationId'] = correlation_id
        
        # BLOQUE 3: Campos finales del CSV (2 campos)
        registro['AssociatedAdminUnits'] = row.get('AssociatedAdminUnits', 'N/A')
        registro['AssociatedAdminUnitsNames'] = row.get('AssociatedAdminUnitsNames', 'N/A')
        
        # Agregar a la lista
        lista_registros.append(registro)
        
        print(f"   Total de campos en este registro: {len(registro)}")
        print(f"Usuario SharePoint {i} procesado correctamente")
    
    print(f"\n{'=' * 80}")
    print(f"Extraccion usuarios SharePoint system completada: {len(lista_registros)} registros procesados")
    
    # Obtener todos los campos únicos de todos los registros
    campos_unicos = obtener_campos_unicos(lista_registros)
    print(f"Total de campos únicos encontrados: {len(campos_unicos)}")
    print(f"{'=' * 80}")
    
    # Normalizar todos los registros para que tengan los mismos campos
    print("\nNormalizando registros de usuarios SharePoint system...")
    registros_normalizados = []
    for registro in lista_registros:
        registro_normalizado = normalizar_registro(registro, campos_unicos)
        registros_normalizados.append(registro_normalizado)
    
    print("Registros de usuarios SharePoint system normalizados")
    
    return registros_normalizados, campos_unicos

def mostrar_resumen_usuarios_sharepoint_system(campos_unicos):
    """
    Muestra un resumen organizado de los campos encontrados para usuarios SharePoint system
    
    Args:
        campos_unicos (list): Lista de campos únicos
    """
    print("\n" + "=" * 80)
    print("RESUMEN DE CAMPOS - USUARIOS SHAREPOINT SYSTEM")
    print("=" * 80)
    
    # Identificar campos por bloques
    campos_base = ['RecordId', 'CreationDate', 'RecordType', 'Operation', 'UserId']
    campos_finales = ['AssociatedAdminUnits', 'AssociatedAdminUnitsNames']
    campos_json_sharepoint = [c for c in campos_unicos 
                             if c not in campos_base 
                             and c not in campos_finales]
    
    print(f"\nBLOQUE 1 - Campos Base del CSV ({len(campos_base)} campos):")
    for campo in campos_base:
        if campo in campos_unicos:
            print(f"   {campo}")
    
    print(f"\nBLOQUE 2 - Campos del JSON AuditData ({len(campos_json_sharepoint)} campos):")
    for campo in sorted(campos_json_sharepoint):
        print(f"   {campo}")
    
    print(f"\nBLOQUE 3 - Campos Finales del CSV ({len(campos_finales)} campos):")
    for campo in campos_finales:
        if campo in campos_unicos:
            print(f"   {campo}")
    
    print(f"\n{'=' * 80}")
    print(f"TOTAL USUARIOS SHAREPOINT SYSTEM: {len(campos_unicos)} columnas en el Excel final")
    print("=" * 80)
