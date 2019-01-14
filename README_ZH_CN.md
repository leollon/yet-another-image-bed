# 自建属于你自己的图床

# 致谢
- [letsencrypt](https://letsencrypt.org/)
- [flask](https://github.com/pallets/flask)
- [docker-ce](https://www.docker.com/community-edition)
- [docker-compose](https://github.com/docker/compose)
- [sm.ms](https://sm.ms)

## 目的
> 为了使[我的动态博客](https://blog.quantuminit.com)支持全站https，所以跟着flask文档并阅读docker官方文档，进行开发与部署，个人需求驱使，也属于填坑项吧。

## 部署

1. $ git clone https://github.com/leollon/yet-another-image-bed.git imgbed-project
2. $ sudo bash onekey-deploy.sh
3. paste this configuration to your nginx vhost in the server block.
3. 复制下面这段配置到Nginx server 块中。

    **注意: 更改username为你自己的username, 然后 `ctrl+c`，接着 `ctrl+v`, 是的，没错。**
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

### 待做
   - [x] 上传/删除一张照片
   - [x] 使用docker compose部署
   - [x] 查看所有上传的图片

### 自定义个人配置

- config.py

  > 设置mongoengine 连接，限制上传的图片的大小等等。

- compose/local/mongodb/createUser.js
  > 为`imgbed`文档数据库设置用户名和密码

## License 
> [GNU LV3](./LICENSE)
