import pandas as pd
import json
import re
from informe_interface import InformeInterface

def limpiar_json(json_string):
    """Limpia caracteres de control inválidos del JSON"""
    if not json_string or json_string == 'N/A':
        return json_string
    
    # Método más agresivo para limpiar caracteres problemáticos
    # Reemplazar caracteres de control y caracteres no ASCII problemáticos
    json_limpio = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', json_string)
    
    # También limpiar caracteres específicos que pueden causar problemas
    json_limpio = json_limpio.replace('\x00', '').replace('\x09', '').replace('\x0B', '')
    
    # Si aún hay problemas, intentar limpiar todo lo que no sea ASCII imprimible básico
    # pero preservando caracteres JSON importantes
    json_limpio = ''.join(char for char in json_limpio if ord(char) >= 32 or char in ['\t', '\n', '\r'])
    
    return json_limpio

def extraer_datos_audit(audit_data, fila_numero):
    """
    Extrae múltiples campos del JSON de AuditData
    
    Args:
        audit_data: JSON string con los datos de auditoría
        fila_numero: Número de fila para debug
        
    Returns:
        dict: Diccionario con todos los campos extraídos
    """
    # Inicializar todos los campos con N/A
    campos_audit = {
        'creation_time': 'N/A',
        'audit_id': 'N/A',
        'audit_operation': 'N/A',
        'organization_id': 'N/A',
        'audit_record_type': 'N/A',
        'user_key': 'N/A',
        'user_type': 'N/A',
        'version': 'N/A',
        'workload': 'N/A',
        'client_ip': 'N/A'
    }
    
    try:
        if audit_data and audit_data != 'N/A':
            # Limpiar el JSON antes de parsearlo
            audit_data_limpio = limpiar_json(audit_data)
            
            # Debug: mostrar el carácter en la posición problemática
            if len(audit_data) > 1144:
                char_prob = audit_data[1144]
                print(f"Carácter en posición 1144: '{char_prob}' (ord: {ord(char_prob)})")
            
            audit_data_dict = json.loads(audit_data_limpio)
            
            # Extraer todos los campos
            campos_audit['creation_time'] = audit_data_dict.get('CreationTime', 'N/A')
            campos_audit['audit_id'] = audit_data_dict.get('Id', 'N/A')
            campos_audit['audit_operation'] = audit_data_dict.get('Operation', 'N/A')
            campos_audit['organization_id'] = audit_data_dict.get('OrganizationId', 'N/A')
            campos_audit['audit_record_type'] = audit_data_dict.get('RecordType', 'N/A')
            campos_audit['user_key'] = audit_data_dict.get('UserKey', 'N/A')
            campos_audit['user_type'] = audit_data_dict.get('UserType', 'N/A')
            campos_audit['version'] = audit_data_dict.get('Version', 'N/A')
            campos_audit['workload'] = audit_data_dict.get('Workload', 'N/A')
            campos_audit['client_ip'] = audit_data_dict.get('ClientIP', 'N/A')
            
            print(f"DEBUG - Fila {fila_numero}: Extraídos {len([v for v in campos_audit.values() if v != 'N/A'])} campos del JSON")
            
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error parsing JSON para fila {fila_numero}: {e}")
        print(f"Primeros 100 caracteres del JSON: {audit_data[:100] if audit_data else 'None'}")
        
        # Intentar mostrar el carácter problemático
        if audit_data and len(audit_data) > 1144:
            char_problemático = audit_data[1144]
            print(f"Carácter problemático en posición 1144: '{char_problemático}' (ord: {ord(char_problemático)})")
            
            # Intentar una limpieza manual en esa posición específica
            try:
                audit_data_manual = audit_data[:1144] + audit_data[1145:]
                audit_data_dict = json.loads(audit_data_manual)
                
                # Extraer todos los campos con limpieza manual
                campos_audit['creation_time'] = audit_data_dict.get('CreationTime', 'N/A')
                campos_audit['audit_id'] = audit_data_dict.get('Id', 'N/A')
                campos_audit['audit_operation'] = audit_data_dict.get('Operation', 'N/A')
                campos_audit['organization_id'] = audit_data_dict.get('OrganizationId', 'N/A')
                campos_audit['audit_record_type'] = audit_data_dict.get('RecordType', 'N/A')
                campos_audit['user_key'] = audit_data_dict.get('UserKey', 'N/A')
                campos_audit['user_type'] = audit_data_dict.get('UserType', 'N/A')
                campos_audit['version'] = audit_data_dict.get('Version', 'N/A')
                campos_audit['workload'] = audit_data_dict.get('Workload', 'N/A')
                campos_audit['client_ip'] = audit_data_dict.get('ClientIP', 'N/A')
                
                print(f"ÉXITO con limpieza manual - Fila {fila_numero}: Extraídos {len([v for v in campos_audit.values() if v != 'N/A'])} campos")
            except Exception as e2:
                print(f"Falló también la limpieza manual: {e2}")
    
    return campos_audit

