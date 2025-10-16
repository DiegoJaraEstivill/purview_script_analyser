import pandas as pd
from json_parser import extraer_y_aplanar_audit_data, obtener_campos_unicos, normalizar_registro

def extraer_todos_los_campos_csv(archivo_csv, num_filas=5):
    """
    Extrae TODOS los campos del CSV incluyendo el JSON aplanado de AuditData
    
    BLOQUES DE COLUMNAS:
    1. Campos base del CSV (5): RecordId, CreationDate, RecordType, Operation, UserId
    2. Campos del JSON AuditData (aplanados, ~40+)
    3. Campos finales del CSV (2): AssociatedAdminUnits, AssociatedAdminUnitsNames
    
    Args:
        archivo_csv (str): Ruta al archivo CSV fuente
        num_filas (int): Número de filas a procesar
        
    Returns:
        list: Lista de diccionarios con TODOS los campos
    """
    print(f"📂 Leyendo archivo CSV completo: {archivo_csv}")
    print("=" * 80)
    
    # Leer el archivo CSV - AHORA leemos TODAS las columnas
    df = pd.read_csv(
        archivo_csv,
        encoding='utf-8',
        sep=',',
        quotechar='"',
        escapechar='\\'
    )
    
    print(f"📊 Total de filas en el archivo: {len(df)}")
    print(f"📋 Columnas del CSV: {list(df.columns)}")
    
    # Tomar las primeras x filas
    filas_a_revisar = df.head(num_filas)
    
    print(f"\n🔍 Procesando {len(filas_a_revisar)} filas...")
    print("=" * 80)
    
    # Lista para almacenar resultados
    lista_registros = []
    
    # Procesar cada fila
    for i, (index, row) in enumerate(filas_a_revisar.iterrows(), 1):
        print(f"\n🔄 Procesando fila {i}/{len(filas_a_revisar)}...")
        
        # BLOQUE 1: Campos base del CSV (5 campos)
        registro = {
            'RecordId': row.get('RecordId', 'N/A'),
            'CreationDate': row.get('CreationDate', 'N/A'),
            'RecordType': row.get('RecordType', 'N/A'),
            'Operation': row.get('Operation', 'N/A'),
            'UserId': row.get('UserId', 'N/A'),
        }
        
        # BLOQUE 2: Campos del JSON AuditData (aplanados)
        audit_data = row.get('AuditData', 'N/A')
        
        if pd.notna(audit_data) and audit_data != 'N/A':
            # Extraer y aplanar el JSON
            campos_json = extraer_y_aplanar_audit_data(str(audit_data), i)
            
            # Agregar campos del JSON al registro con prefijo para evitar conflictos
            for key, value in campos_json.items():
                # Renombrar campos duplicados del JSON para evitar conflictos
                if key in ['Operation', 'UserId', 'RecordType', 'Id']:
                    nuevo_key = f"Audit_{key}"
                else:
                    nuevo_key = key
                
                registro[nuevo_key] = value
        
        # BLOQUE 3: Campos finales del CSV (2 campos)
        registro['AssociatedAdminUnits'] = row.get('AssociatedAdminUnits', 'N/A')
        registro['AssociatedAdminUnitsNames'] = row.get('AssociatedAdminUnitsNames', 'N/A')
        
        # Agregar a la lista
        lista_registros.append(registro)
        
        print(f"   ✓ Total de campos en este registro: {len(registro)}")
        print(f"✅ Fila {i} procesada correctamente")
    
    print(f"\n{'=' * 80}")
    print(f"🎯 Extracción completada: {len(lista_registros)} registros procesados")
    
    # Obtener todos los campos únicos de todos los registros
    campos_unicos = obtener_campos_unicos(lista_registros)
    print(f"📊 Total de campos únicos encontrados: {len(campos_unicos)}")
    print(f"{'=' * 80}")
    
    # Normalizar todos los registros para que tengan los mismos campos
    print("\n🔄 Normalizando registros...")
    registros_normalizados = []
    for registro in lista_registros:
        registro_normalizado = normalizar_registro(registro, campos_unicos)
        registros_normalizados.append(registro_normalizado)
    
    print("✅ Registros normalizados")
    
    return registros_normalizados, campos_unicos

def mostrar_resumen_campos(campos_unicos):
    """
    Muestra un resumen organizado de los campos encontrados
    
    Args:
        campos_unicos (list): Lista de campos únicos
    """
    print("\n" + "=" * 80)
    print("📋 RESUMEN DE CAMPOS ENCONTRADOS")
    print("=" * 80)
    
    # Identificar campos por bloques
    campos_base = ['RecordId', 'CreationDate', 'RecordType', 'Operation', 'UserId']
    campos_finales = ['AssociatedAdminUnits', 'AssociatedAdminUnitsNames']
    campos_app_context = [c for c in campos_unicos if 'AppAccessContext_' in c]
    campos_json_resto = [c for c in campos_unicos 
                         if c not in campos_base 
                         and c not in campos_finales 
                         and 'AppAccessContext_' not in c]
    
    print(f"\n📌 BLOQUE 1 - Campos Base del CSV ({len(campos_base)} campos):")
    for campo in campos_base:
        if campo in campos_unicos:
            print(f"   ✓ {campo}")
    
    print(f"\n📌 BLOQUE 2 - Campos de AppAccessContext ({len(campos_app_context)} campos):")
    for campo in sorted(campos_app_context)[:10]:  # Mostrar primeros 10
        print(f"   ✓ {campo}")
    if len(campos_app_context) > 10:
        print(f"   ... y {len(campos_app_context) - 10} más")
    
    print(f"\n📌 BLOQUE 3 - Campos del JSON AuditData ({len(campos_json_resto)} campos):")
    for campo in sorted(campos_json_resto)[:15]:  # Mostrar primeros 15
        print(f"   ✓ {campo}")
    if len(campos_json_resto) > 15:
        print(f"   ... y {len(campos_json_resto) - 15} más")
    
    print(f"\n📌 BLOQUE 4 - Campos Finales del CSV ({len(campos_finales)} campos):")
    for campo in campos_finales:
        if campo in campos_unicos:
            print(f"   ✓ {campo}")
    
    print(f"\n{'=' * 80}")
    print(f"📊 TOTAL: {len(campos_unicos)} columnas en el Excel final")
    print("=" * 80)

