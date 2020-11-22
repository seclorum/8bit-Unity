echo off

setlocal enableextensions enabledelayedexpansion

mkdir c64
cd ..

del build\c64\*.* /F /Q

echo --------------- CONVERT ASSETS ---------------  

utils\py27\python utils\scripts\c64\C64Bitmap.py projects/goblin/bitmaps/banner-c64.png build/c64/banner.img
utils\py27\python utils\scripts\c64\C64Bitmap.py projects/goblin/bitmaps/scene1-c64.png build/c64/scene1.img
utils\py27\python utils\scripts\c64\C64Sprites.py projects/goblin/sprites/sprites-c64.png build/c64/sprites.dat
utils\py27\python utils\scripts\ProcessChunks.py c64 projects/goblin/chunks/chunks-c64.txt build/c64/

utils\scripts\c64\sidreloc.exe -v -z 30-ff -p 08 projects/goblin/music/goblin-c64.sid build/c64/goblin.sid
if exist build/c64/goblin.sid (
    utils\scripts\c64\psid64.exe -n build/c64/goblin.sid
) else (
    echo Relocation impossible, using the original file instead...
    copy projects\goblin\music\goblin-c64.sid build\c64\goblin.prg
)

echo DONE!

echo --------------- COMPILE PROGRAM ---------------

utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\bitmap.c
utils\cc65\bin\ca65 -t c64 unity\bitmap.s
del unity\bitmap.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\charmap.c
utils\cc65\bin\ca65 -t c64 unity\charmap.s
del unity\charmap.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\chunks.c
utils\cc65\bin\ca65 -t c64 unity\chunks.s
del unity\chunks.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\geom2d.c
utils\cc65\bin\ca65 -t c64 unity\geom2d.s
del unity\geom2d.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\mouse.c
utils\cc65\bin\ca65 -t c64 unity\mouse.s
del unity\mouse.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\music.c
utils\cc65\bin\ca65 -t c64 unity\music.s
del unity\music.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\net-base.c
utils\cc65\bin\ca65 -t c64 unity\net-base.s
del unity\net-base.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\net-url.c
utils\cc65\bin\ca65 -t c64 unity\net-url.s
del unity\net-url.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\net-tcp.c
utils\cc65\bin\ca65 -t c64 unity\net-tcp.s
del unity\net-tcp.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\net-udp.c
utils\cc65\bin\ca65 -t c64 unity\net-udp.s
del unity\net-udp.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\net-web.c
utils\cc65\bin\ca65 -t c64 unity\net-web.s
del unity\net-web.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\pixel.c
utils\cc65\bin\ca65 -t c64 unity\pixel.s
del unity\pixel.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\print.c
utils\cc65\bin\ca65 -t c64 unity\print.s
del unity\print.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\scaling.c
utils\cc65\bin\ca65 -t c64 unity\scaling.s
del unity\scaling.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\sfx.c
utils\cc65\bin\ca65 -t c64 unity\sfx.s
del unity\sfx.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\sprites.c
utils\cc65\bin\ca65 -t c64 unity\sprites.s
del unity\sprites.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\widgets.c
utils\cc65\bin\ca65 -t c64 unity\widgets.s
del unity\widgets.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\C64\directory.c
utils\cc65\bin\ca65 -t c64 unity\C64\directory.s
del unity\C64\directory.s
utils\cc65\bin\cc65 -Cl -O -t c64 -I unity unity\C64\VIC2.c
utils\cc65\bin\ca65 -t c64 unity\C64\VIC2.s
del unity\C64\VIC2.s
utils\cc65\bin\ca65 -t c64 unity\atan2.s
utils\cc65\bin\ca65 -t c64 unity\chars.s
utils\cc65\bin\ca65 -t c64 unity\tiles.s
utils\cc65\bin\ca65 -t c64 unity\C64\joystick.s
utils\cc65\bin\ca65 -t c64 unity\C64\scroll.s
utils\cc65\bin\ca65 -t c64 unity\C64\ROM.s
utils\cc65\bin\ca65 -t c64 unity\C64\SID.s
utils\cc65\bin\ar65 r build/c64/unity.lib unity\bitmap.o unity\charmap.o unity\chunks.o unity\geom2d.o unity\mouse.o unity\music.o unity\net-base.o unity\net-url.o unity\net-tcp.o unity\net-udp.o unity\net-web.o unity\pixel.o unity\print.o unity\scaling.o unity\sfx.o unity\sprites.o unity\widgets.o unity\C64\directory.o unity\C64\VIC2.o unity\atan2.o unity\chars.o unity\tiles.o unity\C64\joystick.o unity\C64\scroll.o unity\C64\ROM.o unity\C64\SID.o 
utils\cc65\bin\cl65 -o build/c64/goblin.bin -m build/goblin-c64.map -Cl -O -t c64 -C unity/C64/c64.cfg -I unity projects/goblin/src/goblin.c projects/goblin/src/chunks.c projects/goblin/src/interface.c projects/goblin/src/scene.c build/c64/unity.lib unity/IP65/ip65_tcp.lib unity/IP65/ip65_c64.lib

utils\scripts\exomizer-3.0.2.exe sfx $180d build/c64/goblin.bin build/c64/sprites.dat -o build/c64/loader.prg

echo DONE!

echo --------------- C64 DISK BUILDER --------------- 

set C1541=utils\scripts\c64\c1541 -format loader,666 d64 build/goblin-c64.d64 -attach build/goblin-c64.d64 -write build/c64/loader.prg loader.prg -write build/c64/banner.img banner.img -write build/c64/scene1.img scene1.img -write build/c64/goblin.prg goblin.mus 
for /f "tokens=*" %%A in (build\c64\chunks.lst) do set C1541=!C1541!-write %%A %%~nxA 
%C1541%


echo DONE
pause

cd "utils\emulators\WinVICE-2.4"
x64.exe "..\..\..\build\goblin-c64.d64"