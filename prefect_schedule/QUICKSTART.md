# Prefect Docker 快速入门 🚀

## 一键启动（推荐）

### 方式 1：使用启动脚本

```bash
./start.sh
```

### 方式 2：使用 Makefile

```bash
make start
```

这将自动完成：
- ✅ 创建必要的目录
- ✅ 生成环境变量文件
- ✅ 启动所有 Docker 服务
- ✅ 健康检查

## 访问 UI

浏览器打开：**http://localhost:4200**

## 部署你的第一个 Flow

### 步骤 1：创建 Work Pool

```bash
docker-compose exec prefect-server prefect work-pool create default --type process
```

### 步骤 2：部署 Flow

```bash
# 方式 1：使用脚本
./deploy-flow.sh

# 方式 2：使用 Makefile
make deploy

# 方式 3：手动执行
docker-compose exec prefect-server sh -c "cd /flows && prefect deploy --all"
```

### 步骤 3：手动运行（测试）

```bash
docker-compose exec prefect-server prefect deployment run 'get-repo-info/github-repo-info-deployment'
```

### 步骤 4：查看执行结果

访问 UI 查看 flow runs：http://localhost:4200/flow-runs

## 常用命令速查

### 使用 Makefile（推荐）

```bash
make help           # 显示所有命令
make start          # 启动服务
make stop           # 停止服务
make restart        # 重启服务
make logs           # 查看日志
make ps             # 查看状态
make deploy         # 部署 flow
make backup         # 备份数据库
make health         # 健康检查
```

### 使用 Docker Compose

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 查看状态
docker-compose ps

# 重启服务
docker-compose restart
```

## 目录结构

```
prefect_schedule/
├── docker-compose.yml          # 开发环境配置 ⭐
├── docker-compose.prod.yml     # 生产环境配置
├── env.template                # 环境变量模板
├── nginx.conf                  # Nginx 配置
├── Makefile                    # 快捷命令 ⭐
├── start.sh                    # 启动脚本 ⭐
├── deploy-flow.sh             # 部署脚本 ⭐
├── QUICKSTART.md              # 本文件
├── README.docker.md           # 详细文档
│
├── flows/                      # Flow 代码目录 📝
│   └── flow.py                # 你的 flow 文件
├── data/                       # 数据目录
├── backups/                    # 备份目录
└── ssl/                        # SSL 证书（生产环境）
```

## 管理 Flow

### 查看 Deployments

```bash
docker-compose exec prefect-server prefect deployment ls
```

### 查看 Work Pools

```bash
docker-compose exec prefect-server prefect work-pool ls
```

### 查看 Flow Runs

```bash
docker-compose exec prefect-server prefect flow-run ls --limit 10
```

### 手动触发 Deployment

```bash
docker-compose exec prefect-server prefect deployment run 'FLOW_NAME/DEPLOYMENT_NAME'
```

## 查看日志

### 查看所有日志

```bash
docker-compose logs -f
```

### 查看特定服务日志

```bash
# Server 日志
docker-compose logs -f prefect-server

# Worker 日志
docker-compose logs -f prefect-worker

# 数据库日志
docker-compose logs -f postgres
```

## 调试技巧

### 进入容器

```bash
# 进入 server 容器
docker-compose exec prefect-server bash

# 进入 worker 容器
docker-compose exec prefect-worker bash

# 进入数据库容器
docker-compose exec postgres psql -U prefect
```

### 检查服务健康

```bash
# API 健康检查
curl http://localhost:4200/api/health

# 数据库连接检查
docker-compose exec postgres pg_isready -U prefect

# 查看容器状态
docker-compose ps
```

### 重启单个服务

```bash
docker-compose restart prefect-server
docker-compose restart prefect-worker
```

## 扩展 Worker

```bash
# 启动 3 个 worker 实例
docker-compose up -d --scale prefect-worker=3

# 使用 Makefile
make scale-workers
# 然后输入数量
```

## 备份与恢复

### 备份数据库

```bash
# 使用 Makefile
make backup

# 或手动备份
docker-compose exec postgres pg_dump -U prefect prefect > backup.sql
```

### 恢复数据库

```bash
cat backup.sql | docker-compose exec -T postgres psql -U prefect prefect
```

## 停止服务

### 保留数据

```bash
docker-compose down
```

### 删除所有数据（危险）

```bash
docker-compose down -v
```

## 生产环境部署

### 1. 创建 .env 文件

```bash
cp env.template .env
# 编辑 .env，修改密码和域名
```

### 2. 配置 SSL 证书

```bash
# 将证书放入 ssl 目录
cp your-cert.pem ssl/cert.pem
cp your-key.pem ssl/key.pem

# 修改 nginx.conf，启用 HTTPS
```

### 3. 启动生产环境

```bash
make start-prod
```

## 常见问题

### Q: Worker 无法连接到 Server？

**A:** 检查网络和 API URL：

```bash
docker-compose exec prefect-worker env | grep PREFECT_API_URL
docker-compose exec prefect-worker curl http://prefect-server:4200/api/health
```

### Q: Flow 代码修改后如何更新？

**A:** 重新部署：

```bash
# 1. 修改 flows/flow.py
# 2. 重新部署
make deploy
```

### Q: 如何查看具体的 Flow Run 日志？

**A:** 在 UI 中查看：http://localhost:4200/flow-runs，点击具体的 run

### Q: 数据库占用空间过大？

**A:** 清理旧的 flow runs（在 UI 中操作或使用 API）

### Q: 时区不对？

**A:** 检查 `.env` 中的 `TZ=Asia/Shanghai`，重启服务：

```bash
docker-compose restart
```

## 性能优化

### 增加 Worker 数量

```bash
docker-compose up -d --scale prefect-worker=5
```

### 调整资源限制

编辑 `docker-compose.yml`，修改 `deploy.resources` 配置。

## 监控

### 查看资源使用

```bash
docker stats
```

### 查看磁盘使用

```bash
docker system df
```

## 更多信息

- 📚 详细文档：`README.docker.md`
- 🌐 Prefect 官方文档：https://docs.prefect.io/
- 💬 社区支持：https://discourse.prefect.io/

## 快速命令参考卡

```bash
# 启动
./start.sh                   或  make start

# 部署
./deploy-flow.sh            或  make deploy

# 查看日志
make logs

# 查看状态
make ps

# 健康检查
make health

# 备份
make backup

# 停止
make stop
```

---

**祝使用愉快！** 🎉

有问题请查看 `README.docker.md` 获取更详细的文档。

