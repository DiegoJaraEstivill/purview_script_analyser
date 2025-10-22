#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST SIMPLE - Extraer CorrelationId desde JSON parcial
======================================================

Script para extraer CorrelationId desde solo la parte inicial del JSON
"""

import pandas as pd
import json
import os
import sys
import re

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

def test_correlation_id_extraction():
    """Probar extracción de CorrelationId"""
    
    print("TEST CORRELATION ID EXTRACTION")
    print("=" * 50)
    
    # Leer CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_csv = os.path.join(script_dir, "..", "Data", "Input", "7000LineasTextoPlano.csv")
    archivo_csv = os.path.normpath(archivo_csv)
    
    df = pd.read_csv(
        archivo_csv,
        encoding='utf-8',
        sep=',',
        quotechar='"',
        escapechar='\\'
    )
    
    # Buscar usuarios SharePoint system
    sharepoint_lines = df[df['UserId'].str.contains('SHAREPOINT', case=False, na=False)]
    
    print(f"Usuarios SharePoint system encontrados: {len(sharepoint_lines)}")
    
    # Procesar las primeras 5 líneas SharePoint
    for i, (index, fila) in enumerate(sharepoint_lines.head(5).iterrows(), 1):
        num_linea = index + 1
        print(f"\n--- LINEA {num_linea} ---")
        
        # Columnas A-E (básicas)
        record_id = fila.get('RecordId', 'N/A')
        operation = fila.get('Operation', 'N/A')
        user_id = fila.get('UserId', 'N/A')
        
        print(f"A: RecordId = {record_id}")
        print(f"D: Operation = {operation}")
        print(f"E: UserId = {user_id}")
        
        # Columna F: CorrelationId desde AppAccessContext
        audit_data_raw = fila.get('AuditData', 'N/A')
        
        if pd.notna(audit_data_raw) and audit_data_raw != 'N/A':
            correlation_id = extraer_correlation_id_desde_json_parcial(str(audit_data_raw))
            print(f"F: CorrelationId = {correlation_id}")
        else:
            print(f"F: CorrelationId = N/A (AuditData vacío)")

if __name__ == "__main__":
    test_correlation_id_extraction()
