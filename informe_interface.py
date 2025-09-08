class InformeInterface:
    """Clase para representar una línea del archivo Excel"""
    
    def __init__(self, record_id, creation_date, record_type, operation, user_id, audit_creation_time, audit_id, audit_operation, organization_id, audit_record_type, user_key, user_type, version, workload, client_ip):
        self.record_id = record_id
        self.creation_date = creation_date
        self.record_type = record_type
        self.operation = operation
        self.user_id = user_id
        self.audit_creation_time = audit_creation_time
        self.audit_id = audit_id
        self.audit_operation = audit_operation
        self.organization_id = organization_id
        self.audit_record_type = audit_record_type
        self.user_key = user_key
        self.user_type = user_type
        self.version = version
        self.workload = workload
        self.client_ip = client_ip
        
    
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
        print(f"9 Organization ID: {self.organization_id}")
        print(f"10 Audit Record Type: {self.audit_record_type}")
        print(f"11 User Key: {self.user_key}")
        print(f"12 User Type: {self.user_type}")
        print(f"13 Version: {self.version}")
        print(f"14 Workload: {self.workload}")
        print(f"15 Client IP: {self.client_ip}")
        print("|" * 60)