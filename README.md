# Project Setup

Follow the steps below to set up and run the project locally using Docker.

## 1. Clone the repository

First, clone the repository to your local machine:

```bash
git clone <repository_url>
```

## 2. Navigate to the project directory

```bash
cd <project_directory>
```

## 3. Build the Docker images

```bash
docker-compose build
```

## 4. Start the Docker containers

```bash
docker-compose up -d
```

## 5. Run migrations

```bash
docker-compose exec django python manage.py migrate
```

Replace `<repository_url>` and `<project_directory>` with the actual values for your project.
