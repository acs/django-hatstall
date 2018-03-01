VERSION= $(shell grep '_version_' ../../_version.py  | awk -F '"' '{print $$2}') 
IMAGE='olblak/hatstall'

build:
	docker build -t $(IMAGE):$(VERSION) -f Dockerfile ../..

run:
	docker run -i -t --rm $(IMAGE):$(VERSION)
