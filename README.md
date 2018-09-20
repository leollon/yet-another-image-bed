# A image bed is ready for my blog, which supports https.

# Thanks
- [letsencrypt](https://letsencrypt.org/)
- [flask](https://github.com/pallets/flask)
- [docker-ce](https://www.docker.com/community-edition)
- [docker-compose](https://github.com/docker/compose)

## Aim
> Letsencrypt provides SSL/TLP certificate to support https.


## Deploy

```
$ sudo bash onekey-deploy.sh
```

### Modification based on your needs

- config.py

  >set mongoengine connection, the max size of each uploaded image and so on.

- compose/production/mongodb/createUser.js
  > set user for imgbed document

## License 
> [GNU LV3](./LICENSE)