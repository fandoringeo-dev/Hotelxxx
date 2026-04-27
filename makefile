# ===============================
# Настройки проекта
# ===============================
# Каталоги с кодом/тестами
PY_SRCS=hotelxxx
# Порог для Radon:
# - запрещаем функции со сложностью CC уровней E/F
# - минимальный Maintainability Index (MI)
RADON_MIN_MI=65
# ===============================
# Служебные цели
# ===============================

.PHONY: help install lint fmt type security cc hal raw check

help:
	@echo "Доступные цели:"
	@echo " lint - ruff check (с автофиксом)"
	@echo " fmt - ruff format"
	@echo " type - mypy (проверка типов)"
	@echo " security - bandit (скан безопасности)"
	@echo " cc - radon cc (цикломатическая сложность) + quality gate"
	@echo " hal - radon hal (метрика халстеда)"
	@echo " raw - radon raw (SLOC, LLOC, комментарии, число функций/классов)"
	@echo " check - быстрый локальный quality gate (ruff+mypy+bandit+radon)"


# ===============================
# Ruff: линт и форматирование
# ===============================
lint:
	uv run ruff check $(PY_SRCS) --fix

fmt:
	uv run ruff format $(PY_SRCS)

# ===============================
# Mypy: проверка типов
# (если есть mypy.ini / pyproject.toml, он подхватится автоматически)
# ===============================

type:
	uv run mypy $(PY_SRCS)

# ===============================
# Bandit: анализ безопасности
# ===============================
security:
# -r: рекурсивно, -lll: максимум строгости вывода,
# -x: исключения (подправьте под проект)
	uv run bandit -r hotelxxx -lll -x .venv,venv,build,dist,migrations

# ===============================
# Radon: метрики
# ===============================
# Цикломатическая сложность: подробный вывод (-s), среднее (-a)
cc:
	@uv run radon cc -s -a $(PY_SRCS)
	@powershell -NoProfile -Command '$$output = uv run radon cc -s $(PY_SRCS); $$bad = $$output | Where-Object { $$_ -match "\s[EF]\s" }; if ($$bad.Count -gt 0) { Write-Host "Radon CC: обнаружены функции со сложностью E/F"; exit 1 } else { Write-Host "Radon CC: нет функций с E/F" }'

# Метрика халстеда
hal:
	uv run radon hal $(PY_SRCS)
# Метрика Raw
raw:
	uv run radon raw $(PY_SRCS)

# ===============================
# Комплексные цели
# ===============================
# Локальный быстрый прогон с автофиксом Ruff
check: lint fmt type security cc hal raw
