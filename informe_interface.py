class InformeInterface:
    """Clase para representar una línea del archivo Excel"""
    
    def __init__(self, record_id, creation_date, record_type, operation, user_id, audit_creation_time, audit_id, audit_operation):
        self.record_id = record_id
        self.creation_date = creation_date
        self.record_type = record_type
        self.operation = operation
        self.user_id = user_id
        self.audit_creation_time = audit_creation_time
        self.audit_id = audit_id
        self.audit_operation = audit_operation
        
    
    def mostrar_datos(self, numero_linea):
        """Muestra todos los datos de la línea de forma organizada"""
        print(f"Línea {numero_linea}: Data")
        print("=" * 60)
        print(f"1 RecordID su valor es: {self.record_id}")
        print(f"2 Creation date: {self.creation_date}")
        print(f"3 Record Type: {self.record_type}")
        print(f"4 Operation: {self.operation}")
        print(f"5 User ID: {self.user_id}")
        print(f"6 Audit Creation Time: {self.audit_creation_time}")
        print(f"7 Audit ID: {self.audit_id}")
        print(f"8 Audit Operation: {self.audit_operation}")
        print("|" * 60)