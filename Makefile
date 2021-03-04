.PHONY: requirements freeze syncdb user install exec up build down ps test clean push pull

requirements:
	-@echo "### Installing requirements"
	-@docker-compose -f docker-compose.yml exec web pip3 install -r requirements.txt

freeze:
	-@echo "### Freezing python packages to requirements.txt"
	-@docker-compose -f docker-compose.yml exec web pip3 freeze > requirements.txt

syncdb:
	-@echo "### Creating database tables and loading fixtures"
	-@docker-compose -f docker-compose.yml exec web python3 src/manage.py makemigrations
	-@docker-compose -f docker-compose.yml exec web python3 src/manage.py migrate

user:
	-@docker-compose -f docker-compose.yml exec web python3 src/manage.py createsuperuser

ifeq (install,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
install:
	-@echo $(RUN_ARGS) >> requirements.txt
	-@docker-compose -f docker-compose.yml up -d --build
	-@docker-compose -f docker-compose.yml exec web pip3 freeze > requirements.txt

ifeq (exec,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
exec:
	-@docker-compose -f docker-compose.yml exec web python3 src/manage.py $(RUN_ARGS)

up:
	-@docker-compose -f docker-compose.yml up -d --build

down:
	-@docker-compose -f docker-compose.yml down

ps:
	-@docker-compose -f docker-compose.yml ps

logs:
	-@docker-compose -f docker-compose.yml logs -f

test:
	-@docker-compose -f docker-compose.yml exec web python3 src/manage.py test src/

ifeq (testapp,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
testapp:
	-@docker-compose -f docker-compose.yml exec web python3 src/manage.py test src/api/$(RUN_ARGS)

ifeq (testclass,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
testclass:
	-@docker-compose -f docker-compose.yml exec web python3 src/manage.py test $(RUN_ARGS)

clean:
	-@echo "### Cleaning *.pyc and .DS_Store files"
	-@find . | grep -E "(__pycache__|\.pyc|\.pyo|\.DS_Store$)" | xargs rm -rf

messages:
	-@echo "### Creating messages"
	-@docker-compose -f docker-compose.yml exec web python3 src/manage.py makemessages
	-@docker-compose -f docker-compose.yml exec web python3 src/manage.py compilemessages

push:
	docker build -f etc/docker/Dockerfile -t registry.gitlab.com/oldminteam/genesis .
	docker push registry.gitlab.com/oldminteam/genesis

gen-swagger:
	-@docker-compose exec web python src/manage.py generate_swagger swagger.json
