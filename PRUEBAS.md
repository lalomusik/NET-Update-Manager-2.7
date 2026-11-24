# Evidencia de pruebas — 3.0

Realizadas en entorno Linux de construcción cruzada:
- Compilación `GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build`: OK.
- Compilación del ejecutable de pruebas `go test -c`: OK (no ejecutadas; ejecutable Windows).
- Análisis estático `go vet ./src` con target Windows: OK.
- Validación de cabecera MZ / PE32+ de Windows, GUI x64, 9 secciones: OK.
- Incorporación de icono en recurso PE `.rsrc`: OK.

**No realizadas**: pruebas de ejecución del EXE, UI, Windows 10/11, UAC, proxy corporativo, red NVD/Microsoft/GitHub, actualizaciones, instalaciones o cancelación bajo condiciones reales. No puede afirmarse que la aplicación esté libre de AppHangB1 hasta pasar esas pruebas.
