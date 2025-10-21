@echo off
REM ============================================
REM Script para compilar dijkstra.dll en Windows
REM Requiere: MinGW-w64 instalado
REM ============================================

echo ============================================
echo Compilando dijkstra.dll con MinGW
echo ============================================

REM Compilar con g++ de MinGW
g++ -shared -o dijkstra.dll cpp/dijkstra.cpp -O2 -std=c++11 -static-libgcc -static-libstdc++

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo ✅ Compilacion exitosa!
    echo ============================================
    echo Archivo generado: dijkstra.dll
    echo.
    dir dijkstra.dll
) else (
    echo.
    echo ============================================
    echo ❌ Error en la compilacion
    echo ============================================
    echo.
    echo Verifica que MinGW este instalado:
    echo https://www.mingw-w64.org/downloads/
    echo.
    echo Agrega MinGW al PATH:
    echo Ejemplo: C:\mingw64\bin
)

pause