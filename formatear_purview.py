from data_extractor import getdata_from_base_excel
from excel_creator import crear_excel_purview

def main():
    """
    Función principal que orquesta todo el proceso:
    1. Extrae datos del Excel base
    2. Muestra los datos en consola
    3. Crea el archivo Excel de salida
    """
    print("🚀 Iniciando procesamiento de datos Purview...")
    print("=" * 60)
    
    # Paso 1: Extraer datos del archivo Excel base
    # archivo_fuente = "3000lineasDelimitadoComas.xlsx"
    archivo_fuente = "3000lineasDelimitadoComas.xlsx"
    num_filas_procesar = 3000
    
    registros_interface, datos_para_excel = getdata_from_base_excel(
        archivo_fuente, 
        num_filas_procesar
    )
    
    # Paso 2: Mostrar datos en consola usando InformeInterface
    print("\n📋 MOSTRANDO DATOS PROCESADOS:")
    print("=" * 60)
    
    for i, registro in enumerate(registros_interface, 1):
        registro.mostrar_datos(i)
    
    # Paso 3: Crear archivo Excel con los datos
    print("\n📊 GENERANDO ARCHIVO EXCEL:")
    print("=" * 60)
    print("🚀 Generando archivo Excel...")
    
    nombre_archivo = crear_excel_purview(datos_para_excel)
    
    # Resumen final
    print("\n🎉 PROCESO COMPLETADO EXITOSAMENTE!")
    print("=" * 60)
    print(f"📄 Archivo generado: {nombre_archivo}")
    print(f"📊 Registros procesados: {len(registros_interface)}")
    print(f"🔍 Archivo fuente: {archivo_fuente}")

if __name__ == "__main__":
    main()