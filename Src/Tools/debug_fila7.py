#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG SCRIPT - Análisis específico de fila 7
============================================

Script para debuggear exactamente qué está pasando con la extracción
del CorrelationId en la fila 7 del CSV.
"""

import pandas as pd
import json
import os
import sys

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Business.json_parser import extraer_y_aplanar_audit_data, limpiar_json_string, flatten_json

def debug_fila_especifica(num_fila):
    """
    Debug específico de una fila del CSV
    
    Args:
        num_fila (int): Número de fila a debuggear (1-indexed)
    """
    print(f"🔍 DEBUGGING FILA {num_fila}")
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
    
    # Obtener la fila específica (convertir a 0-indexed)
    fila_idx = num_fila - 1
    fila = df.iloc[fila_idx]
    
    print(f"📊 Datos básicos de la fila {num_fila}:")
    print(f"   • RecordId: {fila.get('RecordId', 'N/A')}")
    print(f"   • UserId: {fila.get('UserId', 'N/A')}")
    print(f"   • Operation: {fila.get('Operation', 'N/A')}")
    
    # Obtener AuditData
    audit_data_raw = fila.get('AuditData', 'N/A')
    print(f"\n📋 AuditData RAW (primeros 200 caracteres):")
    print(f"   {str(audit_data_raw)[:200]}...")
    
    if pd.isna(audit_data_raw) or audit_data_raw == 'N/A':
        print("❌ AuditData está vacío o es N/A")
        return
    
    # Limpiar JSON
    print(f"\n🧹 Limpiando JSON...")
    audit_data_limpio = limpiar_json_string(str(audit_data_raw))
    print(f"   ✓ JSON limpiado (primeros 200 caracteres):")
    print(f"   {audit_data_limpio[:200]}...")
    
    # Parsear JSON
    print(f"\n🔧 Parseando JSON...")
    try:
        audit_data_dict = json.loads(audit_data_limpio)
        print(f"   ✅ JSON parseado exitosamente")
        print(f"   📊 Claves principales encontradas: {list(audit_data_dict.keys())}")
        
        # Verificar AppAccessContext
        if 'AppAccessContext' in audit_data_dict:
            app_context = audit_data_dict['AppAccessContext']
            print(f"   📋 AppAccessContext encontrado:")
            print(f"      • Tipo: {type(app_context)}")
            print(f"      • Claves: {list(app_context.keys())}")
            
            # Verificar CorrelationId específicamente
            if 'CorrelationId' in app_context:
                correlation_id = app_context['CorrelationId']
                print(f"      ✅ CorrelationId en AppAccessContext: '{correlation_id}'")
            else:
                print(f"      ❌ CorrelationId NO encontrado en AppAccessContext")
        
        # Verificar CorrelationId en nivel principal
        if 'CorrelationId' in audit_data_dict:
            correlation_id_main = audit_data_dict['CorrelationId']
            print(f"   ✅ CorrelationId en nivel principal: '{correlation_id_main}'")
        else:
            print(f"   ❌ CorrelationId NO encontrado en nivel principal")
        
        # Aplanar JSON
        print(f"\n📊 Aplanando JSON...")
        campos_aplanados = flatten_json(audit_data_dict)
        print(f"   ✅ JSON aplanado exitosamente")
        print(f"   📋 Total de campos aplanados: {len(campos_aplanados)}")
        
        # Buscar CorrelationId en campos aplanados
        correlation_campos = [k for k in campos_aplanados.keys() if 'CorrelationId' in k]
        print(f"   🔍 Campos con 'CorrelationId': {correlation_campos}")
        
        for campo in correlation_campos:
            valor = campos_aplanados[campo]
            print(f"      • {campo}: '{valor}'")
        
        # Mostrar todos los campos aplanados
        print(f"\n📋 TODOS LOS CAMPOS APLANADOS:")
        for i, (campo, valor) in enumerate(campos_aplanados.items(), 1):
            print(f"   {i:2d}. {campo:<40} = '{valor}'")
        
    except json.JSONDecodeError as e:
        print(f"   ❌ Error parseando JSON: {e}")
        print(f"   📋 JSON problemático (primeros 500 caracteres):")
        print(f"   {audit_data_limpio[:500]}")
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

def comparar_filas_1_y_7():
    """Compara específicamente las filas 1 y 7"""
    print("🔍 COMPARACIÓN FILA 1 vs FILA 7")
    print("=" * 60)
    
    print("\n" + "="*30 + " FILA 1 " + "="*30)
    debug_fila_especifica(1)
    
    print("\n" + "="*30 + " FILA 7 " + "="*30)
    debug_fila_especifica(7)

def main():
    """Función principal de debug"""
    print("🚀 DEBUG SCRIPT - Análisis de extracción JSON")
    print("=" * 60)
    
    print("¿Qué quieres debuggear?")
    print("1. Solo fila 1")
    print("2. Solo fila 7") 
    print("3. Comparar fila 1 vs fila 7")
    print("4. Fila personalizada")
    
    try:
        opcion = input("\nIngresa tu opción (1-4): ").strip()
        
        if opcion == "1":
            debug_fila_especifica(1)
        elif opcion == "2":
            debug_fila_especifica(7)
        elif opcion == "3":
            comparar_filas_1_y_7()
        elif opcion == "4":
            num_fila = int(input("Ingresa el número de fila: "))
            debug_fila_especifica(num_fila)
        else:
            print("❌ Opción inválida")
            
    except KeyboardInterrupt:
        print("\n⏹️ Debug cancelado")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
