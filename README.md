# info_vacinas

Projeto web para disponibilizar informações sobre vacinas.

O projeto utiliza a linguagem de programação Python com o framework Flask
e banco de dados Postgres.

A aplicação está disponível na internet, no endereço: https://info-vacinas.herokuapp.com/

## Clonar o projeto

```sh
$ git clone https://github.com/univesp-projeto-integrador-1/info_vacinas.git
```


## Instalar as dependências

```sh
$ pip install -r requirements.txt
```

# Setup

Use this guide if you do NOT want to use Docker in your project.

## Getting Started

Create and activate a virtual environment, and then install the requirements.

### Set Environment Variables

Update *project/server/config.py*, and then run:

```sh
$ export APP_NAME="info_vacinas"
$ export APP_SETTINGS=project.server.config.ProductionConfig
$ export FLASK_DEBUG=0
```

By default the app is set to use the production configuration. If you would like to use the development configuration, you can alter the `APP_SETTINGS` environment variable:

```sh
$ export APP_SETTINGS=project.server.config.DevelopmentConfig
```

### Create DB

```sh
$ python manage.py create-db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create-admin
$ python manage.py create-data
```

### Run the Application

```sh
$ python manage.py run
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```

Run flake8 on the app:

```sh
$ python manage.py flake
```

or

```sh
$ flake8 project
```

