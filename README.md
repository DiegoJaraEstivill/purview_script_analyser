# 📊 Purview Script Analyser

Analizador de archivos CSV de Microsoft Purview para extraer y procesar datos de auditoría.

## 🚀 Inicio Rápido

### Ejecutar el análisis
```bash
python formatear_purview.py
```

Esto procesará el archivo `7000LineasTextoPlano.csv` y generará un Excel con las primeras 5 filas.

## 📁 Estructura del Proyecto

```
purview_script_analyser/
│
├── 📄 formatear_purview.py          # Script principal (USAR ESTE)
├── 📄 data_extractor.py             # Extractor de datos CSV
├── 📄 excel_creator.py              # Creador de archivos Excel
├── 📄 informe_interface.py          # Clase de interfaz (deprecada)
│
├── 📂 Analisis_Real_CSV/            # ✅ Código NUEVO y CORRECTO
│   ├── csv_extractor.py             # Extractor simplificado
│   ├── simple_excel_creator.py      # Creador de Excel simplificado
│   ├── main_csv_processor.py        # Script alternativo
│   └── README.md                    # Documentación detallada
│
├── 📂 Analisis_Antiguo_Excel/       # ❌ Código ANTIGUO (archivado)
│   ├── data_extractor_antiguo.py    # Con bug de Excel
│   ├── excel_creator_antiguo.py     # 44 columnas
│   ├── formatear_purview_antiguo.py # Script antiguo
│   └── README.md                    # Explicación del bug
│
├── 📄 CONTEXTO_MIGRACION_CSV.md     # 📋 Documentación del cambio
│
└── 📄 7000LineasTextoPlano.csv      # Archivo de entrada (CSV)
```

## 🔧 Configuración

### Requisitos
```bash
pip install pandas openpyxl
```

### Archivo de entrada
- **Formato:** CSV de texto plano
- **Encoding:** UTF-8
- **Separador:** Comas (,)
- **Nombre:** `7000LineasTextoPlano.csv`

## 📋 Campos Extraídos (Fase 1)

El script actualmente extrae los primeros **5 campos básicos**:

1. **RecordId** - GUID único del registro
2. **CreationDate** - Fecha/hora en formato ISO 8601
3. **RecordType** - Tipo de registro (número)
4. **Operation** - Operación realizada
5. **UserId** - Email del usuario

## 📊 Salida

**Formato:** Excel (.xlsx)  
**Nombre:** `PurviewInf_DDMMAAAA_HHMM.xlsx`  
**Ejemplo:** `PurviewInf_16102025_1137.xlsx`

### Características del Excel generado:
- ✅ Headers con formato (azul, bold, blanco)
- ✅ Ancho de columnas auto-ajustado
- ✅ 5 columnas limpias sin corrupción
- ✅ Datos preservados en UTF-8

## ⚠️ Cambios Importantes

### 🔴 Bug Corregido (16/10/2025)

**Problema anterior:**
- ❌ Leía archivos Excel (.xlsx) en lugar de CSV
- ❌ Causaba corrupción de datos JSON
- ❌ Requería funciones de limpieza complejas
- ❌ Caracteres especiales se corrompían

**Solución actual:**
- ✅ Lee CSV directamente con pandas
- ✅ Sin corrupción de datos
- ✅ Código más simple y limpio
- ✅ Preserva encoding UTF-8

Ver `CONTEXTO_MIGRACION_CSV.md` para más detalles.

## 🎯 Fases del Proyecto

### ✅ Fase 1: Campos Básicos (ACTUAL)
- Extracción de 5 campos principales
- Lectura correcta de CSV
- Generación de Excel simple
- **Estado:** Completado

### 🔜 Fase 2: Análisis de JSON (FUTURO)
- Parsear campo `AuditData` (JSON)
- Extraer campos relevantes del JSON
- Expandir a más columnas
- **Estado:** Planificado

## 📖 Documentación Adicional

- `CONTEXTO_MIGRACION_CSV.md` - Historia del bug y migración
- `Analisis_Real_CSV/README.md` - Código de producción actual
- `Analisis_Antiguo_Excel/README.md` - Código archivado

## 🛠️ Uso Avanzado

### Procesar más filas
Edita `formatear_purview.py`:
```python
num_filas_procesar = 100  # Cambia de 5 a 100
```

### Ejecutar versión alternativa
```bash
cd Analisis_Real_CSV
python main_csv_processor.py
```

### Cambiar archivo de entrada
Edita `formatear_purview.py`:
```python
archivo_fuente = "tu_archivo.csv"
```

## 🐛 Troubleshooting

### Error: "Archivo no encontrado"
- Verifica que `7000LineasTextoPlano.csv` esté en la raíz del proyecto
- Usa rutas absolutas si es necesario

### Error: "UnicodeDecodeError"
- Asegúrate de que el CSV esté en UTF-8
- Si está en otra codificación, conviértelo primero

### Datos corruptos en el Excel
- **NO uses Excel para abrir/editar el CSV**
- Usa un editor de texto (VS Code, Notepad++)
- El CSV debe mantenerse como texto plano

## 📞 Contacto

Para preguntas o problemas, revisa:
1. `CONTEXTO_MIGRACION_CSV.md` - Contexto general
2. Los READMEs en las carpetas de análisis
3. Los comentarios en el código

---

**Última actualización:** 16/10/2025  
**Versión:** 2.0 (Post-migración CSV)

