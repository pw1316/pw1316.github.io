@echo off
echo Enter Minimum Number:
set /p min=
echo Enter Maximum Number:
set /p max=
choice /c:1234567 /m 1:PS4,2:PS3,4:PSV
if errorlevel 7 (
    for /l %%i in (%min%, 1, %max%) do python TrophyGenFromP9.py %%i PS4 PS3 PSV
)else if errorlevel 6 (
    for /l %%i in (%min%, 1, %max%) do python TrophyGenFromP9.py %%i PS3 PSV
)else if errorlevel 5 (
    for /l %%i in (%min%, 1, %max%) do python TrophyGenFromP9.py %%i PS4 PSV
)else if errorlevel 4 (
    for /l %%i in (%min%, 1, %max%) do python TrophyGenFromP9.py %%i PSV
)else if errorlevel 3 (
    for /l %%i in (%min%, 1, %max%) do python TrophyGenFromP9.py %%i PS4 PS3
)else if errorlevel 2 (
    for /l %%i in (%min%, 1, %max%) do python TrophyGenFromP9.py %%i PS3
)else if errorlevel 1 for /l %%i in (%min%, 1, %max%) do python TrophyGenFromP9.py %%i PS4
pause