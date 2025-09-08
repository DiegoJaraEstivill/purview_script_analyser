class InformeInterface:
    """Clase para representar una línea del archivo Excel"""
    
    def __init__(self, record_id, creation_date, record_type, operation, user_id, campos_audit):
        self.record_id = record_id
        self.creation_date = creation_date
        self.record_type = record_type
        self.operation = operation
        self.user_id = user_id
        self.campos_audit = campos_audit
        
    
    def mostrar_datos(self, numero_linea):
        """Muestra todos los datos de la línea de forma organizada"""
        print(f"Línea {numero_linea}: Data")
        print("=" * 60)
        print(f"1 RecordID su valor es: {self.record_id}")
        print(f"2 Creation date: {self.creation_date}")
        print(f"3 Record Type: {self.record_type}")
        print(f"4 Operation: {self.operation}")
        print(f"5 User ID: {self.user_id}")
        # Mostrar campos de auditoría de forma dinámica
        print("=== CAMPOS DE AUDITORÍA ===")
        contador = 6
        for key, value in self.campos_audit.items():
            # Convertir snake_case a title case para mejor legibilidad
            display_name = key.replace('_', ' ').title()
            print(f"{contador} {display_name}: {value}")
            contador += 1
        print("|" * 60)