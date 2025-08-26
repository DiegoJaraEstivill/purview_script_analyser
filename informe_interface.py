class InformeInterface:
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
