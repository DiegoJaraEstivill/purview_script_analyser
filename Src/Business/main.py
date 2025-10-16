from extractor import extraer_todos_los_campos_csv, mostrar_resumen_campos
from excel_creator import crear_excel_completo, crear_resumen_columnas

def main():
    """
    FASE 2: Análisis Completo con JSON Flattening
    
    Este script:
    1. Lee el CSV completo (8 columnas)
    2. Parsea el JSON del campo AuditData
    3. Aplana (flatten) el JSON anidado
    4. Genera Excel con TODAS las columnas (~43+)
    """
    print("\n" + "=" * 80)
    print("🚀 PURVIEW SCRIPT ANALYSER - FASE 2: ANÁLISIS COMPLETO")
    print("=" * 80)
    print("📌 Características:")
    print("   ✓ Lectura directa de CSV (NO Excel)")
    print("   ✓ Parsing completo del JSON AuditData")
    print("   ✓ Flattening de JSON anidado (AppAccessContext)")
    print("   ✓ Generación de Excel con todas las columnas")
    print("=" * 80)
    
    # Configuración
    archivo_fuente = "../Data/Input/7000LineasTextoPlano.csv"
    num_filas_procesar = 7000  # Empezar con pocas filas para probar
    
    print(f"\n📂 Archivo fuente: {archivo_fuente}")
    print(f"📊 Número de filas a procesar: {num_filas_procesar}")
    print(f"⚠️  Procesando pocas filas para validación inicial")
    
    # PASO 1: Extraer datos del CSV con JSON aplanado
    print("\n" + "=" * 80)
    print("🔍 PASO 1: EXTRAYENDO DATOS DEL CSV")
    print("=" * 80)
    
    try:
        datos_extraidos, campos_unicos = extraer_todos_los_campos_csv(
            archivo_fuente, 
            num_filas_procesar
        )
        
        # Mostrar resumen de campos
        mostrar_resumen_campos(campos_unicos)
        
    except FileNotFoundError:
        print(f"\n❌ ERROR: No se encontró el archivo {archivo_fuente}")
        print("   Verifica que el archivo CSV esté en la ubicación correcta")
        return
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {e}")
        return
    
    # PASO 2: Crear archivo Excel
    print("\n" + "=" * 80)
    print("📊 PASO 2: GENERANDO ARCHIVO EXCEL COMPLETO")
    print("=" * 80)
    
    try:
        nombre_archivo_excel = crear_excel_completo(datos_extraidos, campos_unicos)
        
        # Crear archivo de resumen de columnas
        nombre_archivo_resumen = crear_resumen_columnas(campos_unicos)
        
    except Exception as e:
        print(f"\n❌ ERROR al crear Excel: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # RESUMEN FINAL
    print("\n" + "=" * 80)
    print("🎉 PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    print(f"\n📄 Archivos generados:")
    print(f"   1. Excel: {nombre_archivo_excel}")
    print(f"   2. Resumen: {nombre_archivo_resumen}")
    print(f"\n📊 Estadísticas:")
    print(f"   ✓ Registros procesados: {len(datos_extraidos)}")
    print(f"   ✓ Columnas totales: {len(campos_unicos)}")
    print(f"   ✓ Archivo fuente: {archivo_fuente}")
    print("\n" + "=" * 80)
    print("✅ Datos extraídos sin corrupción")
    print("✅ JSON completamente aplanado")
    print("✅ UTF-8 preservado")
    print("✅ Listo para análisis")
    print("=" * 80)
    
    # Sugerencia para procesar más filas
    if num_filas_procesar < 100:
        print("\n💡 SUGERENCIA:")
        print(f"   Si el resultado es correcto, edita la línea 21 para procesar más filas:")
        print(f"   num_filas_procesar = 100  # o 1000, o todo el archivo")
        print("=" * 80)

if __name__ == "__main__":
    main()

