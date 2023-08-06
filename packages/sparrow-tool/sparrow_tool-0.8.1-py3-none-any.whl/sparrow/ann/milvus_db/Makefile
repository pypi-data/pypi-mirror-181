set-env:
	pip install protobuf==3.20.0 grpcio-tools
	pip install pymilvus==2.2.0

start:
	@sudo docker compose up -d
#	@sudo docker-compose up -d

stop:
	@sudo docker-compose down

rm-data:
	@sudo rm -rf volumes