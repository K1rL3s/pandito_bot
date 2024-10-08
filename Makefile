.PHONY: up down logs flush monitor

up:
	docker compose up --build --remove-orphans

down:
	docker compose down

logs:
		docker compose logs -f

flush:
	docker compose down -v

monitor:
	python3 monitor/main.py