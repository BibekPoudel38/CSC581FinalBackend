
# CSC 581 Advanced Computer Engineering Backend (Django)

Final project for Advanced Software Engineering




## Authors

- [@BibekPoudel38](https://github.com/BibekPoudel38)



## Installation

Requirements

```bash
  Docker 
  Python
```
Install Docker (https://docs.docker.com/engine/install/)
    
## Run Locally

Clone the project

```bash
  git clone https://github.com/BibekPoudel38/CSC581FinalBackend.git
```

Go to the project directory

```bash
  cd CSC581FinalBackend
```
Start the server

```bash
  docker compose up -d --build
  docker exec -it django-app python3 manage.py migrate
  docker exec -it django-app python3 manage.py createsuperuser
```


## FAQ

#### Server not running or has some errors? we can delete all the files and build again

```bash
docker stop `docker ps -qa` > /dev/null 2>&1;
docker system prune --volumes --all;
```

