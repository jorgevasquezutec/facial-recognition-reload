IMAGE_NAME=facial-recognition-reload
VERSION=v1.0.0
TAR_FILE = $(IMAGE_NAME)-$(VERSION).tar
GZIP_FILE = $(TAR_FILE).gz
DOCKER_HUB_ID= jorgevasquezutec


build-image:
	docker build -t $(IMAGE_NAME):$(VERSION) .

save-image: build-image
	docker save -o $(TAR_FILE) $(IMAGE_NAME):$(VERSION) 
	gzip -f $(TAR_FILE)

conda-update:
	conda env update --prune -f environment.yml

pip-tools:
	python -m pip install pip-tools
	pip-compile requirements/prod.in

# execute after pull this repo
	pip-sync requirements/prod.txt


pip-tools-dev:
	python -m pip install pip-tools
	pip-compile requirements/dev.in

# execute after pull this repo
	pip-sync requirements/dev.txt


run:
	python .

watch:
	uvicorn app.app:app --reload

extract-chroma:
	 docker cp chroma:/chroma/chroma/. ./db

import-chroma:
	docker cp ./db/. chroma:/chroma/chroma/

delete-chroma:
	docker exec chroma rm -rf /chroma/chroma/

seed:
	python -m app.seeders.uploadChunk './other/*.jpg' --chunk 25

seed-1:
	python -m app.seeders.uploadChunk './dnis/*.jpg' --chunk 30


hub:
	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_HUB_ID)/$(IMAGE_NAME):$(VERSION)
	docker push $(DOCKER_HUB_ID)/$(IMAGE_NAME):$(VERSION)


hub-image:
	echo $(DOCKER_HUB_ID)/$(IMAGE_NAME):$(VERSION)