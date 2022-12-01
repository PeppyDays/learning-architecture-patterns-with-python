local-up:
	docker compose -p allocation -f docker-compose.yaml up -d

local-down:
	docker compose down

test:
	pytest --tb=short -vvv