def getdata_from_base_excel(archivo_excel, num_filas=5):
    """
    Extrae datos del archivo Excel base y crea objetos InformeInterface
    
    Args:
        archivo_excel (str): Ruta al archivo Excel fuente
        num_filas (int): Número de filas a procesar
        
    Returns:
        tuple: (lista_registros_interface, lista_datos_para_excel)
    """
    print(f"📂 Leyendo archivo: {archivo_excel}")
    
    # Leer el archivo Excel
    df = pd.read_excel(archivo_excel)
    
    # Tomar las primeras x filas
    filas_a_revisar = df.head(num_filas)
    
    print(f"📊 Procesando {len(filas_a_revisar)} filas...")
    print("=" * 60)
    
    # Listas para almacenar resultados
    lista_registros_interface = []
    lista_datos_para_excel = []
    
    # Procesar cada fila
    for i, (index, row) in enumerate(filas_a_revisar.iterrows(), 1):
        print(f"\n🔄 Procesando fila {i}...")
        
        # Obtener audit_data
        audit_data = row.get('AuditData', 'N/A')
        print(f"audit data: {audit_data}")
        
        # Extraer datos del JSON de auditoría (ahora incluye múltiples campos)
        campos_audit = extraer_datos_audit(audit_data, i)
        
        # Crear objeto InformeInterface
        registro = InformeInterface(
            record_id=row.get('RecordId', 'N/A'),
            creation_date=row.get('CreationDate', 'N/A'),
            record_type=row.get('RecordType', 'N/A'),
            operation=row.get('Operation', 'N/A'),
            user_id=row.get('UserId', 'N/A'),
            audit_creation_time=campos_audit['creation_time'],
            audit_id=campos_audit['audit_id'],
            audit_operation=campos_audit['audit_operation'],
            organization_id=campos_audit['organization_id'],
            audit_record_type=campos_audit['audit_record_type'],
            user_key=campos_audit['user_key'],
            user_type=campos_audit['user_type'],
            version=campos_audit['version'],
            workload=campos_audit['workload'],
            client_ip=campos_audit['client_ip']
        )
        
        # Agregar a lista de objetos InformeInterface
        lista_registros_interface.append(registro)
        
        # Crear diccionario para el Excel (ahora incluye múltiples campos del audit)
        datos_excel = {
            'record_id': row.get('RecordId', 'N/A'),
            'creation_date': row.get('CreationDate', 'N/A'),
            'record_type': row.get('RecordType', 'N/A'),
            'operation': row.get('Operation', 'N/A'),
            'user_id': row.get('UserId', 'N/A'),
            'audit_creation_time': campos_audit['creation_time'],
            'audit_id': campos_audit['audit_id'],
            'audit_operation': campos_audit['audit_operation'],
            'organization_id': campos_audit['organization_id'],
            'audit_record_type': campos_audit['audit_record_type'],
            'user_key': campos_audit['user_key'],
            'user_type': campos_audit['user_type'],
            'version': campos_audit['version'],
            'workload': campos_audit['workload'],
            'client_ip': campos_audit['client_ip']
        }
        
        # Agregar a lista de datos para Excel
        lista_datos_para_excel.append(datos_excel)
        
        print(f"✅ Fila {i} procesada correctamente")
    
    print(f"\n🎯 Extracción completada: {len(lista_registros_interface)} registros procesados")
    
    return lista_registros_interface, lista_datos_para_excel