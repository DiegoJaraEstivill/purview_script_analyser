import pandas as pd

class RegistroExcel:
    """Clase para representar una línea del archivo Excel"""
    
    def __init__(self, record_id, creation_date, record_type, operation, user_id):
        self.record_id = record_id
        self.creation_date = creation_date
        self.record_type = record_type
        self.operation = operation
        self.user_id = user_id
    
    def mostrar_datos(self, numero_linea):
        """Muestra todos los datos de la línea de forma organizada"""
        print(f"Línea {numero_linea}: Data")
        print(f"RecordID su valor es: {self.record_id}")
        print(f"Creation date: {self.creation_date}")
        print(f"Record Type: {self.record_type}")
        print(f"Operation: {self.operation}")
        print(f"User ID: {self.user_id}")
        print("-" * 60)

def main():
    # Leer el archivo Excel
    df = pd.read_excel("3000lineasDelimitadoComas.xlsx")
    
    # Tomar las primeras 4 filas
    primeras_4_filas = df.head(4)
    
    print("Mostrando las primeras 4 filas del archivo Excel:")
    print("=" * 60)
    
    # Crear objetos RegistroExcel para cada fila y mostrarlos
    for i, (index, row) in enumerate(primeras_4_filas.iterrows(), 1):
        registro = RegistroExcel(
            record_id=row.get('RecordId', 'N/A'),
            creation_date=row.get('CreationDate', 'N/A'),
            record_type=row.get('RecordType', 'N/A'),
            operation=row.get('Operation', 'N/A'),
            user_id=row.get('UserId', 'N/A')
        )
        
        registro.mostrar_datos(i)

if __name__ == "__main__":
    main()
