# 📁 Análisis Antiguo - Excel (ARCHIVADO)

## ⚠️ IMPORTANTE: NO USAR ESTE CÓDIGO

Este directorio contiene el código **ANTIGUO** que tenía el bug de leer archivos Excel en lugar de CSV.

## 🔴 Problema con este código:

1. **Leía archivos .xlsx** en lugar de CSV de texto plano
2. **Causaba corrupción** de datos JSON en el campo `AuditData`
3. **Requería funciones de limpieza** complejas (`limpiar_json()`) para intentar reparar datos corruptos
4. **Generaba Excel con 44 columnas** incluyendo 39 campos del JSON AuditData

## 📄 Archivos en este directorio:

### `data_extractor_antiguo.py`
- Función: `getdata_from_base_excel()` - ❌ Usaba `pd.read_excel()`
- Función: `limpiar_json()` - Intentaba reparar caracteres corruptos
- Función: `extraer_datos_audit()` - Extraía 39 campos del JSON
- **Problema:** Los datos ya llegaban corruptos por usar Excel

### `excel_creator_antiguo.py`
- Función: `crear_excel_purview()` - Creaba Excel con 44 columnas
- **Columnas:** 5 base + 39 del JSON AuditData
- **Problema:** Datos corruptos en las columnas del JSON

### `formatear_purview_antiguo.py`
- Script principal antiguo
- **Archivo fuente:** `7000lineasDelimitadoComas.xlsx` ❌
- **Problema:** Leía Excel en lugar de CSV

### `informe_interface_antiguo.py`
- Clase `InformeInterface` con 39 campos de auditoría
- **Complejidad innecesaria** para la fase inicial

## 🔄 Migración

Este código fue **reemplazado** por el código en `Analisis_Real_CSV/` que:
- ✅ Lee CSV directamente
- ✅ No corrompe datos
- ✅ Es más simple (5 campos en fase 1)
- ✅ Evita funciones de "limpieza" innecesarias

## 📚 Propósito de este archivo

Mantenido como **referencia histórica** y para:
- Entender el bug original
- Aprender de los errores
- Referencia para migrar funcionalidad del JSON en fase 2

**NO ejecutar este código en producción.**

---
*Archivado: 16/10/2025*

