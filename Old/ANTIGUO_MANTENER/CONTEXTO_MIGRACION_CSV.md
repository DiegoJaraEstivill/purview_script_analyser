# 📋 Contexto de Migración: Excel → CSV

## 🔴 Problema Identificado

**Fecha:** 16 de Octubre de 2025

### Bug Grave Detectado

El algoritmo estaba leyendo archivos **Excel (.xlsx)** en lugar de archivos de **texto plano (CSV/TXT)**, lo cual causaba:

1. **Corrupción de datos JSON**: El campo `AuditData` contiene JSON con comas internas. Al abrir CSV en Excel y guardarlo como .xlsx, Excel interpreta mal las comas y rompe el formato.

2. **Caracteres corruptos**: Pérdida de encoding UTF-8, caracteres especiales se convierten en caracteres raros que rompen el parsing JSON.

3. **Separación incorrecta de campos**: Un campo con comas se convertía en múltiples columnas, destruyendo la estructura de datos.

4. **Necesidad de código de limpieza**: El archivo `data_extractor.py` tenía funciones complejas (`limpiar_json()`) intentando reparar datos que nunca debieron corromperse.

---

## 📂 Estructura del CSV Original

**Archivo fuente:** `7000LineasTextoPlano.csv`

### Campos (8 columnas):
```
RecordId,CreationDate,RecordType,Operation,UserId,AuditData,AssociatedAdminUnits,AssociatedAdminUnitsNames
```

### Primeros 5 campos a extraer (Fase 1):
1. **RecordId** - GUID del registro
2. **CreationDate** - Fecha de creación (formato ISO)
3. **RecordType** - Tipo de registro (número)
4. **Operation** - Operación realizada (string)
5. **UserId** - Email del usuario

El campo 6 (`AuditData`) es un JSON complejo que se analizará en fases posteriores.

---

## 🔧 Solución Implementada

### Cambio Principal:
```python
# ❌ ANTES (MALO):
df = pd.read_excel(archivo_excel)

# ✅ AHORA (CORRECTO):
df = pd.read_csv(
    archivo_csv,
    encoding='utf-8',
    sep=',',
    quotechar='"',
    escapechar='\\',
    usecols=['RecordId', 'CreationDate', 'RecordType', 'Operation', 'UserId']
)
```

### Beneficios:
- ✅ **Sin corrupción de datos**
- ✅ **Lectura directa del CSV** sin intermediarios
- ✅ **Respeto del formato UTF-8**
- ✅ **Manejo correcto de campos con comas** (usando quotechar)
- ✅ **Código más simple** (sin necesidad de `limpiar_json()`)

---

## 📁 Organización del Proyecto

### Carpeta `Analisis_Antiguo_Excel/`
Contiene el código antiguo que leía archivos Excel (.xlsx):
- `data_extractor.py` - Con funciones `limpiar_json()` y parsing JSON de 39 campos
- `excel_creator.py` - Creaba Excel con 44 columnas
- `formatear_purview.py` - Script principal antiguo
- `informe_interface.py` - Clase de interfaz compleja

**Estado:** Archivado como referencia, NO usar en producción

### Carpeta `Analisis_Real_CSV/`
Contiene el código NUEVO que lee CSV correctamente:
- `csv_extractor.py` - Extrae solo los primeros 5 campos del CSV
- `simple_excel_creator.py` - Crea Excel con 5 columnas
- `main_csv_processor.py` - Script principal simplificado

**Estado:** Código de producción actual

### Archivos en raíz (actualizados):
- `data_extractor.py` - Versión actualizada que lee CSV
- `excel_creator.py` - Versión simplificada
- `formatear_purview.py` - Script principal actualizado

---

## 🎯 Próximos Pasos

### Fase 1: ✅ Extracción básica (5 campos)
- Leer CSV correctamente
- Extraer RecordId, CreationDate, RecordType, Operation, UserId
- Generar Excel con 5 columnas

### Fase 2: 🔜 Análisis de AuditData JSON
- Una vez validada la lectura correcta del CSV
- Parsear el campo `AuditData` (JSON)
- Extraer campos relevantes del JSON
- Expandir a más columnas según necesidad

---

## 📊 Resultados Esperados

**Input:** `7000LineasTextoPlano.csv` (7000+ registros)

**Output:** `PurviewInf_DDMMAAAA_HHMM.xlsx` con:
- 5 filas de datos
- 5 columnas: RecordId, CreationDate, RecordType, Operation, UserId
- Sin datos corruptos
- Sin caracteres raros
- Formato limpio y legible

---

## ⚠️ Lecciones Aprendidas

1. **Nunca usar Excel como intermediario** para archivos CSV con JSON o datos complejos
2. **Leer directamente desde CSV** usando pandas con parámetros correctos
3. **Especificar encoding** explícitamente (UTF-8)
4. **Usar `usecols`** para leer solo las columnas necesarias
5. **Validar formato de entrada** antes de procesar miles de registros

---

**Documentado por:** AI Assistant  
**Última actualización:** 16/10/2025

