#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON Field Analyzer - Análisis Automático de Campos JSON
========================================================

Este script analiza automáticamente todas las filas del CSV para identificar:
- Campos únicos en todos los JSONs
- Diferencias entre filas
- Patrones de campos faltantes
- Estadísticas de frecuencia

Autor: Sistema de Análisis Purview
Fecha: 16/10/2025
"""

import pandas as pd
import json
import sys
import os
from collections import defaultdict, Counter
from datetime import datetime

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Business.json_parser import extraer_y_aplanar_audit_data


class JSONFieldAnalyzer:
    """Analizador automático de campos JSON en el CSV de Purview"""
    
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv
        self.todos_los_campos = set()
        self.presencia_campos = defaultdict(list)  # campo -> [filas donde aparece]
        self.estadisticas = defaultdict(int)
        self.errores_json = []
        self.total_filas = 0
        self.filas_procesadas = 0
        
    def analizar_todas_las_filas(self, max_filas=None):
        """
        Analiza todas las filas del CSV para extraer campos únicos
        
        Args:
            max_filas (int, optional): Límite de filas a procesar. None = todas
        """
        print(f"🔍 Iniciando análisis del archivo: {self.archivo_csv}")
        print("=" * 60)
        
        try:
            # Leer CSV
            df = pd.read_csv(
                self.archivo_csv,
                encoding='utf-8',
                sep=',',
                quotechar='"',
                escapechar='\\'
            )
            
            self.total_filas = len(df)
            filas_a_procesar = min(max_filas or self.total_filas, self.total_filas)
            
            print(f"📊 Total de filas en CSV: {self.total_filas:,}")
            print(f"🎯 Filas a procesar: {filas_a_procesar:,}")
            print()
            
            # Procesar cada fila
            for idx, fila in df.iterrows():
                if max_filas and idx >= max_filas:
                    break
                    
                if idx % 500 == 0:  # Progreso cada 500 filas
                    print(f"⏳ Procesando fila {idx + 1:,}/{filas_a_procesar:,} ({((idx + 1)/filas_a_procesar)*100:.1f}%)")
                
                self._procesar_fila_json(idx + 1, fila)
                
            self.filas_procesadas = min(filas_a_procesar, len(df))
            
        except Exception as e:
            print(f"❌ Error al leer el CSV: {e}")
            return False
            
        return True
    
    def _procesar_fila_json(self, num_fila, fila):
        """
        Procesa una fila individual para extraer campos del JSON
        
        Args:
            num_fila (int): Número de fila (1-indexed)
            fila (pandas.Series): Fila del DataFrame
        """
        try:
            # Obtener el campo AuditData (columna 6, índice 5)
            if len(fila) > 5:
                audit_data_str = str(fila.iloc[5])
                
                # Verificar si no está vacío o es NaN
                if pd.isna(audit_data_str) or audit_data_str.strip() == '' or audit_data_str == 'nan':
                    return
                
                # Extraer y aplanar el JSON
                campos_aplanados = extraer_y_aplanar_audit_data(audit_data_str)
                
                if campos_aplanados:
                    # Agregar campos únicos
                    for campo in campos_aplanados.keys():
                        self.todos_los_campos.add(campo)
                        self.presencia_campos[campo].append(num_fila)
                        self.estadisticas[campo] += 1
                        
        except Exception as e:
            self.errores_json.append({
                'fila': num_fila,
                'error': str(e)
            })
    
    def generar_reporte_completo(self):
        """Genera un reporte completo del análisis"""
        
        print("\n" + "=" * 60)
        print("📋 REPORTE COMPLETO DE ANÁLISIS JSON")
        print("=" * 60)
        
        # Estadísticas generales
        print(f"\n📊 ESTADÍSTICAS GENERALES:")
        print(f"   • Total de filas procesadas: {self.filas_procesadas:,}")
        print(f"   • Total de campos únicos encontrados: {len(self.todos_los_campos):,}")
        print(f"   • Errores de parsing JSON: {len(self.errores_json):,}")
        
        # Top 20 campos más frecuentes
        print(f"\n🏆 TOP 20 CAMPOS MÁS FRECUENTES:")
        campos_ordenados = sorted(self.estadisticas.items(), key=lambda x: x[1], reverse=True)
        
        for i, (campo, frecuencia) in enumerate(campos_ordenados[:20], 1):
            porcentaje = (frecuencia / self.filas_procesadas) * 100
            print(f"   {i:2d}. {campo:<35} | {frecuencia:5,} veces ({porcentaje:5.1f}%)")
        
        # Campos que aparecen en todas las filas
        print(f"\n✅ CAMPOS QUE APARECEN EN TODAS LAS FILAS:")
        campos_completos = [campo for campo, filas in self.presencia_campos.items() 
                           if len(filas) == self.filas_procesadas]
        
        if campos_completos:
            for campo in sorted(campos_completos):
                print(f"   • {campo}")
        else:
            print("   (Ningún campo aparece en todas las filas)")
        
        # Campos raros (aparecen en menos del 10% de las filas)
        print(f"\n🔍 CAMPOS RAROS (aparecen en <10% de las filas):")
        umbral_rareza = self.filas_procesadas * 0.1
        campos_raros = [(campo, frecuencia) for campo, frecuencia in self.estadisticas.items() 
                       if frecuencia < umbral_rareza]
        
        if campos_raros:
            for campo, frecuencia in sorted(campos_raros, key=lambda x: x[1]):
                porcentaje = (frecuencia / self.filas_procesadas) * 100
                print(f"   • {campo:<35} | {frecuencia:3,} veces ({porcentaje:4.1f}%)")
        else:
            print("   (No hay campos raros)")
        
        # Lista completa de todos los campos
        print(f"\n📝 LISTA COMPLETA DE TODOS LOS CAMPOS ({len(self.todos_los_campos)} campos):")
        for i, campo in enumerate(sorted(self.todos_los_campos), 1):
            frecuencia = self.estadisticas[campo]
            porcentaje = (frecuencia / self.filas_procesadas) * 100
            print(f"   {i:3d}. {campo:<40} | {frecuencia:5,} veces ({porcentaje:5.1f}%)")
        
        # Errores de parsing
        if self.errores_json:
            print(f"\n❌ ERRORES DE PARSING JSON ({len(self.errores_json)} errores):")
            for error in self.errores_json[:10]:  # Mostrar solo los primeros 10
                print(f"   • Fila {error['fila']}: {error['error']}")
            if len(self.errores_json) > 10:
                print(f"   ... y {len(self.errores_json) - 10} errores más")
    
    def guardar_reporte_detallado(self, archivo_salida=None):
        """
        Guarda un reporte detallado en archivo de texto
        
        Args:
            archivo_salida (str, optional): Ruta del archivo de salida
        """
        if not archivo_salida:
            timestamp = datetime.now().strftime("%d%m%Y_%H%M")
            archivo_salida = f"../Data/Output/reporte_campos_json_{timestamp}.txt"
        
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("REPORTE DETALLADO DE ANÁLISIS DE CAMPOS JSON\n")
                f.write("=" * 50 + "\n")
                f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Archivo analizado: {self.archivo_csv}\n")
                f.write(f"Filas procesadas: {self.filas_procesadas:,}\n")
                f.write(f"Total de campos únicos: {len(self.todos_los_campos):,}\n\n")
                
                # Todos los campos con estadísticas
                f.write("CAMPOS Y ESTADÍSTICAS:\n")
                f.write("-" * 30 + "\n")
                for campo in sorted(self.todos_los_campos):
                    frecuencia = self.estadisticas[campo]
                    porcentaje = (frecuencia / self.filas_procesadas) * 100
                    f.write(f"{campo:<40} | {frecuencia:5,} veces ({porcentaje:5.1f}%)\n")
                
                # Errores
                if self.errores_json:
                    f.write(f"\nERRORES DE PARSING ({len(self.errores_json)} errores):\n")
                    f.write("-" * 30 + "\n")
                    for error in self.errores_json:
                        f.write(f"Fila {error['fila']}: {error['error']}\n")
            
            print(f"\n💾 Reporte guardado en: {archivo_salida}")
            
        except Exception as e:
            print(f"❌ Error al guardar reporte: {e}")


def main():
    """Función principal para ejecutar el análisis"""
    
    print("🚀 JSON FIELD ANALYZER - Análisis Automático de Campos JSON")
    print("=" * 60)
    
    # Ruta del archivo CSV
    archivo_csv = "../Data/Input/7000LineasTextoPlano.csv"
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo_csv):
        print(f"❌ Error: No se encontró el archivo {archivo_csv}")
        return
    
    # Crear analizador
    analyzer = JSONFieldAnalyzer(archivo_csv)
    
    # Preguntar cuántas filas procesar
    print(f"📁 Archivo encontrado: {archivo_csv}")
    print("\n¿Cuántas filas quieres analizar?")
    print("1. Todas las filas (7,237 filas) - Análisis completo")
    print("2. Primeras 1,000 filas - Análisis rápido")
    print("3. Primeras 500 filas - Análisis de prueba")
    print("4. Personalizado")
    
    try:
        opcion = input("\nIngresa tu opción (1-4): ").strip()
        
        if opcion == "1":
            max_filas = None  # Todas las filas
            print("🔄 Iniciando análisis completo de todas las filas...")
        elif opcion == "2":
            max_filas = 1000
            print("🔄 Iniciando análisis de las primeras 1,000 filas...")
        elif opcion == "3":
            max_filas = 500
            print("🔄 Iniciando análisis de las primeras 500 filas...")
        elif opcion == "4":
            max_filas = int(input("Ingresa el número de filas a procesar: "))
            print(f"🔄 Iniciando análisis de las primeras {max_filas:,} filas...")
        else:
            print("❌ Opción inválida. Usando análisis de 500 filas por defecto.")
            max_filas = 500
        
        # Ejecutar análisis
        if analyzer.analizar_todas_las_filas(max_filas):
            # Generar reporte
            analyzer.generar_reporte_completo()
            
            # Guardar reporte detallado
            analyzer.guardar_reporte_detallado()
            
            print(f"\n✅ Análisis completado exitosamente!")
            print(f"📊 Procesadas {analyzer.filas_procesadas:,} filas")
            print(f"🔍 Encontrados {len(analyzer.todos_los_campos)} campos únicos")
            
        else:
            print("❌ Error durante el análisis")
            
    except KeyboardInterrupt:
        print("\n⏹️ Análisis cancelado por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()

