# 📊 Análisis Real CSV - Purview Script Analyser

Analizador profesional de archivos CSV de Microsoft Purview con extracción y flattening de JSON.

---

## 📁 Estructura del Proyecto

```
Analisis_Real_CSV/
│
├── Business/              # Lógica de negocio (código Python)
│   ├── main.py           # Script principal ⭐ EJECUTAR ESTE
│   ├── extractor.py      # Extractor de datos CSV + JSON
│   ├── excel_creator.py  # Generador de Excel
│   └── json_parser.py    # Parser y flattener de JSON
│
├── Data/                  # Datos de entrada y salida
│   ├── Input/            # CSV base de entrada
│   │   └── 7000LineasTextoPlano.csv
│   └── Output/           # Excel y archivos generados
│       ├── PurviewInf_Completo_*.xlsx
│       └── resumen_columnas_*.txt
│
├── Docs/                  # Documentación
│   ├── README.md         # Guía general
│   ├── README_FASE2.md   # Conceptos de flattening
│   └── COMO_USAR_FASE2.md # Guía de uso detallada
│
└── README.md             # Este archivo
```

---

## 🚀 Inicio Rápido

### 1. Ejecutar el Análisis

```bash
cd Analisis_Real_CSV/Business
python main.py
```

### 2. Resultado

El script generará:
- **Excel:** `Data/Output/PurviewInf_Completo_DDMMAAAA_HHMM.xlsx`
- **Resumen:** `Data/Output/resumen_columnas_DDMMAAAA_HHMM.txt`

---

## 📊 ¿Qué Hace?

### Entrada
- **Archivo:** `Data/Input/7000LineasTextoPlano.csv`
- **Formato:** CSV con 8 columnas (incluye JSON en campo 6)

### Proceso
1. ✅ Lee CSV directamente (sin corrupción)
2. ✅ Parsea JSON del campo `AuditData`
3. ✅ Aplana (flatten) JSON anidado
4. ✅ Extrae ~57 columnas

### Salida
- **Excel:** 57 columnas con todos los datos aplanados
- **Formato:** Profesional, limpio, listo para análisis

---

## 📋 Columnas Generadas (57 total)

### BLOQUE 1: Campos CSV Base (5)
- RecordId, CreationDate, RecordType, Operation, UserId

### BLOQUE 2: AppAccessContext (9)
- Campos del JSON anidado nivel 2

### BLOQUE 3: AuditData JSON (41)
- Campos del JSON nivel 1

### BLOQUE 4: Campos Finales (2)
- AssociatedAdminUnits, AssociatedAdminUnitsNames

---

## ⚙️ Configuración

### Cambiar número de filas a procesar

Edita `Business/main.py`, línea 26:

```python
num_filas_procesar = 5  # Cambiar a 100, 1000, o 7237 (todo)
```

---

## 📚 Documentación Completa

Ver `Docs/` para documentación detallada:

- **`COMO_USAR_FASE2.md`** - Guía de uso completa
- **`README_FASE2.md`** - Conceptos y explicaciones
- **`README.md`** - Guía general del código

---

## 🎯 Características

✅ **Sin corrupción de datos** - Lee CSV directamente  
✅ **JSON completo** - Parsea todo el campo AuditData  
✅ **Flattening automático** - JSON anidado → columnas planas  
✅ **Nombres duplicados** - Resueltos automáticamente  
✅ **UTF-8 preservado** - Caracteres especiales intactos  
✅ **Excel profesional** - Headers formateados, columnas ajustadas  

---

## 🆘 Troubleshooting

### Error: "Archivo no encontrado"
- Verifica que `7000LineasTextoPlano.csv` esté en `Data/Input/`

### Error: "Module not found"
```bash
pip install pandas openpyxl
```

### Excel muy grande
- Reduce `num_filas_procesar` temporalmente

---

## 📞 Más Información

Para más detalles, consulta:
- `Docs/COMO_USAR_FASE2.md` - Guía detallada
- `Docs/README_FASE2.md` - Explicación conceptual

---

**Última actualización:** 16/10/2025  
**Versión:** 2.0 (Refactorizada y Organizada)

