build_production:
	docker-compose -f docker-compose.build.yml build live
build_test:
	docker-compose -f docker-compose.build.yml build dev
push_production:
	docker-compose -f docker-compose.build.yml push live
push_test:
	docker-compose -f docker-compose.build.yml push dev
pull_production:
	docker-compose -f docker-compose.build.yml pull live
pull_test:
	docker-compose -f docker-compose.build.yml pull dev
restart:
	docker-compose restart
start:
	docker-compose up -d
down:
	docker-compose down
