# NET Update Manager — Individual 3.0 (versión preliminar)

Aplicación **local** para Windows 10/11 x64, con una interfaz gráfica azul basada en Win32 y desarrollada en Go. No controla equipos remotos ni utiliza Active Directory.

## Empezar

1. Descomprime el ZIP completo.
2. Abre `NETUpdateManager.exe` con doble clic.
3. Pulsa **Verificar ahora** para detectar los runtimes instalados.
4. Pulsa **Consultar Microsoft** en Actualizaciones para comparar las versiones del mismo componente y arquitectura.
5. Selecciona una fila, revisa el estado, descarga y verifica el instalador oficial. La instalación requiere confirmación.

## Funciones 3.0

| Sección | Qué hace realmente |
|---|---|
| Actualizaciones inteligentes | Compara la versión más alta instalada con la última publicada para la misma familia principal, tipo y arquitectura. No migra aplicaciones automáticamente. |
| Seguridad / CVE | Consulta coincidencias de palabras clave en el servicio público NVD. Son **candidatos no confirmados**, no vulnerabilidades demostradas del equipo. El estado de fin de soporte también se muestra por separado. |
| Dependencias | Examina archivos `*.runtimeconfig.json` de Program Files y Program Files (x86) con límites de tiempo, profundidad y tamaño. No garantiza encontrar todas las aplicaciones. |
| Limpieza segura | Identifica parches anteriores dentro de una misma familia/arquitectura y muestra una **lista de revisión**. NO desinstala ni borra nada. |
| Diagnóstico y reparación | Comprueba las rutas dotnet y ejecuta `DISM /Online /Cleanup-Image /CheckHealth` (solo consulta). Ofrece enlace a la guía oficial de reparación. NO realiza una reparación automática. |
| Actualización desde GitHub | Comprueba la última Release estable publicada en el repositorio indicado y permite abrir la página Releases. No ejecuta binarios de GitHub automáticamente. |
| Descarga e instalación .NET | Usa metadatos oficiales de Microsoft, verifica SHA-512 y firma Authenticode. Solo lanza el instalador después de confirmación. |

## Seguridad y limitaciones

- Es una versión **pre-release**. La compilación cruzada y `go vet` se completaron, pero la interfaz y todas las rutas de red aún requieren pruebas en un equipo Windows real.
- El ejecutable no está firmado digitalmente. Windows SmartScreen puede advertir sobre programas desconocidos.
- Ninguna opción elimina los runtimes obsoletos automáticamente.
- No se ejecutan reparaciones, instalaciones ni limpieza sin aprobación explícita.
- NVD devuelve CVE candidatos por palabra clave; no hay correlación de versiones CPE verificada. **No afirmes que una coincidencia es un CVE aplicable**.
- Las aplicaciones empaquetadas/self-contained y los runtimes de rutas no estándar pueden no aparecer en el análisis.
- Las consultas pueden fallar por proxy, TLS, limitación de servicios o Internet ausente. Deben mostrar errores sin afectar el diagnóstico local.
- El uso de `DISM` puede requerir permisos elevados para algunas consultas; la app mostrará el resultado.

## Datos y privacidad

Los reportes y el registro local se guardan en `C:\ProgramData\NETUpdateManager`. El inventario puede incluir nombres de equipo y rutas de aplicaciones. No publiques esos archivos sin revisarlos. La app solo consulta NVD, Microsoft y la API pública de GitHub cuando lo solicitas.

## Compilación

En Windows con Go 1.23 o más reciente:

```powershell
go test ./src
go vet ./src
go build -trimpath -ldflags="-H windowsgui -s -w" -o NETUpdateManager.exe ./src
python -m pip install Pillow
python embed_icon.py
```

`embed_icon.py` agrega el recurso ICO al PE resultante. Es una herramienta de empaquetado, no debe ejecutarse sobre un EXE ya modificado.

## Pruebas recomendadas

1. Abrir/cerrar y cambiar de sección repetidamente.
2. Analizar con x86 y x64 disponibles, y cuando no exista una instalación de .NET.
3. Consultar el catálogo con Internet, sin Internet y con proxy restrictivo.
4. Iniciar y cancelar consulta de CVE y de dependencias; la ventana debe responder.
5. Verificar que la lista de limpieza **no** elimine archivos.
6. Comprobar que descargar no sea equivalente a instalar, y que la instalación requiera confirmación.
7. Revisar `activity.log` si se produce un bloqueo AppHangB1.

Este proyecto es una herramienta de ayuda para administradores, no reemplaza Microsoft Update ni un escáner de vulnerabilidades certificado.
