HUGO_DIR := .

run:
	hugo server -D

build:
	hugo --gc

publish: build
	@echo "Готово: каталог public/. Залейте изменения в main — деплой через Actions."

commit:
	git add . && git commit -m "updated site" && git push
