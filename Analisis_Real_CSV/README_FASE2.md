# 📊 Fase 2: Análisis Completo con JSON Flattening

## 🎯 Concepto: Aplanamiento (Flattening)

Convertir la estructura JSON anidada del campo `AuditData` en columnas individuales del Excel.

---

## 📋 Estructura del Excel Final

### Columnas del Excel (en orden):

#### 📌 BLOQUE 1: Campos directos del CSV (5 columnas)
1. RecordId
2. CreationDate
3. RecordType
4. Operation
5. UserId

#### 📌 BLOQUE 2: Campos del JSON anidado `AppAccessContext` (nivel 2) (~7 columnas)
6. AADSessionId
7. AuthTime
8. ClientAppId
9. ClientAppName
10. CorrelationId
11. TokenIssuedAtTime
12. UniqueTokenId

#### 📌 BLOQUE 3: Campos del JSON `AuditData` (nivel 1) (~30+ columnas)
13. CreationTime
14. Id
15. Operation
16. OrganizationId
17. RecordType
18. UserKey
19. Workload
20. ClientIP
21. UserId
22. ApplicationId
23. AuthenticationType
24. BrowserName
25. BrowserVersion
26. EventSource
27. GeoLocation
28. IsManagedDevice
29. ItemType
30. ListId
31. Platform
32. Site
33. UserAgent
34. WebId
35. DeviceDisplayName
36. SourceRelativeUrl
37. SourceFileName
38. SourceFileExtension
39. ApplicationDisplayName
40. SiteUrl
41. ObjectId
... (y cualquier otro campo que aparezca)

#### 📌 BLOQUE 4: Campos finales del CSV (2 columnas)
42. AssociatedAdminUnits
43. AssociatedAdminUnitsNames

**Total estimado:** ~43+ columnas

---

## 🔄 Proceso de Flattening

### Entrada (Fila del CSV):
```
RecordId: 0161b511..., 
CreationDate: 2025-08-18..., 
AuditData: {
  "AppAccessContext": {
    "AADSessionId": "006cd379...",
    "ClientAppName": "Microsoft Office"
  },
  "CreationTime": "2025-08-18T07:12:10",
  "Operation": "FileAccessed"
},
AssociatedAdminUnits: ""
```

### Salida (Fila del Excel con ~43 columnas):
```
| RecordId | CreationDate | AADSessionId | ClientAppName    | CreationTime     | Operation    | AssociatedAdminUnits |
|----------|--------------|--------------|------------------|------------------|--------------|---------------------|
| 0161b511 | 2025-08-18   | 006cd379...  | Microsoft Office | 2025-08-18T07:12 | FileAccessed | (vacío)             |
```

---

## 📊 Ejemplo Visual del Proceso

```
CSV Original (8 columnas)
┌──────────┬──────────┬────┬────┬────┬──────────────┬────┬────┐
│ RecordId │ Creation │ RT │ Op │ UID│  AuditData   │ AA │ AN │
│          │   Date   │    │    │    │   {JSON}     │    │    │
└──────────┴──────────┴────┴────┴────┴──────────────┴────┴────┘
                                         ↓
                              ┌──────────────────┐
                              │ JSON Parsing     │
                              │ & Flattening     │
                              └──────────────────┘
                                         ↓
Excel Final (~43 columnas)
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│ R  │ CD │ RT │ Op │ UID│AAD │Auth│Client│Crea│ Id │Org │...│ AA │ AN │
│ Id │    │    │    │    │Sess│Time│AppNa │Time│    │Id  │   │    │    │
└────┴────┴────┴────┴────┴────┴────┴──────┴────┴────┴────┴────┴────┴────┘
```

---

## ⚙️ Manejo de Casos Especiales

### 1. Campos Duplicados
Algunos campos aparecen tanto en el CSV como en el JSON:
- `Operation` → En CSV (col 4) Y en JSON
- `UserId` → En CSV (col 5) Y en JSON
- `RecordType` → En CSV (col 3) Y en JSON

**Solución:** Renombrar para evitar conflictos
- CSV: `Operation` → Mantener como `Operation`
- JSON: `Operation` → Renombrar a `AuditOperation`

### 2. Campos Faltantes
Si un registro no tiene cierto campo en el JSON:
- **Valor por defecto:** `N/A`

### 3. JSON Anidado (Nivel 2)
El objeto `AppAccessContext` se "aplana" con prefijo o sin prefijo:
- **Con prefijo:** `AppAccessContext_AADSessionId`
- **Sin prefijo:** `AADSessionId` (más simple)

---

## 🎯 Resultado Final

Un archivo Excel donde:
- ✅ Cada fila = 1 registro del CSV
- ✅ Cada columna = 1 campo (ya sea del CSV o del JSON)
- ✅ JSON completamente "aplanado" en horizontal
- ✅ Sin datos anidados
- ✅ Fácil de analizar con filtros y tablas dinámicas

---

## 🚀 Ventajas del Flattening

1. **Fácil análisis:** Todos los datos en una tabla plana
2. **Filtros simples:** Puedes filtrar por cualquier campo
3. **Tablas dinámicas:** Compatible con herramientas de BI
4. **Sin corrupción:** Lectura directa desde CSV (no Excel)
5. **UTF-8 preservado:** Todos los caracteres especiales intactos

---

**Fase actual:** Planificación  
**Siguiente paso:** Implementación del parser JSON con flattening

