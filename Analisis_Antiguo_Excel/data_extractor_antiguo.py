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
    # Inicializar todos los 39 campos con N/A
    campos_audit = {
        # Campos existentes (10)
        'creation_time': 'N/A',
        'audit_id': 'N/A',
        'audit_operation': 'N/A',
        'organization_id': 'N/A',
        'audit_record_type': 'N/A',
        'user_key': 'N/A',
        'user_type': 'N/A',
        'version': 'N/A',
        'workload': 'N/A',
        'client_ip': 'N/A',
        # Nuevos campos (29)
        'audit_user_id': 'N/A',
        'authentication_type': 'N/A',
        'browser_name': 'N/A',
        'browser_version': 'N/A',
        'correlation_id': 'N/A',
        'event_source': 'N/A',
        'geo_location': 'N/A',
        'is_managed_device': 'N/A',
        'item_type': 'N/A',
        'list_id': 'N/A',
        'list_item_unique_id': 'N/A',
        'platform': 'N/A',
        'site': 'N/A',
        'user_agent': 'N/A',
        'web_id': 'N/A',
        'device_display_name': 'N/A',
        'event_signature': 'N/A',
        'machine_id': 'N/A',
        'file_sync_bytes_committed': 'N/A',
        'high_priority_media_processing': 'N/A',
        'implicit_share': 'N/A',
        'list_base_type': 'N/A',
        'list_server_template': 'N/A',
        'source_relative_url': 'N/A',
        'source_file_name': 'N/A',
        'source_file_extension': 'N/A',
        'application_display_name': 'N/A',
        'site_url': 'N/A',
        'object_id': 'N/A'
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
            
            # Extraer todos los 39 campos del JSON
            # Campos existentes (10)
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
            # Nuevos campos (29)
            campos_audit['audit_user_id'] = audit_data_dict.get('UserId', 'N/A')
            campos_audit['authentication_type'] = audit_data_dict.get('AuthenticationType', 'N/A')
            campos_audit['browser_name'] = audit_data_dict.get('BrowserName', 'N/A')
            campos_audit['browser_version'] = audit_data_dict.get('BrowserVersion', 'N/A')
            campos_audit['correlation_id'] = audit_data_dict.get('CorrelationId', 'N/A')
            campos_audit['event_source'] = audit_data_dict.get('EventSource', 'N/A')
            campos_audit['geo_location'] = audit_data_dict.get('GeoLocation', 'N/A')
            campos_audit['is_managed_device'] = audit_data_dict.get('IsManagedDevice', 'N/A')
            campos_audit['item_type'] = audit_data_dict.get('ItemType', 'N/A')
            campos_audit['list_id'] = audit_data_dict.get('ListId', 'N/A')
            campos_audit['list_item_unique_id'] = audit_data_dict.get('ListItemUniqueId', 'N/A')
            campos_audit['platform'] = audit_data_dict.get('Platform', 'N/A')
            campos_audit['site'] = audit_data_dict.get('Site', 'N/A')
            campos_audit['user_agent'] = audit_data_dict.get('UserAgent', 'N/A')
            campos_audit['web_id'] = audit_data_dict.get('WebId', 'N/A')
            campos_audit['device_display_name'] = audit_data_dict.get('DeviceDisplayName', 'N/A')
            campos_audit['event_signature'] = audit_data_dict.get('EventSignature', 'N/A')
            campos_audit['machine_id'] = audit_data_dict.get('MachineId', 'N/A')
            campos_audit['file_sync_bytes_committed'] = audit_data_dict.get('FileSyncBytesCommitted', 'N/A')
            campos_audit['high_priority_media_processing'] = audit_data_dict.get('HighPriorityMediaProcessing', 'N/A')
            campos_audit['implicit_share'] = audit_data_dict.get('ImplicitShare', 'N/A')
            campos_audit['list_base_type'] = audit_data_dict.get('ListBaseType', 'N/A')
            campos_audit['list_server_template'] = audit_data_dict.get('ListServerTemplate', 'N/A')
            campos_audit['source_relative_url'] = audit_data_dict.get('SourceRelativeUrl', 'N/A')
            campos_audit['source_file_name'] = audit_data_dict.get('SourceFileName', 'N/A')
            campos_audit['source_file_extension'] = audit_data_dict.get('SourceFileExtension', 'N/A')
            campos_audit['application_display_name'] = audit_data_dict.get('ApplicationDisplayName', 'N/A')
            campos_audit['site_url'] = audit_data_dict.get('SiteUrl', 'N/A')
            campos_audit['object_id'] = audit_data_dict.get('ObjectId', 'N/A')
            
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
                
                # Extraer todos los 39 campos con limpieza manual
                # Campos existentes (10)
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
                # Nuevos campos (29)
                campos_audit['audit_user_id'] = audit_data_dict.get('UserId', 'N/A')
                campos_audit['authentication_type'] = audit_data_dict.get('AuthenticationType', 'N/A')
                campos_audit['browser_name'] = audit_data_dict.get('BrowserName', 'N/A')
                campos_audit['browser_version'] = audit_data_dict.get('BrowserVersion', 'N/A')
                campos_audit['correlation_id'] = audit_data_dict.get('CorrelationId', 'N/A')
                campos_audit['event_source'] = audit_data_dict.get('EventSource', 'N/A')
                campos_audit['geo_location'] = audit_data_dict.get('GeoLocation', 'N/A')
                campos_audit['is_managed_device'] = audit_data_dict.get('IsManagedDevice', 'N/A')
                campos_audit['item_type'] = audit_data_dict.get('ItemType', 'N/A')
                campos_audit['list_id'] = audit_data_dict.get('ListId', 'N/A')
                campos_audit['list_item_unique_id'] = audit_data_dict.get('ListItemUniqueId', 'N/A')
                campos_audit['platform'] = audit_data_dict.get('Platform', 'N/A')
                campos_audit['site'] = audit_data_dict.get('Site', 'N/A')
                campos_audit['user_agent'] = audit_data_dict.get('UserAgent', 'N/A')
                campos_audit['web_id'] = audit_data_dict.get('WebId', 'N/A')
                campos_audit['device_display_name'] = audit_data_dict.get('DeviceDisplayName', 'N/A')
                campos_audit['event_signature'] = audit_data_dict.get('EventSignature', 'N/A')
                campos_audit['machine_id'] = audit_data_dict.get('MachineId', 'N/A')
                campos_audit['file_sync_bytes_committed'] = audit_data_dict.get('FileSyncBytesCommitted', 'N/A')
                campos_audit['high_priority_media_processing'] = audit_data_dict.get('HighPriorityMediaProcessing', 'N/A')
                campos_audit['implicit_share'] = audit_data_dict.get('ImplicitShare', 'N/A')
                campos_audit['list_base_type'] = audit_data_dict.get('ListBaseType', 'N/A')
                campos_audit['list_server_template'] = audit_data_dict.get('ListServerTemplate', 'N/A')
                campos_audit['source_relative_url'] = audit_data_dict.get('SourceRelativeUrl', 'N/A')
                campos_audit['source_file_name'] = audit_data_dict.get('SourceFileName', 'N/A')
                campos_audit['source_file_extension'] = audit_data_dict.get('SourceFileExtension', 'N/A')
                campos_audit['application_display_name'] = audit_data_dict.get('ApplicationDisplayName', 'N/A')
                campos_audit['site_url'] = audit_data_dict.get('SiteUrl', 'N/A')
                campos_audit['object_id'] = audit_data_dict.get('ObjectId', 'N/A')
                
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
        
        # Crear objeto InformeInterface con todos los campos
        registro = InformeInterface(
            record_id=row.get('RecordId', 'N/A'),
            creation_date=row.get('CreationDate', 'N/A'),
            record_type=row.get('RecordType', 'N/A'),
            operation=row.get('Operation', 'N/A'),
            user_id=row.get('UserId', 'N/A'),
            campos_audit=campos_audit  # Pasamos todo el diccionario
        )
        
        # Agregar a lista de objetos InformeInterface
        lista_registros_interface.append(registro)
        
        # Crear diccionario para el Excel (ahora incluye todos los 39 campos del audit)
        datos_excel = {
            'record_id': row.get('RecordId', 'N/A'),
            'creation_date': row.get('CreationDate', 'N/A'),
            'record_type': row.get('RecordType', 'N/A'),
            'operation': row.get('Operation', 'N/A'),
            'user_id': row.get('UserId', 'N/A'),
        }
        # Agregar todos los campos del audit al diccionario
        datos_excel.update(campos_audit)
        
        # Agregar a lista de datos para Excel
        lista_datos_para_excel.append(datos_excel)
        
        print(f"✅ Fila {i} procesada correctamente")
    
    print(f"\n🎯 Extracción completada: {len(lista_registros_interface)} registros procesados")
    
    return lista_registros_interface, lista_datos_para_excel