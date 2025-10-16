import pandas as pd

def extraer_campos_basicos_csv(archivo_csv, num_filas=5):
    """
    Extrae los primeros 5 campos del archivo CSV de texto plano
    
    Args:
        archivo_csv (str): Ruta al archivo CSV fuente
        num_filas (int): Número de filas a procesar
        
    Returns:
        list: Lista de diccionarios con los datos de cada registro
    """
    print(f"📂 Leyendo archivo CSV: {archivo_csv}")
    
    # Leer el archivo CSV correctamente
    # usecols: solo leer las primeras 5 columnas para evitar problemas con el JSON
    df = pd.read_csv(
        archivo_csv,
        encoding='utf-8',
        sep=',',
        quotechar='"',
        escapechar='\\',
        usecols=['RecordId', 'CreationDate', 'RecordType', 'Operation', 'UserId']
    )
    
    print(f"📊 Total de filas en el archivo: {len(df)}")
    
    # Tomar las primeras x filas
    filas_a_revisar = df.head(num_filas)
    
    print(f"🔍 Procesando {len(filas_a_revisar)} filas...")
    print("=" * 60)
    
    # Lista para almacenar resultados
    lista_datos = []
    
    # Procesar cada fila
    for i, (index, row) in enumerate(filas_a_revisar.iterrows(), 1):
        print(f"\n🔄 Procesando fila {i}...")
        
        # Crear diccionario con los 5 campos
        datos = {
            'RecordId': row.get('RecordId', 'N/A'),
            'CreationDate': row.get('CreationDate', 'N/A'),
            'RecordType': row.get('RecordType', 'N/A'),
            'Operation': row.get('Operation', 'N/A'),
            'UserId': row.get('UserId', 'N/A'),
        }
        
        # Agregar a la lista
        lista_datos.append(datos)
        
        # Mostrar datos procesados
        print(f"   ✓ RecordId: {datos['RecordId'][:40]}..." if len(str(datos['RecordId'])) > 40 else f"   ✓ RecordId: {datos['RecordId']}")
        print(f"   ✓ CreationDate: {datos['CreationDate']}")
        print(f"   ✓ RecordType: {datos['RecordType']}")
        print(f"   ✓ Operation: {datos['Operation']}")
        print(f"   ✓ UserId: {datos['UserId']}")
        print(f"✅ Fila {i} procesada correctamente")
    
    print(f"\n{'=' * 60}")
    print(f"🎯 Extracción completada: {len(lista_datos)} registros procesados")
    print(f"{'=' * 60}")
    
    return lista_datos

