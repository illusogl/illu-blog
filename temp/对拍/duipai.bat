@echo off
rem ===== stress-test script for Windows CMD (no bash needed) =====
rem edit sol.cpp (your solution) / bf.cpp (brute force) / gen.cpp (generator) first
rem usage: run "duipai.bat" in a terminal, or double-click this file
cd /d %~dp0

set GXX=C:\mingw64\bin\g++.exe
if not exist "%GXX%" set GXX=g++

%GXX% -O2 sol.cpp -o sol.exe || (echo COMPILE FAILED: sol.cpp & pause & exit /b 1)
%GXX% -O2 bf.cpp -o bf.exe || (echo COMPILE FAILED: bf.cpp & pause & exit /b 1)
%GXX% -O2 gen.cpp -o gen.exe || (echo COMPILE FAILED: gen.cpp & pause & exit /b 1)

set /a i=1
:loop
.\gen.exe %i% > in.txt
.\sol.exe < in.txt > out1.txt
.\bf.exe < in.txt > out2.txt
fc out1.txt out2.txt > nul
if errorlevel 1 (
    echo WA! seed=%i%  reproduce: .\gen.exe %i% ^> in.txt
    echo ---- input ----
    type in.txt
    echo ---------------
    pause
    exit /b 0
)
set /a i+=1
goto loop
