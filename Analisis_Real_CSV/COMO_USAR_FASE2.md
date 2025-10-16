# 🚀 Cómo Usar la Fase 2: Análisis Completo

## ✅ Implementación Completada

La **Fase 2** está lista y funcionando. Extrae **57 columnas** del CSV con JSON aplanado.

---

## 🎯 Ejecución Rápida

### Desde la carpeta `Analisis_Real_CSV`:
```bash
cd Analisis_Real_CSV
python main_fase2_completo.py
```

### Desde la raíz del proyecto:
```bash
python Analisis_Real_CSV/main_fase2_completo.py
```

---

## 📊 ¿Qué Genera?

### Archivos de Salida:

1. **Excel Completo:** `PurviewInf_Completo_DDMMAAAA_HHMM.xlsx`
   - 5 filas de datos (configurable)
   - 57 columnas con JSON aplanado
   - Headers formateados
   - Columnas auto-ajustadas

2. **Resumen de Columnas:** `resumen_columnas_DDMMAAAA_HHMM.txt`
   - Lista de las 57 columnas generadas
   - Útil para referencia

---

## 📋 Columnas Generadas (57 total)

### BLOQUE 1: Campos Base del CSV (5)
- RecordId
- CreationDate
- RecordType
- Operation
- UserId

### BLOQUE 2: AppAccessContext (9)
- AppAccessContext_AADSessionId
- AppAccessContext_AuthTime
- AppAccessContext_ClientAppId
- AppAccessContext_ClientAppName
- AppAccessContext_CorrelationId
- AppAccessContext_DeviceId
- AppAccessContext_TokenIssuedAtTime
- AppAccessContext_UniqueTokenId
- AppAccessContext_UserObjectId

### BLOQUE 3: Campos del JSON AuditData (41)
- ApplicationDisplayName
- ApplicationId
- Audit_Id (era "Id" en el JSON)
- Audit_Operation (era "Operation" en el JSON)
- Audit_RecordType (era "RecordType" en el JSON)
- Audit_UserId (era "UserId" en el JSON)
- AuthenticationType
- BrowserName
- BrowserVersion
- ClientIP
- CorrelationId
- CreationTime
- DeviceDisplayName
- DoNotDistributeEvent
- EventSignature
- EventSource
- FileSyncBytesCommitted
- GeoLocation
- HighPriorityMediaProcessing
- ImplicitShare
- IsManagedDevice
- ItemType
- ListBaseType
- ListId
- ListItemUniqueId
- ListServerTemplate
- MachineId
- ObjectId
- OrganizationId
- Platform
- Site
- SiteUrl
- SourceFileExtension
- SourceFileName
- SourceRelativeUrl
- UserAgent
- UserKey
- UserType
- Version
- WebId
- Workload

### BLOQUE 4: Campos Finales del CSV (2)
- AssociatedAdminUnits
- AssociatedAdminUnitsNames

---

## ⚙️ Configuración

### Cambiar el número de filas a procesar:

Edita `main_fase2_completo.py`, línea 21:

```python
num_filas_procesar = 5  # Cambia a 100, 1000, o 7237 (todas)
```

### Ejemplos:
```python
num_filas_procesar = 100    # Procesar 100 filas
num_filas_procesar = 1000   # Procesar 1000 filas
num_filas_procesar = 7237   # Procesar TODO el archivo
```

---

## 🔍 Características Implementadas

✅ **Lectura directa de CSV** (no Excel, sin corrupción)  
✅ **Parsing completo del JSON AuditData**  
✅ **Flattening de JSON anidado** (AppAccessContext)  
✅ **Manejo de campos duplicados** (renombrados con prefijo "Audit_")  
✅ **Normalización de registros** (todos tienen las mismas columnas)  
✅ **Valores faltantes** (rellenados con "N/A")  
✅ **Encoding UTF-8 preservado**  
✅ **Headers formateados** (azul, bold, centrado)  
✅ **Columnas auto-ajustadas**  
✅ **Fila de headers congelada** (para scroll)  

---

## 📊 Resultado del Test

### Prueba realizada: ✅ EXITOSA

```
📊 Total de filas procesadas: 5
📋 Total de columnas: 57
📄 Excel generado: PurviewInf_Completo_16102025_1215.xlsx
📄 Resumen generado: resumen_columnas_16102025_1215.txt
```

### Campos JSON extraídos por fila:
- Fila 1: 44 campos del JSON
- Fila 2: 46 campos del JSON
- Fila 3: 43 campos del JSON
- Fila 4: 44 campos del JSON
- Fila 5: 43 campos del JSON

**Total único:** 57 columnas (algunos campos no aparecen en todas las filas)

---

## 🎯 Manejo de Casos Especiales

### 1. Campos Duplicados
Algunos campos aparecen tanto en el CSV como en el JSON:

| Campo en CSV | Campo en JSON | Columna Final |
|-------------|---------------|---------------|
| Operation   | Operation     | `Operation` (CSV) + `Audit_Operation` (JSON) |
| UserId      | UserId        | `UserId` (CSV) + `Audit_UserId` (JSON) |
| RecordType  | RecordType    | `RecordType` (CSV) + `Audit_RecordType` (JSON) |
| Id (N/A en CSV) | Id        | `Audit_Id` (JSON) |

**Solución:** Campos del JSON renombrados con prefijo `Audit_` para evitar conflictos.

### 2. JSON Anidado
El objeto `AppAccessContext` dentro del JSON se aplana con prefijo:

```json
{
  "AppAccessContext": {
    "AADSessionId": "123"
  }
}
```
**Se convierte en:**
- Columna: `AppAccessContext_AADSessionId`
- Valor: `123`

### 3. Campos Faltantes
Si un registro no tiene cierto campo:
- **Valor:** `N/A`

---

## 💡 Próximos Pasos

1. **Validar el Excel generado:**
   - Abre `PurviewInf_Completo_16102025_1215.xlsx`
   - Verifica que los datos se vean correctos
   - Comprueba que no haya corrupción

2. **Si todo está correcto:**
   - Edita `num_filas_procesar` para procesar más filas
   - Ejecuta de nuevo

3. **Para análisis:**
   - Usa filtros en Excel
   - Crea tablas dinámicas
   - Exporta a Power BI o herramientas de análisis

---

## 🆘 Troubleshooting

### Error: "Archivo no encontrado"
**Solución:** Verifica que `7000LineasTextoPlano.csv` esté en la raíz del proyecto

### Error: "JSON decode error"
**Solución:** Algunas filas pueden tener JSON malformado, el script lo maneja automáticamente poniendo `N/A`

### Excel muy grande
**Solución:** Reduce `num_filas_procesar` temporalmente

---

## 📚 Archivos del Proyecto

```
Analisis_Real_CSV/
├── json_flattener.py           # Funciones de parsing y flattening
├── csv_extractor_completo.py   # Extractor con JSON completo
├── excel_creator_completo.py   # Generador de Excel completo
├── main_fase2_completo.py      # Script principal ⭐
├── README_FASE2.md             # Documentación conceptual
└── COMO_USAR_FASE2.md          # Esta guía
```

---

**Última actualización:** 16/10/2025  
**Estado:** ✅ Implementado y Probado

