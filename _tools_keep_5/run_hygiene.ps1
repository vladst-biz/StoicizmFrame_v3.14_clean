param()

$root = "D:\Projects_GPT_Azure"
$checkScript = "$root\_tools_keep_5\check_bom.ps1"
$fixScript = "$root\_tools_keep_5\fix_bom.ps1"
$normalizeScript = "$root\_tools_keep_5\normalize_yaml.ps1"
$logFile = "$root\dev_log.txt"

function Write-Log {
    param([string]$message)
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $entry = "$timestamp | MILESTONE: PROJECT_FILES_SCOPE_V315 | $message"
    Add-Content -Path $logFile -Value $entry -Encoding UTF8NoBOM
}

Write-Host "🔍 Запуск проверки BOM по всем рабочим узлам..." -ForegroundColor Cyan
Write-Log "RUN_HYGIENE: запуск проверки BOM"

if (Test-Path $checkScript) {
    & $checkScript
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Обнаружены файлы с BOM. Запускаем очистку..." -ForegroundColor Yellow
        Write-Log "RUN_HYGIENE: обнаружены файлы с BOM"

        if (Test-Path $fixScript) {
            & $fixScript
            Write-Host "🔄 Очистка завершена. Повторная проверка..." -ForegroundColor Cyan
            Write-Log "RUN_HYGIENE: очистка завершена"

            & $checkScript
            if ($LASTEXITCODE -eq 0) {
                Write-Log "RUN_HYGIENE: повторная проверка — все узлы чистые"
                Write-Host "✅ Все рабочие узлы проекта теперь без BOM" -ForegroundColor Green

                else {
                    Write-Log "RUN_HYGIENE: повторная проверка — BOM остался"
                    Write-Host "❌ BOM остался в некоторых файлах" -ForegroundColor Red
                }
            }
            else {
                Write-Host "❌ fix_bom.ps1 отсутствует в _tools_keep_5" -ForegroundColor Red
                Write-Log "RUN_HYGIENE: ошибка — отсутствует fix_bom.ps1"
            }
        }
        else {
            Write-Host "✅ Все рабочие узлы проекта без BOM" -ForegroundColor Green
            Write-Log "RUN_HYGIENE: все узлы чистые"
        }
    }
    else {
        Write-Host "❌ check_bom.ps1 отсутствует в _tools_keep_5" -ForegroundColor Red
        Write-Log "RUN_HYGIENE: ошибка — отсутствует check_bom.ps1"
    }

    # 📐 Запуск третьего стража — нормализация YAML
    if (Test-Path $normalizeScript) {
        Write-Host "📐 Запуск нормализации YAML..." -ForegroundColor Cyan
        Write-Log "RUN_HYGIENE: запуск normalize_yaml.ps1"

        & $normalizeScript
        if ($LASTEXITCODE -eq 0) {
            Write-Log "RUN_HYGIENE: YAML уже нормализованы"
            Write-Host "✅ YAML-файлы уже нормализованы" -ForegroundColor Green
        }
        else {
            Write-Log "RUN_HYGIENE: YAML нормализованы"
            Write-Host "🔄 YAML-файлы нормализованы" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "❌ normalize_yaml.ps1 отсутствует в _tools_keep_5" -ForegroundColor Red
        Write-Log "RUN_HYGIENE: ошибка — отсутствует normalize_yaml.ps1"
    }
