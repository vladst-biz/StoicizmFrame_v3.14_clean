<#
.SYNOPSIS
    Скрипт для проверки и очистки кодировки файлов в проекте StoicizmFrame.
.DESCRIPTION
    Проверяет наличие BOM, нормализует кодировку в UTF-8 LF без BOM,
    фиксирует результаты как архитектурные артефакты.
#>

param(
    [string]$RootPath = "D:\StoicizmFrame_v3.14_clean"
)

# Настройка консоли
chcp 65001 | Out-Null
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

Write-Output "=== StoicizmFrame Hygiene Script Started ==="
Write-Output "Root path: $RootPath"

# -------------------------------
# Функция проверки BOM
# -------------------------------
function Test-BOM {
    param([string]$FilePath)

    $bytes = [System.IO.File]::ReadAllBytes($FilePath)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        return $true
    }
    return $false
}

# -------------------------------
# Функция удаления BOM
# -------------------------------
function Remove-BOM {
    param([string]$FilePath)

    $content = Get-Content $FilePath -Raw
    [System.IO.File]::WriteAllText($FilePath, $content, $utf8NoBom)
    Write-Output "BOM removed: $FilePath"
}

# -------------------------------
# Основная логика
# -------------------------------
$files = Get-ChildItem -Path $RootPath -Recurse -Include *.md, *.ps1, *.py, *.txt

foreach ($file in $files) {
    if (Test-BOM $file.FullName) {
        Write-Output "BOM detected: $($file.FullName)"
        Remove-BOM $file.FullName
    }
    else {
        Write-Output "Clean: $($file.FullName)"
    }
}

Write-Output "=== StoicizmFrame Hygiene Script Completed ==="
