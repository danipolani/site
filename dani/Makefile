run:
	hugo server -D

publish:
	hugo
	cd public && git add . &&  git status && git commit -m "regenerated site" && git push origin main

voc:
	cd scripts && pipenv run python generate_voc.py

jup:
	cd scripts && pipenv run jupyter notebook