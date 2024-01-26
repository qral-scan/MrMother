
d=docker
name=telegram_notify_bot
container_name=usb_ios

build: clean
	docker build -t $(name)-$(container_name) . 

start: build
	docker run \
    $(name)-$(container_name)
	
clean:
	docker volume prune -f
	docker system prune -f