import pandas as pd
from informe_interface import InformeInterface

def main():
    # Leer el archivo Excel
    df = pd.read_excel("3000lineasDelimitadoComas.xlsx")
    
    # Tomar las primeras 4 filas
    primeras_4_filas = df.head(4)
    
    print("Mostrando las primeras 4 filas del archivo Excel:")
    print("=" * 60)
    
    # Crear objetos InformeInterface para cada fila y mostrarlos
    for i, (index, row) in enumerate(primeras_4_filas.iterrows(), 1):
        registro = InformeInterface(
            record_id=row.get('RecordId', 'N/A'),
            creation_date=row.get('CreationDate', 'N/A'),
            record_type=row.get('RecordType', 'N/A'),
            operation=row.get('Operation', 'N/A'),
            user_id=row.get('UserId', 'N/A')
        )
        
        registro.mostrar_datos(i)

if __name__ == "__main__":
    main()
