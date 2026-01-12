# ============================================================
# StoicizmFrame — Architecture Documentation Generator v3.15
# Создание архитектурного дерева + документов + rollback + git
# ============================================================

Write-Host "=== StoicizmFrame: Creating Architecture Documentation v3.15 ===" -ForegroundColor Green

# --- Paths ---
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$docsDir = Join-Path $root "docs\architecture"
$archiveDir = Join-Path $root "_archive\architecture_docs\rollback_v3.15"
$rollbackFile = Join-Path $archiveDir "architecture_docs_structure.rollback.txt"

# --- 1. Create directories ---
Write-Host "[1/6] Creating directory structure..." -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path $docsDir | Out-Null
New-Item -ItemType Directory -Force -Path $archiveDir | Out-Null

Write-Host "[OK] Directories created."

# --- 2. Create rollback file ---
Write-Host "[2/6] Creating rollback snapshot..." -ForegroundColor Cyan

$rollbackContent = @"
StoicizmFrame Architecture Docs Rollback v3.15
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

This rollback confirms that the following directory structure
was created automatically:

- docs/
  └── architecture/
      ARCHITECTURE_STATUS_v3.15.md
      ROADMAP_v4.0.md
      BRANCH_TREE.md
      DEPLOYMENT_MAP.md
      FOUNDATION_MODELS.md

- _archive/
  └── architecture_docs/
      └── rollback_v3.15/
"@

Set-Content -Path $rollbackFile -Value $rollbackContent -Encoding UTF8
Write-Host "[OK] Rollback created: $rollbackFile"

# --- 3. Create architecture documents ---
Write-Host "[3/6] Generating architecture documents..." -ForegroundColor Cyan

# 3.1 ARCHITECTURE_STATUS
Set-Content -Path "$docsDir\ARCHITECTURE_STATUS_v3.15.md" -Encoding UTF8 -Value @"
# StoicizmFrame — Architecture Status v3.15

## Текущее состояние архитектуры

- Health Layer — интегрирован
- QC Layer — интегрирован
- PrePublish Gate — интегрирован
- ContentPipeline — обновлён
- PipelineResult — расширен
- Структура C — активна
- Rollback-механизм — активен
- Кодировка — нормализована (UTF-8 LF)
- Проект готов к первому прогону фабрики

## Архитектурный узел
v3.15-ARCHITECTURE-DOCS
"@

# 3.2 ROADMAP_v4.0
Set-Content -Path "$docsDir\ROADMAP_v4.0.md" -Encoding UTF8 -Value @"
# StoicizmFrame — Roadmap v4.0

## Этап A — Завершение ядра
- Первый прогон фабрики
- Архивация rollback'ов
- Коробочная версия v3.15

## Этап B — Расширение Frames
- StoicizmFrame
- MasterFrame
- RecipeFrame

## Этап C — Foundry Integration
- GPT5.2
- DeepSeek
- Flux
- Stable Diffusion
- Azure Speech

## Этап D — Автоматизация
- run_hygiene.ps1
- check_repo.ps1
- tests/

## Этап E — Релиз v4.0
- Полная коробочная версия
"@

# 3.3 BRANCH_TREE
Set-Content -Path "$docsDir\BRANCH_TREE.md" -Encoding UTF8 -Value @"
# StoicizmFrame — Branch Tree (Architectural)

## v3.15 — Architecture Core
- HEALTH_LAYER
- QC_LAYER
- PREPUBLISH_GATE
- PIPELINE_RESULT
- CONTENT_PIPELINE

## v3.16 — Foundation Models
- GPT5.2
- DeepSeek
- Flux
- Stable Diffusion
- Azure Speech

## v3.17 — Visual Pipelines
- Foundry Video Pipeline
- Visual Patterns

## v3.18 — Frames
- StoicizmFrame
- MasterFrame
- RecipeFrame

## v3.19 — Automation
- run_hygiene.ps1
- check_repo.ps1
- tests/

## v4.0 — Box Release
"@

# 3.4 DEPLOYMENT_MAP
Set-Content -Path "$docsDir\DEPLOYMENT_MAP.md" -Encoding UTF8 -Value @"
# StoicizmFrame — Deployment Map

## Основные компоненты
- ContentPipeline
- Health Layer
- QC Layer
- PrePublish Gate
- PipelineResult

## Foundry Models
- GPT5.2
- DeepSeek
- Flux
- Stable Diffusion

## Azure Services
- Azure Speech TTS

## Deployment Formula
DEPLOY = (Scenario + Voice + Visual + QC + Gate) → Foundry → Output
"@

# 3.5 FOUNDATION_MODELS
Set-Content -Path "$docsDir\FOUNDATION_MODELS.md" -Encoding UTF8 -Value @"
# StoicizmFrame — Foundation Models

## LLM
- GPT5.2 — основной сценарный движок
- DeepSeek — массовая генерация

## Visual
- Flux — премиум визуал
- Stable Diffusion — массовый визуал

## Audio
- Azure Speech Neural TTS

## Video
- Foundry Video Pipeline (до 7 минут)
"@

Write-Host "[OK] Architecture documents generated."

# --- 4. Git commit ---
Write-Host "[4/6] Creating Git commit..." -ForegroundColor Cyan

git add docs _archive
git commit -m "v3.15: Add architecture documentation (ARCHITECTURE_STATUS, ROADMAP, BRANCH_TREE, DEPLOYMENT_MAP, FOUNDATION_MODELS)"

Write-Host "[OK] Git commit created."

# --- 5. Git tag ---
Write-Host "[5/6] Creating Git tag..." -ForegroundColor Cyan

git tag v3.15-ARCHITECTURE-DOCS

Write-Host "[OK] Tag v3.15-ARCHITECTURE-DOCS created."

# --- 6. Done ---
Write-Host "=== Architecture Documentation v3.15 Completed ===" -ForegroundColor Green
