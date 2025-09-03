import pandas as pd
import json
import re
from informe_interface import InformeInterface
from excel_creator import crear_excel_purview

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

def main():
    # Leer el archivo Excel
    df = pd.read_excel("3000lineasDelimitadoComas.xlsx")
    
    # Tomar las primeras x filas
    filas_a_revisar = df.head(5)  # Procesamos 5 filas como ejemplo
    
    print("Mostrando las primeras x filas del archivo Excel:")
    print("=" * 60)
    
    # Lista para almacenar todos los registros para el Excel
    datos_registros = []
    
    # Crear objetos InformeInterface para cada fila y mostrarlos
    for i, (index, row) in enumerate(filas_a_revisar.iterrows(), 1):
        
        # Recorrer audit_data y extraer solo CreationTime e Id
        audit_data = row.get('AuditData', 'N/A')
        
        print("audit    data ", audit_data)
        # Extraer solo CreationTime e Id del JSON
        creation_time = 'N/A'
        audit_id = 'N/A'
        
        try:
            if audit_data and audit_data != 'N/A':
                # Limpiar el JSON antes de parsearlo
                audit_data_limpio = limpiar_json(audit_data)
                
                # Debug: mostrar el carácter en la posición problemática
                if len(audit_data) > 1144:
                    char_prob = audit_data[1144]
                    print(f"Carácter en posición 1144: '{char_prob}' (ord: {ord(char_prob)})")
                
                audit_data_dict = json.loads(audit_data_limpio)
                creation_time = audit_data_dict.get('CreationTime', 'N/A')
                audit_id = audit_data_dict.get('Id', 'N/A')
                print(f"DEBUG - Fila {i}: CreationTime={creation_time}, Id={audit_id}")
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error parsing JSON para fila {i}: {e}")
            print(f"Primeros 100 caracteres del JSON: {audit_data[:100] if audit_data else 'None'}")
            # Intentar mostrar el carácter problemático
            if audit_data and len(audit_data) > 1144:
                char_problemático = audit_data[1144]
                print(f"Carácter problemático en posición 1144: '{char_problemático}' (ord: {ord(char_problemático)})")
                
                # Intentar una limpieza manual en esa posición específica
                try:
                    audit_data_manual = audit_data[:1144] + audit_data[1145:]
                    audit_data_dict = json.loads(audit_data_manual)
                    creation_time = audit_data_dict.get('CreationTime', 'N/A')
                    audit_id = audit_data_dict.get('Id', 'N/A')
                    print(f"ÉXITO con limpieza manual - Fila {i}: CreationTime={creation_time}, Id={audit_id}")
                except Exception as e2:
                    print(f"Falló también la limpieza manual: {e2}")
        
        # Crear diccionario con los datos del registro
        registro_data = {
            'record_id': row.get('RecordId', 'N/A'),
            'creation_date': row.get('CreationDate', 'N/A'),
            'record_type': row.get('RecordType', 'N/A'),
            'operation': row.get('Operation', 'N/A'),
            'user_id': row.get('UserId', 'N/A'),
            'audit_creation_time': creation_time,
            'audit_id': audit_id
        }
        
        # Agregar a la lista para el Excel
        datos_registros.append(registro_data)
        
        # Crear objeto InformeInterface para mostrar en consola
        registro = InformeInterface(
            record_id=row.get('RecordId', 'N/A'),
            creation_date=row.get('CreationDate', 'N/A'),
            record_type=row.get('RecordType', 'N/A'),
            operation=row.get('Operation', 'N/A'),
            user_id=row.get('UserId', 'N/A'),
            audit_creation_time=creation_time,
            audit_id=audit_id
        )
        
        registro.mostrar_datos(i)
    
    # Crear el archivo Excel usando la función del módulo excel_creator
    print("\n" + "="*60)
    print("🚀 Generando archivo Excel...")
    nombre_archivo = crear_excel_purview(datos_registros)
    print(f"🎉 ¡Proceso completado exitosamente!")
    print(f"📄 Archivo generado: {nombre_archivo}")

if __name__ == "__main__":
    main()