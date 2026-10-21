.PHONY: up down logs test backend-test frontend-check

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

test: backend-test frontend-check

backend-test:
	cd backend && pytest

frontend-check:
	cd frontend && pnpm run check && pnpm run build

