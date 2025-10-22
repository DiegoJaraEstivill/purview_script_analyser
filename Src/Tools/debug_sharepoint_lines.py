#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG ESPECÍFICO - Líneas 7 y 10 SharePoint System
==================================================

Script para debuggear exactamente por qué no se extraen CreationTime y CorrelationId
de las líneas 7 y 10 que son tipo SharePoint system.
"""

import pandas as pd
import json
import os
import sys

# Agregar el directorio Business al path para importar json_parser
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Business'))
from json_parser import extraer_y_aplanar_audit_data, limpiar_json_string, flatten_json

def debug_lineas_sharepoint():
    """Debug específico de las líneas 7 y 10 que son SharePoint system"""
    
    print("DEBUG ESPECIFICO - LINEAS 7 Y 10 SHAREPOINT SYSTEM")
    print("=" * 60)
    
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
    
    # Analizar líneas 7 y 10 (índices 6 y 9)
    lineas_a_analizar = [7, 10]
    
    for num_linea in lineas_a_analizar:
        print(f"\n{'='*30} LINEA {num_linea} {'='*30}")
        
        fila_idx = num_linea - 1  # Convertir a 0-indexed
        fila = df.iloc[fila_idx]
        
        print(f"UserId: {fila.get('UserId', 'N/A')}")
        print(f"Operation: {fila.get('Operation', 'N/A')}")
        
        # Obtener AuditData
        audit_data_raw = fila.get('AuditData', 'N/A')
        print(f"\nAuditData RAW (primeros 300 caracteres):")
        print(f"{str(audit_data_raw)[:300]}...")
        
        if pd.isna(audit_data_raw) or audit_data_raw == 'N/A':
            print("ERROR: AuditData esta vacio")
            continue
        
        # Limpiar JSON
        audit_data_limpio = limpiar_json_string(str(audit_data_raw))
        
        # Parsear JSON
        try:
            audit_data_dict = json.loads(audit_data_limpio)
            print(f"\nJSON parseado exitosamente")
            print(f"Claves principales: {list(audit_data_dict.keys())}")
            
            # Verificar CreationTime específicamente
            if 'CreationTime' in audit_data_dict:
                creation_time = audit_data_dict['CreationTime']
                print(f"✓ CreationTime encontrado: '{creation_time}'")
            else:
                print(f"❌ CreationTime NO encontrado")
            
            # Verificar CorrelationId específicamente
            if 'CorrelationId' in audit_data_dict:
                correlation_id = audit_data_dict['CorrelationId']
                print(f"✓ CorrelationId encontrado: '{correlation_id}'")
            else:
                print(f"❌ CorrelationId NO encontrado")
            
            # Verificar AppAccessContext
            if 'AppAccessContext' in audit_data_dict:
                app_context = audit_data_dict['AppAccessContext']
                print(f"AppAccessContext claves: {list(app_context.keys())}")
                
                if 'CorrelationId' in app_context:
                    app_correlation = app_context['CorrelationId']
                    print(f"✓ CorrelationId en AppAccessContext: '{app_correlation}'")
                else:
                    print(f"❌ CorrelationId NO encontrado en AppAccessContext")
            
            # Aplanar JSON
            campos_aplanados = flatten_json(audit_data_dict)
            print(f"\nCampos aplanados: {len(campos_aplanados)}")
            
            # Buscar CreationTime y CorrelationId en campos aplanados
            creation_time_campos = [k for k in campos_aplanados.keys() if 'CreationTime' in k]
            correlation_campos = [k for k in campos_aplanados.keys() if 'CorrelationId' in k]
            
            print(f"Campos con 'CreationTime': {creation_time_campos}")
            print(f"Campos con 'CorrelationId': {correlation_campos}")
            
            for campo in creation_time_campos:
                valor = campos_aplanados[campo]
                print(f"  {campo}: '{valor}'")
            
            for campo in correlation_campos:
                valor = campos_aplanados[campo]
                print(f"  {campo}: '{valor}'")
            
            # Mostrar TODOS los campos aplanados para ver qué se está perdiendo
            print(f"\nTODOS LOS CAMPOS APLANADOS:")
            for i, (campo, valor) in enumerate(campos_aplanados.items(), 1):
                print(f"  {i:2d}. {campo:<35} = '{valor}'")
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parseando JSON: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_lineas_sharepoint()
