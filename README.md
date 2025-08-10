# Marshmallow

基于 FastAPI / React 的自用棉花糖。

## 环境部署

```sh
apt install python3 python3-pip python3-venv
apt install postgresql
apt install redis-server
systemctl enable redis-server --now
python3 -m venv /usr/venv/fastapi
source /usr/venv/fastapi/bin/activate
pip install -r requirements.txt
```

### PostgreSQL

```sql
-- 创建数据库
CREATE DATABASE marshmallow;
-- 启用 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- 创建用户
CREATE USER {username} WITH PASSWORD '{password}';
-- 授予用户对 marshmallow 数据库的全部权限
GRANT ALL PRIVILEGES ON DATABASE marshmallow TO {username};
-- 授予用户对 SCHEMA public 的使用、创建权限
GRANT USAGE, CREATE ON SCHEMA public TO {username};
```

### Redis

编辑 `/etc/redis/redis.conf`

```conf
# 启用 UNIX socket
unixsocket /run/redis/redis-server.sock
unixsocketperm 770

# 关闭 TCP/IP 监听
port 0
```

重启 Redis，并且确保权限设置正确。

```sh
systemctl restart redis-server
chown redis:redis /run/redis/redis-server.sock
chmod 770 /run/redis/redis-server.sock
usermod -aG redis www-data
```

测试连接 Redis 服务

```sh
redis-cli -s /run/redis/redis-server.sock
```

- 查看服务是否运行 `PING`
- 获取服务器信息 `INFO`
- 查找以 marshmallow 为开头的 Key `KEYS marshmallow*`
- 退出 `QUIT`

### Uvicorn

- 读取反向代理的 HTTP 头 `--proxy-headers`
- 允许读取反向代理头的来源 IP `--forwarded-allow-ips='*'`

```sh
# 运行
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
uvicorn main:app --uds /run/uvicorn/uvicorn.sock --proxy-headers
```

使用 `systemd` 管理 `Uvicorn` 服务。
编辑 `/etc/systemd/system/marshmallow.service`

```systemd
[Unit]
Description=Marshmallow FastAPI
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/Marshmallow/app
ExecStart=/usr/venv/fastapi/bin/uvicorn main:app \
    --uds /run/uvicorn/uvicorn.sock \
    --proxy-headers \
    --forwarded-allow-ips='*' \
    --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

启动 && 开机启动

```sh
systemctl enable marshmallow --now
```

### Nginx

`/etc/nginx/conf.d/marshmallow.conf`

```conf
server {
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name _;
    charset utf-8;

    server_tokens off;

    http2 on;

    ssl_certificate /etc/ssl/fullchain.pem;
    ssl_certificate_key /etc/ssl/privkey.pem;
    add_header Strict-Transport-Security "max-age=63072000" always;

    location /marshmallow {
        proxy_pass http://unix:/run/uvicorn/uvicorn.sock;

        # 保留原始请求信息
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
