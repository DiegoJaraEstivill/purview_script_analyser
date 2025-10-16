# 📁 Análisis Real CSV - Código de Producción

## ✅ Este es el código CORRECTO a usar

Este directorio contiene el código **NUEVO** que lee archivos CSV de texto plano correctamente.

## 🎯 Objetivo

Extraer datos del archivo `7000LineasTextoPlano.csv` sin corrupción de datos.

## 📄 Archivos en este directorio:

### `csv_extractor.py`
**Función principal:** `extraer_campos_basicos_csv(archivo_csv, num_filas=5)`

- ✅ Lee CSV usando `pd.read_csv()` con parámetros correctos
- ✅ Extrae solo los primeros 5 campos
- ✅ No corrompe datos JSON
- ✅ Respeta encoding UTF-8

**Parámetros importantes:**
```python
pd.read_csv(
    archivo_csv,
    encoding='utf-8',        # Preserva caracteres especiales
    sep=',',                 # Separador de columnas
    quotechar='"',          # Respeta comillas para campos con comas
    escapechar='\\',        # Maneja caracteres escapados
    usecols=[...]           # Solo lee las columnas necesarias
)
```

### `simple_excel_creator.py`
**Función principal:** `crear_excel_simple(datos_registros)`

- ✅ Crea Excel con 5 columnas únicamente
- ✅ Formato profesional con headers azules
- ✅ Ajuste automático de ancho de columnas
- ✅ Nombre de archivo con timestamp

**Formato de salida:** `PurviewInf_DDMMAAAA_HHMM.xlsx`

### `main_csv_processor.py`
**Script principal de ejecución**

- Orquesta todo el proceso
- Lee 5 filas por defecto (configurable)
- Genera Excel de salida
- Muestra progreso detallado

## 🚀 Cómo usar

### Opción 1: Ejecutar desde esta carpeta
```bash
cd Analisis_Real_CSV
python main_csv_processor.py
```

### Opción 2: Ejecutar desde la raíz (actualizado)
```bash
python formatear_purview.py
```

## 📊 Campos extraídos (Fase 1)

1. **RecordId** - GUID único del registro
2. **CreationDate** - Fecha/hora de creación (ISO 8601)
3. **RecordType** - Tipo de registro (número)
4. **Operation** - Operación realizada (string)
5. **UserId** - Email del usuario

## 🔄 Flujo de procesamiento

```
7000LineasTextoPlano.csv
         ↓
   csv_extractor.py
         ↓
   [Datos limpios]
         ↓
 simple_excel_creator.py
         ↓
PurviewInf_DDMMAAAA_HHMM.xlsx
```

## ✨ Ventajas sobre el código antiguo

| Aspecto | Código Antiguo | Código Nuevo |
|---------|---------------|--------------|
| **Formato de entrada** | Excel (.xlsx) ❌ | CSV (.csv) ✅ |
| **Corrupción de datos** | Sí ❌ | No ✅ |
| **Encoding** | Problemas ❌ | UTF-8 limpio ✅ |
| **Campos JSON** | 39 campos rotos ❌ | N/A (Fase 2) ⏳ |
| **Complejidad** | Alta ❌ | Simple ✅ |
| **Funciones de limpieza** | Necesarias ❌ | Innecesarias ✅ |

## 🔜 Próximos pasos (Fase 2)

Una vez validada la extracción de los 5 campos básicos:

1. Analizar el campo `AuditData` (JSON)
2. Extraer campos relevantes del JSON
3. Expandir a más columnas según necesidad
4. Mantener la lectura correcta del CSV

## 📝 Ejemplo de salida

```
RecordId                              | CreationDate                  | RecordType | Operation      | UserId
--------------------------------------|-------------------------------|------------|----------------|---------------------------
0161b511-5aa1-44f6-ec56-08ddde268c9a | 2025-08-18T07:12:10.0000000Z | 6          | FileAccessed   | ext.ealanis@fesanco.cl
0406d38f-f2e7-47c0-18bf-08ddd039ee06 | 2025-07-31T13:55:38.0000000Z | 6          | FileSyncUp...  | ext.ealanis@fesanco.cl
...
```

## ⚠️ Importante

- **NO usar `pd.read_excel()`** para archivos CSV
- **SIEMPRE especificar `encoding='utf-8'`**
- **USAR `usecols`** para leer solo lo necesario
- **VALIDAR** que el archivo sea CSV, no Excel

---
*Creado: 16/10/2025*  
*Estado: Producción activa ✅*

