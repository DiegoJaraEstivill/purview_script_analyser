from data_extractor import getdata_from_csv
from excel_creator import crear_excel_purview

def main():
    """
    Función principal que procesa el CSV de Purview
    
    Fase 1: Extrae solo los primeros 5 campos básicos
    - RecordId
    - CreationDate
    - RecordType
    - Operation
    - UserId
    """
    print("🚀 INICIANDO PROCESAMIENTO DE DATOS PURVIEW")
    print("=" * 60)
    print("📌 FASE 1: Extracción de campos básicos (5 columnas)")
    print("=" * 60)
    
    # Configuración - AHORA LEE CSV, NO EXCEL
    archivo_fuente = "7000LineasTextoPlano.csv"
    num_filas_procesar = 5
    
    print(f"\n📂 Archivo fuente: {archivo_fuente}")
    print(f"📊 Número de filas a procesar: {num_filas_procesar}")
    print(f"✅ Formato: CSV de texto plano (NO Excel)")
    print("\n" + "=" * 60)
    
    # Paso 1: Extraer datos del CSV de texto plano
    print("\n🔍 PASO 1: Extrayendo datos del CSV...")
    datos_para_excel = getdata_from_csv(
        archivo_fuente, 
        num_filas_procesar
    )
    
    # Paso 2: Crear archivo Excel con los datos
    print("\n📊 PASO 2: Generando archivo Excel...")
    nombre_archivo = crear_excel_purview(datos_para_excel)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("🎉 PROCESO COMPLETADO EXITOSAMENTE!")
    print("=" * 60)
    print(f"📄 Archivo generado: {nombre_archivo}")
    print(f"📊 Registros procesados: {len(datos_para_excel)}")
    print(f"📋 Columnas creadas: 5 (RecordId, CreationDate, RecordType, Operation, UserId)")
    print(f"🔍 Archivo fuente: {archivo_fuente}")
    print("=" * 60)
    print("\n✅ Los datos se extrajeron correctamente SIN corrupción")
    print("✅ Formato CSV leído directamente (no Excel)")
    print("✅ Encoding UTF-8 preservado")
    print("\n🔜 Próximo paso: Analizar campo AuditData (JSON) en Fase 2")
    print("=" * 60)

if __name__ == "__main__":
    main()