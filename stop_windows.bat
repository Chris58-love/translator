@echo off
cd /d "%~dp0"

echo ========================================
echo Realtime Interpreter - Stop Local Services
echo ========================================
echo.

echo Stopping backend port 8000...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$processIds = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; if ($processIds) { foreach ($processId in $processIds) { Write-Host '[Stopping] Port 8000 process' $processId; Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue; if ($?) { Write-Host '[DONE] Process stopped:' $processId } else { Write-Host '[WARNING] Could not stop process:' $processId } } } else { Write-Host '[INFO] No listening service found on port 8000.' }"

echo.
echo Stopping frontend port 5500...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$processIds = Get-NetTCPConnection -LocalPort 5500 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; if ($processIds) { foreach ($processId in $processIds) { Write-Host '[Stopping] Port 5500 process' $processId; Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue; if ($?) { Write-Host '[DONE] Process stopped:' $processId } else { Write-Host '[WARNING] Could not stop process:' $processId } } } else { Write-Host '[INFO] No listening service found on port 5500.' }"

echo.
echo [DONE] Stop command finished.
echo If windows are still open, close the related command windows manually.
echo.
pause
exit /b 0