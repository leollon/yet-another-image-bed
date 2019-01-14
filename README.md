# A image bed is ready for my blog, which supports https.

[中文部署文档](README_ZH_CN.md)

# Acknowledgements
- [letsencrypt](https://letsencrypt.org/)
- [flask](https://github.com/pallets/flask)
- [docker-ce](https://www.docker.com/community-edition)
- [docker-compose](https://github.com/docker/compose)
- [sm.ms](https://sm.ms)

## Ambition
> Letsencrypt provides SSL/TLP certificate to support https, code based on my
> personal needs, and practise what I've learned from docker and docker-compose.

## Deploy

1. $ git clone https://github.com/leollon/yet-another-image-bed.git imgbed-project
2. $ sudo bash onekey-deploy.sh
3. paste this configuration to your nginx vhost in the server block.

    **Note: modify username to your username, then `ctrl+c` and `ctrl+v`, yeah.**
    ```
    location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_buffering off;
            proxy_pass http://127.0.0.1:5050;
        }

        location ^~ /static/ {
            alias /home/username/imgbed-project/static_files/;
        }

        location ~* \.(jpg|jpeg|png|gif|svg) {
            # serving uploaded images
            root /home/username/imgbed-project/uploaded_images;
        }
    ```

### ToDO
   - [x] upload/remove an image
   - [x] deploy with docker compose
   - [x] view all uploaded images

### Modifications based on your needs

- config.py

  >set mongoengine connection, the max size of each uploaded image and so on.

- compose/local/mongodb/createUser.js
  > set user and password for imgbed document

## License 
> [GNU LV3](./LICENSE)
