VERSION= $(shell grep '_version_' ../../_version.py  | awk -F '"' '{print $$2}') 
IMAGE='grimoirelab/hatstall'

build:
	docker build -t $(IMAGE):$(VERSION) -f Dockerfile ../..

publish:
	docker push $(IMAGE):$(VERSION)

run:
	docker run -i -t --rm $(IMAGE):$(VERSION)
