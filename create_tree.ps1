# Переходим в папку
Set-Location D:\StoicizmFrame_v3.14_clean

# Файлы верхнего уровня
New-Item -Path README.md -ItemType File -Force
New-Item -Path dev_log.txt -ItemType File -Force
New-Item -Path DECLARATION.md -ItemType File -Force
New-Item -Path CHARTER.md -ItemType File -Force
New-Item -Path LEGACY.md -ItemType File -Force
New-Item -Path HERITAGE.md -ItemType File -Force
New-Item -Path .gitignore -ItemType File -Force
New-Item -Path .gitattributes -ItemType File -Force
New-Item -Path .env -ItemType File -Force

# Папка src
New-Item -Path src -ItemType Directory -Force
New-Item -Path src\donor_parser.py -ItemType File -Force
New-Item -Path src\scenario_builder.py -ItemType File -Force
New-Item -Path src\voice_adapter.py -ItemType File -Force
New-Item -Path src\layout_composer.py -ItemType File -Force

# Папка tests
New-Item -Path tests -ItemType Directory -Force
New-Item -Path tests\test_scenarios.py -ItemType File -Force
New-Item -Path tests\test_voice.py -ItemType File -Force

# Папка _tools_keep_5
New-Item -Path _tools_keep_5 -ItemType Directory -Force
New-Item -Path _tools_keep_5\run_hygiene.ps1 -ItemType File -Force
New-Item -Path _tools_keep_5\normalize_yaml.ps1 -ItemType File -Force
