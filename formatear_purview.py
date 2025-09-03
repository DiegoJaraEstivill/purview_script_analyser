import pandas as pd
import json
from informe_interface import InformeInterface

def main():
    # Leer el archivo Excel
    df = pd.read_excel("3000lineasDelimitadoComas.xlsx")
    
    # Tomar las primeras x filas
    filas_a_revisar = df.head(2)
    
    print("Mostrando las primeras x filas del archivo Excel:")
    print("=" * 60)
    
    # Crear objetos InformeInterface para cada fila y mostrarlos
    for i, (index, row) in enumerate(filas_a_revisar.iterrows(), 1):
        
        # Recorrer audit_data y extraer solo CreationTime e Id
        audit_data = row.get('AuditData', 'N/A')
        
        # Extraer solo CreationTime e Id del JSON
        creation_time = 'N/A'
        audit_id = 'N/A'
        
        try:
            if audit_data and audit_data != 'N/A':
                audit_data_dict = json.loads(audit_data)
                creation_time = audit_data_dict.get('CreationTime', 'N/A')
                audit_id = audit_data_dict.get('Id', 'N/A')
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error parsing JSON: {e}")
        
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

if __name__ == "__main__":
    main()
