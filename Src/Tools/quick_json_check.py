#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick JSON Check - Análisis Rápido de Campos JSON
================================================

Script rápido para comparar campos JSON entre filas específicas
y identificar diferencias inmediatamente.

Autor: Sistema de Análisis Purview
Fecha: 16/10/2025
"""

import pandas as pd
import json
import sys
import os
from collections import defaultdict

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Business.json_parser import extraer_y_aplanar_audit_data


def comparar_filas_json(fila1, fila2, num_fila1, num_fila2):
    """
    Compara los campos JSON entre dos filas específicas
    
    Args:
        fila1, fila2: pandas.Series - Las filas a comparar
        num_fila1, num_fila2: int - Números de fila para referencia
    """
    print(f"🔍 COMPARANDO FILA {num_fila1} vs FILA {num_fila2}")
    print("=" * 50)
    
    try:
        # Extraer campos de ambas filas
        audit_data1 = str(fila1.iloc[5]) if len(fila1) > 5 else ""
        audit_data2 = str(fila2.iloc[5]) if len(fila2) > 5 else ""
        
        campos1 = extraer_y_aplanar_audit_data(audit_data1) if audit_data1 != "nan" else {}
        campos2 = extraer_y_aplanar_audit_data(audit_data2) if audit_data2 != "nan" else {}
        
        print(f"📊 Fila {num_fila1}: {len(campos1)} campos")
        print(f"📊 Fila {num_fila2}: {len(campos2)} campos")
        
        # Encontrar diferencias
        campos_solo_fila1 = set(campos1.keys()) - set(campos2.keys())
        campos_solo_fila2 = set(campos2.keys()) - set(campos1.keys())
        campos_comunes = set(campos1.keys()) & set(campos2.keys())
        
        print(f"\n✅ Campos comunes: {len(campos_comunes)}")
        print(f"🔴 Solo en fila {num_fila1}: {len(campos_solo_fila1)}")
        print(f"🔴 Solo en fila {num_fila2}: {len(campos_solo_fila2)}")
        
        # Mostrar campos únicos de cada fila
        if campos_solo_fila1:
            print(f"\n🔴 CAMPOS SOLO EN FILA {num_fila1}:")
            for campo in sorted(campos_solo_fila1):
                print(f"   • {campo}")
        
        if campos_solo_fila2:
            print(f"\n🔴 CAMPOS SOLO EN FILA {num_fila2}:")
            for campo in sorted(campos_solo_fila2):
                print(f"   • {campo}")
        
        # Mostrar algunos campos comunes para verificar
        if campos_comunes:
            print(f"\n✅ PRIMEROS 10 CAMPOS COMUNES:")
            for campo in sorted(list(campos_comunes))[:10]:
                print(f"   • {campo}")
            if len(campos_comunes) > 10:
                print(f"   ... y {len(campos_comunes) - 10} campos más")
        
        return {
            'campos_fila1': campos1,
            'campos_fila2': campos2,
            'solo_fila1': campos_solo_fila1,
            'solo_fila2': campos_solo_fila2,
            'comunes': campos_comunes
        }
        
    except Exception as e:
        print(f"❌ Error al comparar filas: {e}")
        return None


def analizar_muestra_filas(archivo_csv, num_filas=10):
    """
    Analiza una muestra de filas para identificar patrones rápidamente
    
    Args:
        archivo_csv (str): Ruta del archivo CSV
        num_filas (int): Número de filas a analizar
    """
    print(f"🔍 ANÁLISIS RÁPIDO DE {num_filas} FILAS")
    print("=" * 40)
    
    try:
        df = pd.read_csv(
            archivo_csv,
            encoding='utf-8',
            sep=',',
            quotechar='"',
            escapechar='\\'
        )
        
        print(f"📁 Archivo cargado: {len(df)} filas totales")
        print(f"🎯 Analizando primeras {min(num_filas, len(df))} filas\n")
        
        todos_los_campos = set()
        campos_por_fila = {}
        
        for i in range(min(num_filas, len(df))):
            fila = df.iloc[i]
            audit_data = str(fila.iloc[5]) if len(fila) > 5 else ""
            
            if audit_data != "nan" and audit_data.strip():
                campos = extraer_y_aplanar_audit_data(audit_data)
                campos_por_fila[i + 1] = set(campos.keys())
                todos_los_campos.update(campos.keys())
                
                print(f"Fila {i + 1:2d}: {len(campos):2d} campos")
        
        print(f"\n📊 RESUMEN:")
        print(f"   • Total de campos únicos encontrados: {len(todos_los_campos)}")
        
        # Encontrar campos que aparecen en todas las filas
        campos_consistentes = todos_los_campos.copy()
        for fila_num, campos_fila in campos_por_fila.items():
            campos_consistentes &= campos_fila
        
        print(f"   • Campos que aparecen en TODAS las filas: {len(campos_consistentes)}")
        
        if campos_consistentes:
            print(f"\n✅ CAMPOS CONSISTENTES (en todas las filas):")
            for campo in sorted(campos_consistentes):
                print(f"   • {campo}")
        
        # Campos que varían
        campos_variables = todos_los_campos - campos_consistentes
        if campos_variables:
            print(f"\n🔴 CAMPOS VARIABLES ({len(campos_variables)} campos):")
            for campo in sorted(campos_variables):
                filas_con_campo = [fila for fila, campos in campos_por_fila.items() if campo in campos]
                print(f"   • {campo:<35} | Aparece en filas: {filas_con_campo}")
        
        return {
            'todos_los_campos': todos_los_campos,
            'campos_consistentes': campos_consistentes,
            'campos_variables': campos_variables,
            'campos_por_fila': campos_por_fila
        }
        
    except Exception as e:
        print(f"❌ Error en análisis rápido: {e}")
        return None


def main():
    """Función principal"""
    
    print("🚀 QUICK JSON CHECK - Análisis Rápido de Campos JSON")
    print("=" * 55)
    
    archivo_csv = "../Data/Input/7000LineasTextoPlano.csv"
    
    if not os.path.exists(archivo_csv):
        print(f"❌ Error: No se encontró el archivo {archivo_csv}")
        return
    
    print("¿Qué tipo de análisis quieres hacer?")
    print("1. Comparar fila 1 vs fila 7 (como pediste)")
    print("2. Análisis rápido de las primeras 10 filas")
    print("3. Comparar dos filas específicas")
    
    try:
        opcion = input("\nIngresa tu opción (1-3): ").strip()
        
        df = pd.read_csv(
            archivo_csv,
            encoding='utf-8',
            sep=',',
            quotechar='"',
            escapechar='\\'
        )
        
        if opcion == "1":
            # Comparar fila 1 vs fila 7
            if len(df) >= 7:
                comparar_filas_json(df.iloc[0], df.iloc[6], 1, 7)
            else:
                print("❌ No hay suficientes filas para comparar 1 y 7")
                
        elif opcion == "2":
            # Análisis rápido
            analizar_muestra_filas(archivo_csv, 10)
            
        elif opcion == "3":
            # Comparar filas específicas
            fila1 = int(input("Primera fila a comparar: ")) - 1  # Convertir a 0-indexed
            fila2 = int(input("Segunda fila a comparar: ")) - 1
            
            if 0 <= fila1 < len(df) and 0 <= fila2 < len(df):
                comparar_filas_json(df.iloc[fila1], df.iloc[fila2], fila1 + 1, fila2 + 1)
            else:
                print("❌ Números de fila inválidos")
        else:
            print("❌ Opción inválida")
            
    except KeyboardInterrupt:
        print("\n⏹️ Análisis cancelado")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

