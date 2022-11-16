# DOCKER RUN
- build image:      docker build ./docker -t robotbase_a
- run container:    docker run -it --name robot -p 5001:5000 -v %cd%/src:/code imgpython310
- stop container:   docker stop robot
- borrar container: docker rm robot
- connect tty:      docker exec -it robot /bin/bash

# COMPOSE:
- build image:          docker build ./docker -t robotbase_a
- levantar todo:        docker compose up -d
- manejar contenedor:   docker compose {start|stop|up -d} cont_name

