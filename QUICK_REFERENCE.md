# 🎯 REFERENCIA RÁPIDA - Fotos en Render

## 3 Pasos para Resolver

```
1. Push a GitHub       (git push origin main)
   ↓
2. Deploy en Render   (Auto-trigger)
   ↓
3. Abre la web        (https://curriculum-vitae-485k.onrender.com/hoja-de-vida/)
   ↓
✅ FOTO VISIBLE
```

## Verificar Azure en Render (PRIMERO)

```
Render Dashboard 
  → Tu Servicio "curriculum-vitae-485k"
  → Environment
  → Busca: AZURE_STORAGE_CONNECTION_STRING
  
Si no está → ❌ AGREGAR (obligatorio)
Si está → ✅ Continuar
```

## Git Push

```bash
cd c:\Users\HP\Downloads\prueba
git add -A
git commit -m "Fix: Azure Blob Storage para fotos"
git push origin main
```

## Esperar Deploy

```
Render → Logs
  ├─ Busca: "Build completed successfully"
  └─ Busca: "Migración completada"
```

## Verificar en la Web

```
https://curriculum-vitae-485k.onrender.com/hoja-de-vida/

¿Aparece la foto? → ✅ PROBLEMA RESUELTO
¿No aparece?      → ❌ Revisar VERIFICAR_AZURE_CONFIG.md
```

## Checklist

- [ ] AZURE_STORAGE_CONNECTION_STRING en Render
- [ ] Git push completado
- [ ] Deploy completado
- [ ] Logs muestran "Migración completada"
- [ ] Foto aparece en web
- [ ] Foto aparece en PDF descargado

## Si Falla

1. ¿AZURE_STORAGE_CONNECTION_STRING existe en Render?
   → Si no → Agregarla (OBLIGATORIO)

2. ¿Los logs muestran errores?
   → Revisar VERIFICAR_AZURE_CONFIG.md

3. ¿El container en Azure tiene acceso público?
   → Azure Portal → Storage Account → Containers
   → Click container "media" → Access Level
   → Debe ser "Blob (anonymous read access)"

## Archivos Importantes

```
FIX_FOTOS_RENDER_README.md     ← Guía completa
PASOS_PARA_RESOLVER_FOTOS.md   ← Paso a paso
VERIFICAR_AZURE_CONFIG.md      ← Troubleshooting
RESUMEN_CAMBIOS.md             ← Cambios realizados
```

## URLs

```
Render:    https://curriculum-vitae-485k.onrender.com/hoja-de-vida/
Azure:     https://dashboard.render.com
GitHub:    [Tu repositorio]
```

---

**¡Listo! 🚀**
