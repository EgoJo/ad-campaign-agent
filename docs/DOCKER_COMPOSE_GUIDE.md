# Docker Compose 使用指南

## 概述

`docker-compose.yml` 配置了完整的 Ad Campaign Agent 系统，包括：
- 6 个微服务（product, creative, strategy, meta, logs, optimizer）
- 1 个 orchestrator 服务
- 服务依赖关系和健康检查
- 统一的网络配置

## 服务列表

| 服务 | 端口 | 描述 | 依赖 |
|------|------|------|------|
| product_service | 8001 | 产品选择服务 | - |
| creative_service | 8002 | 创意生成服务 | - |
| strategy_service | 8003 | 策略生成服务 | - |
| meta_service | 8004 | Meta 平台集成 | - |
| logs_service | 8005 | 日志服务 | - |
| optimizer_service | 8007 | 优化服务 | - |
| orchestrator_agent | 8000 | 编排服务 | 所有微服务 |

## 快速开始

### 1. 启动所有服务

```bash
# 启动所有服务（后台运行）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 2. 检查服务健康状态

```bash
# 检查所有服务健康
docker-compose ps

# 手动检查 orchestrator
curl http://localhost:8000/health

# 检查所有微服务状态（通过 orchestrator）
curl http://localhost:8000/services/status
```

### 3. 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除 volumes
docker-compose down -v
```

## 环境变量配置

创建 `.env` 文件（或使用环境变量）：

```bash
# 日志级别
LOG_LEVEL=INFO

# 环境标识
ENVIRONMENT=production

# Gemini API 配置（可选，用于 LLM 功能）
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
```

## 服务依赖关系

Orchestrator 服务配置了 `depends_on`，确保：
- 所有微服务健康后才启动 orchestrator
- 使用 `service_healthy` 条件，而不是简单的启动顺序
- 每个服务都有健康检查配置

## 网络配置

所有服务连接到 `ad_campaign_network` 网络：
- 服务间使用服务名通信（如 `http://product_service:8001`）
- 外部访问使用 `localhost:端口`

## 健康检查

每个服务都配置了健康检查：
- 检查间隔：10秒
- 超时：5秒
- 重试：3次
- 启动等待期：10秒（orchestrator 30秒）

## 常见问题

### 1. 服务无法启动

```bash
# 查看服务日志
docker-compose logs orchestrator_agent

# 检查服务依赖
docker-compose ps
```

### 2. Orchestrator 无法连接微服务

确保环境变量中的服务 URL 使用 Docker 服务名：
```bash
PRODUCT_SERVICE_URL=http://product_service:8001
```

### 3. 端口冲突

如果端口被占用，修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8000:8000"  # 改为其他端口，如 "18000:8000"
```

## 开发模式

使用 volumes 挂载代码，实现热重载：

```yaml
volumes:
  - ./app:/app/app
```

修改代码后，服务会自动重新加载（如果使用 uvicorn reload）。

## 生产部署

1. **移除 volumes**（使用镜像中的代码）
2. **设置环境变量**（通过 `.env` 或环境变量）
3. **配置健康检查**（已配置）
4. **使用 Docker Swarm 或 Kubernetes**（用于生产环境）

## 验证部署

```bash
# 1. 启动所有服务
docker-compose up -d

# 2. 等待服务启动（约 30-60 秒）
sleep 30

# 3. 检查 orchestrator 健康
curl http://localhost:8000/health

# 4. 检查所有服务状态
curl http://localhost:8000/services/status

# 5. 测试创建活动（需要 GEMINI_API_KEY）
curl -X POST http://localhost:8000/create_campaign_nl \
  -H "Content-Type: application/json" \
  -d '{"user_request": "Create a campaign for electronics with $1000 budget"}'
```

## 服务 URL 配置

在 Docker 环境中，服务间通信使用服务名：

| 环境 | 服务 URL 格式 |
|------|--------------|
| Docker Compose | `http://service_name:port` |
| 本地开发 | `http://localhost:port` |

Orchestrator 会自动从环境变量读取服务 URL，Docker Compose 已配置正确的服务名。

