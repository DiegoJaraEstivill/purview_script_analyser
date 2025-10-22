#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTRACTOR SIMPLE - Solo hasta columna F con CorrelationId
==========================================================

Script simple para extraer SOLO hasta la columna F:
A: RecordId
B: CreationDate  
C: RecordType
D: Operation
E: UserId
F: CorrelationId (desde AppAccessContext)
"""

import pandas as pd
import json
import os
import sys
import re

def limpiar_json_simple(json_string):
    """Limpia el JSON reemplazando comillas dobles por simples"""
    if not json_string or json_string == 'N/A':
        return None
    
    # Reemplazar comillas dobles por simples
    json_limpio = json_string.replace('""', '"')
    
    # Remover comillas del inicio y final si existen
    if json_limpio.startswith('"') and json_limpio.endswith('"'):
        json_limpio = json_limpio[1:-1]
    
    return json_limpio

def extraer_correlation_id_simple():
    """Extraer SOLO hasta columna F con CorrelationId"""
    
    print("EXTRACTOR SIMPLE - SOLO HASTA COLUMNA F")
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
    resultados = []
    
    for i, (index, fila) in enumerate(sharepoint_lines.head(5).iterrows(), 1):
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
            # Limpiar JSON
            json_limpio = limpiar_json_simple(str(audit_data_raw))
            
            if json_limpio:
                try:
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
                print(f"F: CorrelationId = N/A (JSON vacío)")
        else:
            print(f"F: CorrelationId = N/A (AuditData vacío)")
        
        # Guardar resultado
        resultado = {
            'RecordId': record_id,
            'CreationDate': creation_date,
            'RecordType': record_type,
            'Operation': operation,
            'UserId': user_id,
            'CorrelationId': correlation_id
        }
        resultados.append(resultado)
    
    print(f"\n{'=' * 50}")
    print(f"RESULTADOS FINALES:")
    print(f"{'=' * 50}")
    
    for i, resultado in enumerate(resultados, 1):
        print(f"\nRegistro {i}:")
        print(f"  A: {resultado['RecordId']}")
        print(f"  B: {resultado['CreationDate']}")
        print(f"  C: {resultado['RecordType']}")
        print(f"  D: {resultado['Operation']}")
        print(f"  E: {resultado['UserId']}")
        print(f"  F: {resultado['CorrelationId']}")
    
    return resultados

if __name__ == "__main__":
    extraer_correlation_id_simple()
