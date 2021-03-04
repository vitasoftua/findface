### Genesis App

Wrapper (Web Interface) for Find Face Security SDK.


To start project run:
```bash
make up
```
or
```bash
docker-compose up -d --build
```

To run tests run:
```bash
make test
```
or
```bash
docker-compose exec web python3 src/manage.py test src/
```


##### Next technologies are used:
- python 3.7
- Django 2.2
- djangorestframework
- django-channels
- Celery
- PostgreSQL 11
- RabbitMQ 3
- Redis 5
- nginx 1.16
- docker


##### Rest API documentation:
- http://<server_ip>/swagger
- http://<server_ip>/redoc


## Environment Variables

```POSTGRES_HOST``` uses to connect to database.

```RABBITMQ_HOST``` uses to connect to RabbitMQ.

```REDIS_HOST``` uses to connect to Redis.

```FCM_SERVER_KEY``` is Firebase Cloud Messaging server key. Uses for mobile notifications.

```FFS_API_URL``` is url to connect to FindFace API.

```FFS_API_TOKEN``` is FindFace API token. Uses FindFace API.

```FFS_UPLOAD_URL``` is url to FindFace component (findface-upload).

```WEB_HOSTNAME``` is a host name for wrapper.

```DEBUG``` uses to turn on/off debug mode. Default is ```True```


## Deploy gitlab-runner

```bash
docker-compose run runner register \
  --url "https://gitlab.com/" \
  --registration-token <PROJECT_REGISTRATION_TOKEN> \
  --description "runner" \
  --executor "docker" \
  --docker-image docker

```

Set ```privileged = true``` in config.toml


## ssl certificate 

```bash
docker run -it --rm \
-v /root/genesis/.docker_data/letsencrypt/etc/letsencrypt:/etc/letsencrypt \
-v /root/genesis/.docker_data/letsencrypt/src/letsencrypt/letsencrypt-site:/data/letsencrypt \
certbot/certbot \
certonly --webroot \
--register-unsafely-without-email --agree-tos \
--webroot-path=/data/letsencrypt \
-d genesis.oldmin.team --dry-run

```
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/genesis.oldmin.team/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/genesis.oldmin.team/privkey.pem
   Your cert will expire on 2019-08-14. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le

