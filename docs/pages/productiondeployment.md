---
layout: page
title: Production Deployment
use-site-title: true
---

The deployment of MobyDQ into **production environment** is similar to a local setup but requires some changes for the application to run on a remote server. Follow the steps described in the [Getting Started](/mobydq/pages/gettingstarted) page and apply the changes below once you are done.

-   [Create SSL Certificate](#create-ssl-certificate)
-   [Update Nginx Configuration](#update-nginx-configuration)
-   [Run Docker Containers](#run-docker-containers)

---

# Create SSL Certificate

If you followed the [Getting Started](/mobydq/pages/gettingstarted) page, you already have a self-signed certificate and its key generated in the project folder `./nginx/config`. See files:

-   `./nginx/config/cert.pem`
-   `./nginx/config/key.pem`

You can reuse this certificate or generate an official one on [Let's Encrypt](https://letsencrypt.org/). If you run MobyDQ on a secured private corporate network, a self-signed certificate is probably enough.

---

# Update Nginx Configuration

Update the file `./nginx/config/nginx.conf` to ensure it is aligned with your host name and that it uses the SSL certificate you created. You should modify in particular the following parameters.

-   `server_name`: two occurences in the file. It must contain your host name without `https://`
-   `ssl_certificate`: one occurence in the file. You can keep the default value `/etc/nginx/cert.pem;` if you use the self-signed certificate created in the [Getting Started](/mobydq/pages/gettingstarted) page.
-   `ssl_certificate_key`: one occurence in the file. You can keep the default value `/etc/nginx/key.pem;` if you use the self-signed certificate created in the [Getting Started](/mobydq/pages/gettingstarted) page.

Example:

```
[...]
# Server for https
server {
    listen       443 ssl http2;
    server_name  mobydq.net;

    ssl_certificate      /etc/letsencrypt/live/mobydq.net/fullchain.pem;
    ssl_certificate_key  /etc/letsencrypt/live/mobydq.net/privkey.pem;
    [...]
}
[...]
# Default server to redirect http requests to https
server {
    listen 80 default_server;
    server_name mobydq.net;
    listen [::]:80 default_server;
    [...]
}
```

---

# Run Docker Containers

To start all the Docker containers as deamons, go to the project root and execute the following command in your terminal window.

```shell
$ cd mobydq
$ docker-compose up -d db graphql app nginx
```

The web application and the GraphQL API can be accessed at the following addresses depending on your host name.

-   Web application: `https://<host_name>`
-   GraphQL API interactive documentation: `https://<host_name>/graphiql`
-   GraphQL API: `https://<host_name>/graphql`
