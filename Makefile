make push:
	docker build -t "localhost:5000/addon-operator-poc:latest" . 
	docker push localhost:5000/addon-operator-poc:latest

make test:
	kubectl apply -k .
	kubectl rollout restart deployment/addon-operator