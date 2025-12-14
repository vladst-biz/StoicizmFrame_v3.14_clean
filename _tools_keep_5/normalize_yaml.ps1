param()

$root = "D:\Projects_GPT_Azure"
$folders = Get-Content "$root\PROJECT_WORKING_FOLDERS.txt" | ForEach-Object { Join-Path $root $_ }
$normalized = @()

foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Get-ChildItem $folder -Recurse -Include *.yaml, *.yml -ErrorAction SilentlyContinue | ForEach-Object {
            $content = Get-Content $_.FullName -Raw

            # Убираем лишние пробелы в конце строк
            $content = ($content -split "`r?`n" | ForEach-Object { $_.TrimEnd() }) -join "`n"

            # Приводим окончания строк к LF
            $content = $content -replace "`r`n", "`n"

            # Пересохраняем в UTF-8 без BOM
            $utf8 = New-Object System.Text.UTF8Encoding($false)
            [System.IO.File]::WriteAllText($_.FullName, $content, $utf8)

            $normalized += $_.FullName
        }
    }
}

if ($normalized.Count -gt 0) {
    Write-Host "🔄 Нормализованы YAML-файлы:" -ForegroundColor Yellow
    $normalized | ForEach-Object { Write-Host $_ -ForegroundColor Green }
    exit 1
}
else {
    Write-Host "✅ YAML-файлы не найдены или уже нормализованы" -ForegroundColor Green
    exit 0
}
