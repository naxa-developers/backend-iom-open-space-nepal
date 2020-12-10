version: "3"

services:
  web:
    image: openspace:0.0.1
    restart: always
    container_name: web
    ports:
      - "8060:8000"
    volumes:
      - ./sock/:/sock/
      - .:/code
      - ./logs/:/logs/
    command: sh entrypoint.sh
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - openspace

  nginx:
    image: nginx:latest
    container_name: nginx
    restart: always
    ports:
      - 80:80
      - 443:443 
    volumes:
      - ./nginx/nginx-proxy.conf:/etc/nginx/conf.d/default.conf
      - ../openspace-frontend/dist:/var/www/frontend
      - ./sock/:/sock/
      - ./logs/nginx:/var/log/nginx
      - ./static:/static
    networks:
      - openspace
  
  db:
    image: mdillon/postgis:11-alpine
    container_name: db
    restart: always
    volumes:
      - ../postgres_data:/var/lib/postgresql/data/
    ports: 
      - 5432:5432
    env_file:
      - postgres.env
    networks:
      - openspace

networks:
  openspace:
    driver: bridge
