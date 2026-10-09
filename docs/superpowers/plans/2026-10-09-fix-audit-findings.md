# Tesseract Audit Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Устранить все критические и архитектурные дефекты, выявленные в ходе общего технического аудита репозитория и аудита совместимости с Google Antigravity.

**Architecture:** 
1. Нормализация конфигурации проекта: добавление корневого `.gitignore`, удаление мертвого файла `gemini-extension.json`, очистка манифеста `plugin.json`.
2. Синхронизация версий: приведение веб-плеера и GitHub Actions к актуальной версии 0.3.1.
3. Кроссплатформенная стабильность: устранение ошибки Fontconfig в FFmpeg на Windows/Linux и замена жестких ссылок `os.link` на атомарный перенос `os.replace`.
4. Оптимизация правил Antigravity: устранение дублирования правил и синхронизация `GEMINI.md` и `rules/AGENTS.md`.
5. Автоматизированное тестирование: добавление тестов целостности версий и работоспособности медиа-хелперов.

**Tech Stack:** Python 3.11+, FFmpeg/ffprobe, JavaScript / WebGPU, GitHub Actions, Antigravity Plugin Framework.

**Spec:** Результаты технического аудита репозитория и аудита совместимости с Google Antigravity.

## Global Constraints

- Версия движка Tesseract и плагина строго зафиксирована на `0.3.1`.
- Формат манифеста `plugin.json` должен строго соответствовать спецификации Antigravity Plugin.
- Изменения в скриптах `skills/tesseract-video/scripts/` должны быть полностью идентичны `skills/tesseract-motion/scripts/`.
- Запрещено использовать `shell=True` в любых вызовах `subprocess`.
- Правила `GEMINI.md` и `rules/AGENTS.md` не должны превышать лимит в 24,000 байт.

## Review Focus

1. Проверка пути импорта рантайма в `player/app.js` и сборки в `.github/workflows/player-pages.yml` на совпадение с версией 0.3.1.
2. Проверка генерации спектрограмм в `tesseract_waveform.py` на Windows без спама ошибок Fontconfig.
3. Проверка надежности атомарного сохранения файлов на не-NTFS или защищенных файловых системах (отказ от `os.link` в пользу `os.replace`).
4. Корректность распознавания плагина в Antigravity (`plugin.json` с валидным путем к логотипу без ведущего `./`).
5. Прохождение всех проверок в новом тест-сьюте `tests/test_audit_remediation.py`.

---

### Task 1: Конфигурационная гигиена и корневой `.gitignore`

**Files:**
- Create: `.gitignore`
- Remove: `gemini-extension.json`
- Remove: `.agents/rules/tesseract.md`

**Interfaces:**
- Consumes: N/A
- Produces: Чистое состояние Git-репозитория без нежелательных артефактов и неподдерживаемых файлов.

- [x] **Step 1: Создать корневой `.gitignore`**
  Создать `.gitignore` в корне `f:\Exp\Mirage\.gitignore`:
  ```gitignore
  # System & OS
  .DS_Store
  Thumbs.db
  desktop.ini

  # Python caches & virtual environments
  __pycache__/
  *.py[cod]
  *$py.class
  .venv/
  env/
  venv/

  # Editor & IDE directories
  .vscode/
  .idea/
  *.swp
  *.swo

  # Tesseract runtime & temporary working files
  .tesseract-work/
  *.tsrct.tmp
  player/runtime/

  # Local workspace agent customizations (to prevent dirty status if cloned as plugin)
  .agents/
  ```

- [x] **Step 2: Удалить неподдерживаемый файл `gemini-extension.json`**
  Удалить `gemini-extension.json`, так как Antigravity использует только `plugin.json`.

- [x] **Step 3: Удалить избыточный дубликат `.agents/rules/tesseract.md`**
  Удалить `.agents/rules/tesseract.md`, устранив двойной расход квоты контекста правил.

- [x] **Step 4: Проверить статус Git**
  Запустить `git status` и убедиться, что мусорные файлы игнорируются, а устаревшие удалены.

---

### Task 2: Синхронизация версий рантайма (Web Player & CI/CD)

**Files:**
- Modify: `player/app.js:1-10`
- Modify: `.github/workflows/player-pages.yml:23-28`

**Interfaces:**
- Consumes: `release-manifest.json` (версия 0.3.1)
- Produces: Синхронизированный плеер и пайплайн GitHub Pages, использующие рантайм `0.3.1`.

- [x] **Step 1: Обновить импорт рантайма в `player/app.js`**
  В строке 3 заменить:
  ```javascript
  const runtimeReady = import('./runtime/0.3.0/web_api.js').then(async (runtime) => {
  ```
  на:
  ```javascript
  const runtimeReady = import('./runtime/0.3.1/web_api.js').then(async (runtime) => {
  ```

- [x] **Step 2: Обновить версию в `.github/workflows/player-pages.yml`**
  В строке 25 заменить:
  ```yaml
  env:
    VERSION: 0.3.0
  ```
  на:
  ```yaml
  env:
    VERSION: 0.3.1
  ```

