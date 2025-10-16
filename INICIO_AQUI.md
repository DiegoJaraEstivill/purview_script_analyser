# 🚀 INICIO AQUÍ - Guía Rápida

## ⚡ Ejecutar el Análisis (30 segundos)

```bash
python formatear_purview.py
```

✅ **Eso es todo!** El script generará un archivo Excel con los datos.

---

## 📁 ¿Qué Archivos Necesito?

### Archivo de Entrada (Ya lo tienes)
- ✅ `7000LineasTextoPlano.csv` - Archivo CSV de Purview

### Archivos de Salida (Se generan automáticamente)
- 📊 `PurviewInf_DDMMAAAA_HHMM.xlsx` - Excel con los datos procesados

---

## 🎯 ¿Qué Hace el Script?

1. **Lee** el archivo CSV `7000LineasTextoPlano.csv`
2. **Extrae** los primeros 5 campos:
   - RecordId
   - CreationDate
   - RecordType
   - Operation
   - UserId
3. **Genera** un archivo Excel con las primeras 5 filas

---

## 📊 Resultado Esperado

Tu Excel tendrá esta estructura:

| RecordId | CreationDate | RecordType | Operation | UserId |
|----------|-------------|------------|-----------|--------|
| 0161b511... | 2025-08-18T07:12:10 | 6 | FileAccessed | ext.ealanis@fesanco.cl |
| 0406d38f... | 2025-07-31T13:55:38 | 6 | FileSyncUploadedFull | ext.ealanis@fesanco.cl |
| ... | ... | ... | ... | ... |

---

## ⚙️ Configuración Rápida

### Cambiar el número de filas
Edita `formatear_purview.py`, línea 22:
```python
num_filas_procesar = 5  # Cambia a 10, 100, 1000, etc.
```

### Cambiar el archivo de entrada
Edita `formatear_purview.py`, línea 21:
```python
archivo_fuente = "7000LineasTextoPlano.csv"  # Cambia al nombre de tu archivo
```

---

## 📚 Documentación Completa

Si necesitas más información, consulta:

1. **`README.md`** - Documentación general del proyecto
2. **`CONTEXTO_MIGRACION_CSV.md`** - Historia del bug corregido
3. **`RESUMEN_CAMBIOS.md`** - Lista detallada de cambios
4. **`Analisis_Real_CSV/README.md`** - Código de producción actual

---

## 🆘 Problemas Comunes

### "Archivo no encontrado"
**Solución:** Verifica que `7000LineasTextoPlano.csv` esté en la misma carpeta que `formatear_purview.py`

### "Module not found: pandas"
**Solución:** Instala las dependencias:
```bash
pip install pandas openpyxl
```

### "Datos corruptos en el Excel"
**Solución:** 
- ✅ Asegúrate de que el archivo sea `.csv` (texto plano)
- ❌ NO uses archivos `.xlsx` como entrada
- ❌ NO abras/edites el CSV con Excel

---

## 📞 ¿Necesitas Ayuda?

1. **Revisa la documentación** (archivos .md en la raíz)
2. **Verifica los requisitos** (pandas, openpyxl)
3. **Comprueba el archivo de entrada** (debe ser CSV, no Excel)

---

## ✨ Funcionalidades Actuales

### ✅ Fase 1 (ACTUAL)
- Extracción de 5 campos básicos
- Lectura correcta de CSV
- Generación de Excel limpio
- **Estado:** ✅ Completado

### 🔜 Fase 2 (FUTURO)
- Análisis del campo `AuditData` (JSON)
- Extracción de campos del JSON
- Expansión a más columnas
- **Estado:** ⏳ Planificado

---

## 🎉 ¡Listo!

Ya puedes ejecutar el script:

```bash
python formatear_purview.py
```

---

**Última actualización:** 16/10/2025  
**Versión:** 2.0

