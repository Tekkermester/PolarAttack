@echo off
REM -----------------------------------------------------------------------
REM PolarAttack Windows build helper (build_windows.bat)
REM Creates a PyInstaller build for the PolarAttack GUI app.
REM This script bundles:
REM   - the app Python sources
REM   - the `ui` folder (UI files and icons)
REM   - chromedriver.exe at the bundle root
REM   - the `chromium_win` folder (if present) so the packaged app can run Chromium directly
REM Output: dist\PolarAttack\PolarAttack.exe (with supporting files in dist\PolarAttack)
REM -----------------------------------------------------------------------

SETLOCAL ENABLEDELAYEDEXPANSION

REM Resolve script directory (project root)
SET "SCRIPT_DIR=%~dp0"
REM Remove trailing backslash if present
IF "%SCRIPT_DIR:~-1%"=="\" SET "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo ================================
echo PolarAttack Windows build script
echo Project root: "%SCRIPT_DIR%"
echo ================================

REM Helper to check for file or folder
IF NOT EXIST "%SCRIPT_DIR%\main.py" (
    echo ERROR: Could not find "main.py" in project root. Aborting.
    exit /b 1
)

REM Check for optional resources and warn if missing
IF NOT EXIST "%SCRIPT_DIR%\chromedriver.exe" (
    echo WARNING: "chromedriver.exe" not found in project root.
    echo The application expects "chromedriver.exe" to be bundled at the exe root (paths.chromium_path()).
) ELSE (
    echo Found chromedriver.exe - will be bundled.
)

IF NOT EXIST "%SCRIPT_DIR%\chromium_win\chrome.exe" (
    echo WARNING: "chromium_win\chrome.exe" not found.
    echo If you want a bundled Chromium build, place your Chromium binary under "chromium_win\chrome.exe".
) ELSE (
    echo Found chromium_win\chrome.exe - will be bundled.
)

IF NOT EXIST "%SCRIPT_DIR%\ui" (
    echo WARNING: "ui" folder missing. The user interface assets may not be available in the build.
) ELSE (
    echo Found ui/ resources - will be bundled.
)

echo.
echo Ensure you have a Python environment (recommended: virtualenv) with the project's dependencies installed.
echo This script will attempt to install dependencies into the active Python environment if needed.
echo.

REM Install dependencies (you can skip if you already have them)
echo Installing/ensuring build dependencies (requirements.txt + pyinstaller)...
python -m pip install --upgrade pip
python -m pip install -r "%SCRIPT_DIR%\requirements.txt" pyinstaller

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies. Resolve pip/requirements issues and re-run.
    exit /b 2
)

REM Change to project root for PyInstaller relative paths
PUSHD "%SCRIPT_DIR%"

REM Compose --add-data arguments for PyInstaller
REM On Windows, --add-data expects "SRC;DEST" pairs.
SET "ADD_DATA="
REM Include UI folder if present
IF EXIST "ui" (
    SET "ADD_DATA=%ADD_DATA% --add-data \"ui;ui\""
)
REM Include chromedriver.exe into the bundle root
IF EXIST "chromedriver.exe" (
    SET "ADD_DATA=%ADD_DATA% --add-data \"chromedriver.exe;.\""
)
REM Include chromium_win directory (so resource_path('chromium_win\chrome.exe') can find it)
IF EXIST "chromium_win\chrome.exe" (
    SET "ADD_DATA=%ADD_DATA% --add-data \"chromium_win;chromium_win\""
)

REM Additional helpful data files (icons etc) are inside ui/ already; include any other files you need here

echo Running PyInstaller...
REM Use --windowed so the app runs as a GUI app (no console) and --onedir so large external binaries (Chromium) can be kept as files
REM Name the app "PolarAttack" as requested
pyinstaller --noconfirm --clean --windowed --onedir --name "PolarAttack" %ADD_DATA% main.py

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: PyInstaller failed. Inspect the output above for details.
    POPD
    exit /b 3
)

echo.
echo Build completed. Output folder:
echo   "%SCRIPT_DIR%\dist\PolarAttack"
echo
echo Important notes:
echo  - The application expects to find Chromium and chromedriver through paths.resource_path() as implemented in paths.py:
echo      Windows: resource_path(\"chromium_win\\chrome.exe\"), resource_path(\"chromedriver.exe\")
echo    Make sure the versions of Chromium and chromedriver are compatible.
echo  - This script uses --onedir. Creating a single-file --onefile bundle with a large Chromium binary is not recommended.
echo  - If you need a portable single .exe despite the size, change --onedir to --onefile in the pyinstaller command above (not recommended).
echo  - Test the built exe on a clean Windows environment similar to your users' systems.
echo  - If Selenium raises WebDriver / driver location errors at runtime, confirm chromedriver.exe is present next to the exe (dist\PolarAttack\chromedriver.exe).
echo
echo If you want to automatically create an installer (MSI/EXE) consider additional tools like Inno Setup or WiX.
echo
POPD

echo Done.
pause