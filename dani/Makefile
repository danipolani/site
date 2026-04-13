HUGO_DIR := .

# Локальный предпросмотр
run:
	hugo server -D

# Сборка в ./public (каталог в .gitignore родительского репозитория — не коммитится)
build:
	hugo --gc

# Публикация на GitHub Pages: запушьте этот репозиторий в main —
# сработает .github/workflows/deploy-pages.yml (нужен секрет GH_PAGES_TOKEN).
# Ручной push в danipolani.github.io больше не требуется.
publish: build
	@echo "Готово: каталог public/. Залейте изменения в main — деплой через Actions."
