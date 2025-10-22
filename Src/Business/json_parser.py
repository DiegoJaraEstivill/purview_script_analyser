import json
import re

def limpiar_json_string(json_string):
    """
    Limpia caracteres problemáticos del JSON sin corromper los datos
    
    Args:
        json_string (str): String JSON potencialmente sucio
        
    Returns:
        str: String JSON limpio
    """
    if not json_string or json_string == 'N/A':
        return json_string
    
    # Eliminar caracteres de control problemáticos (pero no tabs, newlines normales)
    json_limpio = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', json_string)
    
    return json_limpio

def flatten_json(json_obj, parent_key='', sep='_'):
    """
    Aplana un JSON anidado en un diccionario plano
    
    Args:
        json_obj (dict): Objeto JSON a aplanar
        parent_key (str): Prefijo para las claves (usado en recursión)
        sep (str): Separador para claves anidadas
        
    Returns:
        dict: Diccionario plano con todas las claves
        
    Ejemplo:
        Input:  {"AppAccessContext": {"AADSessionId": "123"}}
        Output: {"AppAccessContext_AADSessionId": "123"}
    """
    items = []
    
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, dict):
                # Si es un diccionario, recursión
                items.extend(flatten_json(value, new_key, sep=sep).items())
            elif isinstance(value, list):
                # Si es una lista, convertir a string
                items.append((new_key, str(value)))
            else:
                # Valor simple
                items.append((new_key, value))
    else:
        items.append((parent_key, json_obj))
    
    return dict(items)

def extraer_y_aplanar_audit_data(audit_data_string, fila_numero):
    """
    Extrae y aplana el JSON de AuditData
    
    Args:
        audit_data_string (str): String JSON del campo AuditData
        fila_numero (int): Número de fila para debug
        
    Returns:
        dict: Diccionario con todos los campos aplanados
    """
    campos_extraidos = {}
    
    try:
        if audit_data_string and audit_data_string != 'N/A' and audit_data_string.strip():
            # Limpiar el JSON
            audit_data_limpio = limpiar_json_string(audit_data_string)
            
            # Parsear el JSON
            audit_data_dict = json.loads(audit_data_limpio)
            
            # Aplanar el JSON (esto maneja automáticamente AppAccessContext y otros anidados)
            campos_extraidos = flatten_json(audit_data_dict)
            
            print(f"   OK JSON parseado: {len(campos_extraidos)} campos extraidos")
            
    except json.JSONDecodeError as e:
        print(f"   ERROR parseando JSON en fila {fila_numero}: {str(e)[:100]}")
        # Retornar diccionario vacío en caso de error
        campos_extraidos = {}
    except Exception as e:
        print(f"   ERROR inesperado en fila {fila_numero}: {str(e)[:100]}")
        campos_extraidos = {}
    
    return campos_extraidos

def obtener_campos_unicos(lista_registros):
    """
    Obtiene todos los campos únicos que aparecen en cualquier registro
    Útil para crear las columnas del Excel
    
    Args:
        lista_registros (list): Lista de diccionarios con datos aplanados
        
    Returns:
        list: Lista ordenada de todos los campos únicos
    """
    campos_unicos = set()
    
    for registro in lista_registros:
        campos_unicos.update(registro.keys())
    
    # Convertir a lista ordenada
    return sorted(list(campos_unicos))

def normalizar_registro(registro, campos_esperados):
    """
    Normaliza un registro para que tenga todos los campos esperados
    Rellena con 'N/A' los campos faltantes
    
    Args:
        registro (dict): Registro a normalizar
        campos_esperados (list): Lista de todos los campos que debe tener
        
    Returns:
        dict: Registro normalizado con todos los campos
    """
    registro_normalizado = {}
    
    for campo in campos_esperados:
        registro_normalizado[campo] = registro.get(campo, 'N/A')
    
    return registro_normalizado

