#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTRACTOR SIMPLE - Solo CorrelationId para SharePoint System
============================================================

Script simple para extraer SOLO CorrelationId de usuarios SharePoint system
basándome en la línea específica que me mostraste.
"""

import pandas as pd
import json
import os
import sys

# Agregar el directorio Business al path para importar json_parser
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Business'))
from json_parser import limpiar_json_string

def extraer_solo_correlation_id():
    """Extraer SOLO CorrelationId de usuarios SharePoint system"""
    
    print("EXTRACTOR SIMPLE - SOLO CORRELATION ID")
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
        
        print(f"UserId: {fila.get('UserId', 'N/A')}")
        print(f"Operation: {fila.get('Operation', 'N/A')}")
        
        # Obtener AuditData
        audit_data_raw = fila.get('AuditData', 'N/A')
        
        if pd.isna(audit_data_raw) or audit_data_raw == 'N/A':
            print("ERROR: AuditData vacio")
            continue
        
        # Limpiar JSON
        audit_data_limpio = limpiar_json_string(str(audit_data_raw))
        
        # Parsear JSON
        try:
            audit_data_dict = json.loads(audit_data_limpio)
            
            # Buscar CorrelationId en el JSON
            correlation_id = None
            
            # Buscar en nivel principal
            if 'CorrelationId' in audit_data_dict:
                correlation_id = audit_data_dict['CorrelationId']
                print(f"CorrelationId encontrado en nivel principal: '{correlation_id}'")
            
            # Buscar en AppAccessContext
            elif 'AppAccessContext' in audit_data_dict:
                app_context = audit_data_dict['AppAccessContext']
                if 'CorrelationId' in app_context:
                    correlation_id = app_context['CorrelationId']
                    print(f"CorrelationId encontrado en AppAccessContext: '{correlation_id}'")
            
            if correlation_id:
                print(f"✓ CORRELATION ID EXTRAIDO: '{correlation_id}'")
            else:
                print(f"❌ CorrelationId NO encontrado")
                
        except json.JSONDecodeError as e:
            print(f"ERROR parseando JSON: {e}")
            print(f"JSON problemático (primeros 200 caracteres):")
            print(f"{audit_data_limpio[:200]}...")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

if __name__ == "__main__":
    extraer_solo_correlation_id()
