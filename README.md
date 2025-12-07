# PROYECTO FINAL

### Versión Python 3.10

### Crear emtorno virtual

En la ruta raiz del proyecto, correr el siguiente comando(Asegurarse de tener python instalado y la libreria virtualenv)

* ``` python -m venv nombre_entorno```

Activa el entorno virtual:

    En Windows:
* ```nombre_entorno\Scripts\activate```


    En MacOS/Linux:
* ```source nombre_entorno/bin/activate```

### Variables de entorno

#### Linux/Mac
    
* ```export FLASK_APP="run.py"```
* ```export FLASK_ENV="development"```

#### Windows

* ```set "FLASK_APP=run.py"```
* ```set "FLASK_ENV=development"```
 
### Instalación de dependencias

En el proyecto se distribuye un fichero (requirements.txt) con todas las dependencias. Para instalarlas
basta con ejectuar:

* ```pip install -r requirements.txt```

## Migracion modelos de la aplicacion a la base de datos

* ```flask db init```
* ```flask db migrate -m "First migration"```
* ```flask db upgrade```
* ```flask db downgrade``` (Revertir en caso de que los cambios no funcionen)

## Ejecución con el servidor que trae Flask

Una vez que hayas descargado el proyecto, creado las variables de entorno y descargado las dependencias,
puedes arrancar el proyecto ejecutando:

* ```flask run```


### Servicio en VM

Activar entorno virtual e installar gunicorn con pip

Archivo de inicio de aplicacion(/etc/systemd/system/sistema-ventas.service)

```
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/sistema-ventas
Environment="PATH=/var/www/sistema-ventas/venv/bin"
ExecStart=/var/www/sistema-ventas/venv/bin/gunicorn -w 4 -b 0.0.0.0:3000 run:app --access-logfile access.log --error-logfile error.log

[Install]
WantedBy=multi-user.target
```