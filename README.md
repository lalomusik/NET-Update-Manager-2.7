# NET Update Manager — Individual (v2.7)

Administrador **local** de componentes .NET para Windows 10 y Windows 11 x64.

> **Estado: versión preliminar / pruebas.** Se ha compilado, pero no cuenta con certificación de seguridad ni pruebas completas en Windows real. No usar para instalaciones críticas sin validación previa. El ejecutable no está firmado digitalmente.

## Funciones

- Inventario local de .NET Framework 4.x y runtimes .NET (x64 y x86).
- Comparación de versiones **instaladas** y **disponibles** para la misma familia, componente y arquitectura.
- Consulta del índice de versiones de Microsoft.
- Descarga de instaladores oficiales con verificación de SHA-512 y firma digital.
- Instalación únicamente tras aprobación del usuario; no desinstala runtimes antiguos automáticamente.
- Exportación de resultados y registros locales.

## Cómo usar

1. Descarga el archivo ZIP desde **Releases** (no desde el botón Code).
2. Descomprímelo en una carpeta local.
3. Ejecuta `NETUpdateManager.exe`.
4. Pulsa **Verificar ahora**; después **Consultar Microsoft**.
5. Revisa cuidadosamente las versiones antes de descargar o instalar.

**Nota sobre «Seleccionar»:** en esta versión selecciona/resalta la fila para las acciones inferiores; no abre una ventana modal. La mejora de interacción está pendiente.

## Código fuente y compilación

Requiere Go 1.23 o posterior (solo biblioteca estándar). En Windows PowerShell, desde la raíz:

```powershell
$env:GOOS = 'windows'
$env:GOARCH = 'amd64'
go build -ldflags='-H windowsgui -s -w' -o NETUpdateManager.exe ./src
```

También hay un workflow en **Actions → Build Windows x64 → Run workflow** para compilar. El workflow produce un artifact; **no** publica una Release automáticamente.

## Seguridad y privacidad

- Diseñado para analizar **una PC local**; no utiliza Active Directory ni ejecuta despliegues remotos.
- La información diagnóstica se guarda localmente en `C:\ProgramData\NETUpdateManager`.
- **No subas** los reportes generados, volcados `.dmp`, nombres internos de equipos ni archivos con datos sensibles al repositorio.
- Verifica que un instalador corresponda al componente y arquitectura adecuados antes de aprobar cambios.
- La categorización del estado de soporte no constituye un análisis integral de vulnerabilidades.

## Estado legal

Este repositorio **no incluye una licencia de software**. Todos los derechos permanecen reservados al titular del código hasta que decida publicar una licencia (por ejemplo, MIT). No se agrega una licencia sin autorización.

Consulta [docs/PUBLICACION.md](docs/PUBLICACION.md) para las instrucciones de subida.
