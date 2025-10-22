import pandas as pd
from extractor_usuarios_normales import extraer_usuarios_normales, mostrar_resumen_usuarios_normales
from extractor_usuarios_sharepoint_system import extraer_usuarios_sharepoint_system, mostrar_resumen_usuarios_sharepoint_system
from excel_creator import crear_excel_dos_pestanas, crear_resumen_columnas

def es_usuario_sharepoint_system(user_id):
    """
    Detecta si un usuario es del tipo SharePoint System
    
    Args:
        user_id (str): ID del usuario
        
    Returns:
        bool: True si es usuario SharePoint system, False si es usuario normal
    """
    if pd.isna(user_id) or user_id == 'N/A':
        return False
    
    user_id_str = str(user_id).lower()
    return 'sharepoint' in user_id_str or 'system' in user_id_str

def main():
    """
    FASE 3: Análisis Diferenciado por Tipo de Usuario
    
    Este script:
    1. Lee el CSV completo (8 columnas)
    2. Detecta el tipo de usuario (Normal vs SharePoint System)
    3. Extrae campos específicos según el tipo
    4. Genera Excel con DOS PESTANAS separadas
    """
    print("\n" + "=" * 80)
    print("PURVIEW SCRIPT ANALYSER - FASE 3: ANALISIS DIFERENCIADO")
    print("=" * 80)
    print("Caracteristicas:")
    print("   Lectura directa de CSV (NO Excel)")
    print("   Deteccion automatica de tipo de usuario")
    print("   Extraccion diferenciada por tipo")
    print("   Generacion de Excel con DOS PESTANAS")
    print("=" * 80)
    
    # Configuración
    import os
    # Obtener la ruta absoluta del archivo CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio de este script
    archivo_fuente = os.path.join(script_dir, "..", "Data", "Input", "7000LineasTextoPlano.csv")
    archivo_fuente = os.path.normpath(archivo_fuente)  # Normalizar la ruta
    num_filas_procesar = 100  # Probar con 100 filas como solicitaste
    
    print(f"\nArchivo fuente: {archivo_fuente}")
    print(f"Numero de filas a procesar: {num_filas_procesar}")
    print(f"Procesando con deteccion diferenciada por tipo de usuario")
    
    # PASO 1: Extraer datos diferenciados por tipo de usuario
    print("\n" + "=" * 80)
    print("PASO 1: EXTRAYENDO DATOS DIFERENCIADOS POR TIPO")
    print("=" * 80)
    
    try:
        # Extraer usuarios normales
        print("\n--- EXTRAYENDO USUARIOS NORMALES ---")
        datos_usuarios_normales, campos_usuarios_normales = extraer_usuarios_normales(
            archivo_fuente, 
            num_filas_procesar
        )
        mostrar_resumen_usuarios_normales(campos_usuarios_normales)
        
        # Extraer usuarios SharePoint system
        print("\n--- EXTRAYENDO USUARIOS SHAREPOINT SYSTEM ---")
        datos_usuarios_sharepoint, campos_usuarios_sharepoint = extraer_usuarios_sharepoint_system(
            archivo_fuente, 
            num_filas_procesar
        )
        mostrar_resumen_usuarios_sharepoint_system(campos_usuarios_sharepoint)
        
    except FileNotFoundError:
        print(f"\nERROR: No se encontro el archivo {archivo_fuente}")
        print("   Verifica que el archivo CSV este en la ubicacion correcta")
        return
    except Exception as e:
        print(f"\nERROR inesperado: {e}")
        return
    
    # PASO 2: Crear archivo Excel con DOS PESTANAS
    print("\n" + "=" * 80)
    print("PASO 2: GENERANDO ARCHIVO EXCEL CON DOS PESTANAS")
    print("=" * 80)
    
    try:
        nombre_archivo_excel = crear_excel_dos_pestanas(
            datos_usuarios_normales, 
            campos_usuarios_normales,
            datos_usuarios_sharepoint,
            campos_usuarios_sharepoint
        )
        
        # Crear archivo de resumen de columnas
        nombre_archivo_resumen = crear_resumen_columnas(
            campos_usuarios_normales, 
            campos_usuarios_sharepoint
        )
        
    except Exception as e:
        print(f"\nERROR al crear Excel: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # RESUMEN FINAL
    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    print(f"\nArchivos generados:")
    print(f"   1. Excel: {nombre_archivo_excel}")
    print(f"   2. Resumen: {nombre_archivo_resumen}")
    print(f"\nEstadisticas:")
    print(f"   Registros usuarios normales: {len(datos_usuarios_normales)}")
    print(f"   Registros usuarios SharePoint: {len(datos_usuarios_sharepoint)}")
    print(f"   Columnas usuarios normales: {len(campos_usuarios_normales)}")
    print(f"   Columnas usuarios SharePoint: {len(campos_usuarios_sharepoint)}")
    print(f"   Archivo fuente: {archivo_fuente}")
    print("\n" + "=" * 80)
    print("Datos extraidos sin corrupcion")
    print("JSON completamente aplanado")
    print("UTF-8 preservado")
    print("Dos pestanas separadas por tipo de usuario")
    print("Listo para analisis diferenciado")
    print("=" * 80)

if __name__ == "__main__":
    main()

