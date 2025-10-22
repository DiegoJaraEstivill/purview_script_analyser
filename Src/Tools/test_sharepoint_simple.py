#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST SIMPLE - Solo extractor SharePoint System
==============================================

Script simple para probar SOLO el extractor de SharePoint System
"""

import pandas as pd
import json
import os
import sys

# Agregar el directorio Business al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Business'))

def test_sharepoint_extractor():
    """Probar solo el extractor de SharePoint System"""
    
    print("TEST SIMPLE - EXTRACTOR SHAREPOINT SYSTEM")
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
    
    # Procesar las primeras 3 líneas SharePoint
    for i, (index, fila) in enumerate(sharepoint_lines.head(3).iterrows(), 1):
        num_linea = index + 1
        print(f"\n--- LINEA {num_linea} ---")
        
        # Columnas A-E (básicas)
        record_id = fila.get('RecordId', 'N/A')
        creation_date = fila.get('CreationDate', 'N/A')
        record_type = fila.get('RecordType', 'N/A')
        operation = fila.get('Operation', 'N/A')
        user_id = fila.get('UserId', 'N/A')
        
        print(f"A: RecordId = {record_id}")
        print(f"B: CreationDate = {creation_date}")
        print(f"C: RecordType = {record_type}")
        print(f"D: Operation = {operation}")
        print(f"E: UserId = {user_id}")
        
        # Columna F: CorrelationId desde AppAccessContext
        correlation_id = 'N/A'
        audit_data_raw = fila.get('AuditData', 'N/A')
        
        if pd.notna(audit_data_raw) and audit_data_raw != 'N/A':
            try:
                # Limpiar JSON: reemplazar comillas dobles por simples
                json_string = str(audit_data_raw)
                json_limpio = json_string.replace('""', '"')
                
                # Remover comillas del inicio y final si existen
                if json_limpio.startswith('"') and json_limpio.endswith('"'):
                    json_limpio = json_limpio[1:-1]
                
                # Parsear JSON
                audit_data_dict = json.loads(json_limpio)
                
                # Buscar CorrelationId en AppAccessContext
                if 'AppAccessContext' in audit_data_dict:
                    app_context = audit_data_dict['AppAccessContext']
                    if 'CorrelationId' in app_context:
                        correlation_id = app_context['CorrelationId']
                        print(f"F: CorrelationId = {correlation_id}")
                    else:
                        print(f"F: CorrelationId = N/A (no encontrado en AppAccessContext)")
                else:
                    print(f"F: CorrelationId = N/A (no hay AppAccessContext)")
                    
            except json.JSONDecodeError as e:
                print(f"F: CorrelationId = N/A (error JSON: {e})")
            except Exception as e:
                print(f"F: CorrelationId = N/A (error: {e})")
        else:
            print(f"F: CorrelationId = N/A (AuditData vacío)")

if __name__ == "__main__":
    test_sharepoint_extractor()
