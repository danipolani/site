run:
	hugo server -D

publish:
	hugo
	cd public && git add . &&  git status && git commit -m "regenerated site" && git push origin main