- [x] **Step 3: Верификация совпадения версий**
  Проверить совпадение строк `0.3.1` между `release-manifest.json`, `player/app.js` и `player-pages.yml`.

---

### Task 3: Нормализация манифеста `plugin.json` и правил `GEMINI.md`

**Files:**
- Modify: `plugin.json`
- Modify: `GEMINI.md`
- Modify: `rules/AGENTS.md`

**Interfaces:**
- Consumes: Antigravity Plugin Specification
- Produces: Манифест с валидным путем логотипа и компактные правила без псевдо-трансклюзий.

- [x] **Step 1: Исправить путь к логотипу в `plugin.json`**
  Заменить `"logo": "./assets/plugin-icon.svg"` на `"logo": "assets/plugin-icon.svg"`.
  Убедиться в наличии обязательных для Antigravity полей: `name`, `version`, `displayName`, `description`, `logo`, `suggestedPrompts`.

- [x] **Step 2: Оптимизировать `GEMINI.md`**
  Удалить некорректные псевдо-трансклюзии `- @./skills/...` и структурировать правила компактно:
  - Список доступных навыков (`tesseract-video`, `tesseract-motion`, `tesseract-design`, `tesseract-editor`).
  - Расположение бинарника CLI для Windows (`$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd`), macOS и Linux.
  - Проверка версии CLI `0.3.1`.
  - Принцип сохранения `.tsrct` проектов для неразрушающего монтажа.

- [x] **Step 3: Синхронизировать `rules/AGENTS.md`**
  Убедиться, что `rules/AGENTS.md` соответствует `GEMINI.md`, сохраняя совместимость с плагинной моделью загрузки.

---

### Task 4: Устранение кроссплатформенных багов в Python-скриптах

**Files:**
- Modify: `skills/tesseract-video/scripts/tesseract_waveform.py`
- Modify: `skills/tesseract-video/scripts/tesseract_media.py`
- Modify: `skills/tesseract-motion/scripts/tesseract_waveform.py`
- Modify: `skills/tesseract-motion/scripts/tesseract_media.py`

**Interfaces:**
- Consumes: Системные шрифты Windows / macOS / Linux, пути FFmpeg
- Produces: Стабильную генерацию спектрограмм без ошибок Fontconfig и переносимое атомарное сохранение файлов.

- [x] **Step 1: Реализовать кроссплатформенный поиск шрифтов в `tesseract_waveform.py`**
  В функции `draw_filter` заменить хардкод macOS на проверку шрифтов для всех ОС:
  ```python
  def find_diagnostic_font():
      candidates = [
          Path('/System/Library/Fonts/Supplemental/Arial.ttf'),
          Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts' / 'arial.ttf',
          Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
          Path('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'),
      ]
      for p in candidates:
          if p.is_file():
              return p
      return None

  diagnostic_font = find_diagnostic_font()
  font_option = f"fontfile='{diagnostic_font.as_posix()}':" if diagnostic_font else ''
  ```

- [x] **Step 2: Заменить `os.link` на `os.replace`**
  - В `tesseract_media.py`: в функции `atomic_run` заменить `os.link(temporary, p)` на `os.replace(temporary, p)`.
  - В `tesseract_waveform.py`: заменить `os.link(png, out)` и `os.link(js, dest)` на `os.replace`.

- [x] **Step 3: Добавить Windows-пути поиска в `tesseract_media.py::external`**
  Добавить стандартные пути поиска утилит на Windows:
  ```python
  for parent in (
      "/opt/homebrew/bin",
      "/usr/local/bin",
      r"C:\ffmpeg\bin",
      r"C:\ProgramData\chocolatey\bin"
  ):
  ```

- [x] **Step 4: Скопировать обновленные скрипты в `skills/tesseract-motion/scripts/`**
  Обеспечить 100% идентичность утилит между навыками видео и моушна.

---

### Task 5: Создание автоматизированного тест-сьюта

**Files:**
- Create: `tests/test_audit_remediation.py`

**Interfaces:**
- Consumes: Модули `skills.tesseract-video.scripts.*`, JSON-манифесты
- Produces: Автоматический регрессионный тест, проверяющий целостность репозитория.

- [x] **Step 1: Написать тест `tests/test_audit_remediation.py`**
  Тест должен покрывать:
  1. `test_version_consistency`: проверка версий `0.3.1` в `release-manifest.json`, `plugin.json`, `player/app.js`, `.github/workflows/player-pages.yml` и `cli-version.txt`.
  2. `test_plugin_manifest_antigravity_compatibility`: проверка `logo` без `./` и обязательных полей.
  3. `test_font_resolution`: проверка, что на текущей платформе шрифт корректно находится и `font_option` не пустой.
  4. `test_sound_synthesis_and_atomic_replace`: тест генерации звука `synthesize`, сохранения через `save_cue` и проверки атомарности без ошибок `os.link`.

- [x] **Step 2: Запустить тесты**
  Выполнить: `python -m unittest tests/test_audit_remediation.py`
  Ожидается: OK (все тесты пройдены успешно).

- [x] **Step 3: Финальная проверка Git статуса**
  Запустить `git status` и `git diff --stat`.
