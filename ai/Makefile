IMAGE_NAME=ai-api
CONTAINER_NAME=ai-api-container

build:
	docker build -t ${IMAGE_NAME} .

run:
	docker run -d -p 8080:80 --name ${CONTAINER_NAME} ${IMAGE_NAME}

clean:
	docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}
