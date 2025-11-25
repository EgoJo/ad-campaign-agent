# 部署指南

本文档提供 Ad Campaign Agent 系统的完整部署指南，包括本地开发、Docker 部署和生产环境部署。

## 目录

- [部署方式概览](#部署方式概览)
- [本地开发部署](#本地开发部署)
- [Docker Compose 部署](#docker-compose-部署)
- [生产环境部署](#生产环境部署)
- [环境变量配置](#环境变量配置)
- [服务监控](#服务监控)
- [备份和恢复](#备份和恢复)

---

## 部署方式概览

| 部署方式 | 适用场景 | 复杂度 | 推荐度 |
|---------|---------|--------|--------|
| 本地开发 | 开发和测试 | ⭐ 低 | ✅ 推荐 |
| Docker Compose | 单机部署、演示 | ⭐⭐ 中 | ✅ 推荐 |
| Kubernetes | 生产环境、高可用 | ⭐⭐⭐ 高 | ✅ 生产推荐 |
| Docker Swarm | 小规模生产 | ⭐⭐ 中 | ⚠️ 可选 |

---

## 本地开发部署

### 前置要求

- Python 3.11+
- pip
- (可选) Google Gemini API Key

### 步骤 1: 克隆仓库

```bash
git clone <repository-url>
cd ad-campaign-agent
```

### 步骤 2: 创建虚拟环境

```bash
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 步骤 3: 安装依赖

```bash
# 使用 Makefile
make install

# 或手动安装
pip install -r requirements.txt
```

### 步骤 4: 配置环境变量

创建 `.env` 文件（可选，本地开发使用默认值）：

```bash
# .env
LOG_LEVEL=INFO
ENVIRONMENT=development
GEMINI_API_KEY=your_api_key_here  # 可选
```

### 步骤 5: 启动服务

```bash
# 启动所有微服务
make start-services

# 启动 orchestrator
make start-orchestrator

# 或使用脚本
./scripts/start_services.sh
./scripts/start_orchestrator_llm.sh
```

### 步骤 6: 验证部署

```bash
# 检查所有服务健康状态
make health-check

# 或手动检查
curl http://localhost:8000/health
curl http://localhost:8001/health
# ... 其他服务
```

---

## Docker Compose 部署

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+ (或 docker compose)

### 步骤 1: 准备环境变量

创建 `.env` 文件：

```bash
# .env
LOG_LEVEL=INFO
ENVIRONMENT=production
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
```

### 步骤 2: 构建和启动

```bash
# 构建镜像并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 步骤 3: 验证部署

```bash
# 检查服务健康
docker-compose ps

# 测试 orchestrator
curl http://localhost:8000/health

# 测试所有服务状态
curl http://localhost:8000/services/status
```

### 步骤 4: 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除 volumes
docker-compose down -v
```

### 配置说明

Docker Compose 配置了：
- ✅ 7 个服务（6 个微服务 + 1 个 orchestrator）
- ✅ 服务依赖关系（orchestrator 等待所有微服务健康）
- ✅ 健康检查（所有服务）
- ✅ 服务间网络通信（使用服务名）
- ✅ 环境变量配置

详细配置见 [DOCKER_COMPOSE_GUIDE.md](./DOCKER_COMPOSE_GUIDE.md)

---

## 生产环境部署

### 选项 1: Kubernetes 部署

#### 前置要求

- Kubernetes 1.20+
- kubectl
- Helm 3.0+ (可选)

#### 步骤 1: 创建命名空间

```bash
kubectl create namespace ad-campaign
```

#### 步骤 2: 创建 ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ad-campaign-config
  namespace: ad-campaign
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  PRODUCT_SERVICE_URL: "http://product-service:8001"
  CREATIVE_SERVICE_URL: "http://creative-service:8002"
  # ... 其他服务 URL
```

```bash
kubectl apply -f configmap.yaml
```

#### 步骤 3: 创建 Secret

```bash
kubectl create secret generic ad-campaign-secrets \
  --from-literal=GEMINI_API_KEY=your_api_key \
  -n ad-campaign
```

#### 步骤 4: 部署服务

为每个服务创建 Deployment 和 Service：

```yaml
# product-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
  namespace: ad-campaign
spec:
  replicas: 2
  selector:
    matchLabels:
      app: product-service
  template:
    metadata:
      labels:
        app: product-service
    spec:
      containers:
      - name: product-service
        image: ad-campaign-agent:latest
        command: ["python", "-m", "app.services.product_service.main"]
        ports:
        - containerPort: 8001
        env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: ad-campaign-config
              key: LOG_LEVEL
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: product-service
  namespace: ad-campaign
spec:
  selector:
    app: product-service
  ports:
  - port: 8001
    targetPort: 8001
  type: ClusterIP
```

```bash
kubectl apply -f product-service-deployment.yaml
# 为其他服务创建类似的部署文件
```

#### 步骤 5: 部署 Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ad-campaign-ingress
  namespace: ad-campaign
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /orchestrator
        pathType: Prefix
        backend:
          service:
            name: orchestrator-agent
            port:
              number: 8000
      - path: /product
        pathType: Prefix
        backend:
          service:
            name: product-service
            port:
              number: 8001
      # ... 其他服务
```

### 选项 2: Docker Swarm 部署

```bash
# 初始化 Swarm
docker swarm init

# 部署 stack
docker stack deploy -c docker-compose.yml ad-campaign

# 查看服务
docker service ls

# 扩展服务
docker service scale ad-campaign_product_service=3
```

### 选项 3: 云平台部署

#### AWS ECS

1. 构建并推送镜像到 ECR
2. 创建 ECS 任务定义
3. 创建 ECS 服务
4. 配置 ALB 负载均衡器

#### Google Cloud Run

```bash
# 构建镜像
gcloud builds submit --tag gcr.io/PROJECT_ID/ad-campaign-agent

# 部署服务
gcloud run deploy product-service \
  --image gcr.io/PROJECT_ID/ad-campaign-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name product-service \
  --image ad-campaign-agent:latest \
  --dns-name-label product-service \
  --ports 8001
```

---

## 环境变量配置

### 必需变量

| 变量 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `LOG_LEVEL` | 日志级别 | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `ENVIRONMENT` | 环境标识 | `development` | `development`, `production` |

### 可选变量

| 变量 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `GEMINI_API_KEY` | Gemini API 密钥 | `None` | `AIza...` |
| `GEMINI_MODEL` | Gemini 模型 | `gemini-2.0-flash-exp` | `gemini-pro` |

### 服务 URL 配置

在 Docker/Kubernetes 环境中，使用服务名：

```bash
PRODUCT_SERVICE_URL=http://product_service:8001
CREATIVE_SERVICE_URL=http://creative_service:8002
# ... 其他服务
```

在本地开发中，使用 localhost：

```bash
PRODUCT_SERVICE_URL=http://localhost:8001
CREATIVE_SERVICE_URL=http://localhost:8002
# ... 其他服务
```

---

## 服务监控

### 健康检查

所有服务提供 `/health` 端点：

```bash
# 检查单个服务
curl http://localhost:8001/health

# 检查所有服务（通过 orchestrator）
curl http://localhost:8000/services/status
```

### 日志收集

#### 本地开发

日志文件位于 `logs/` 目录：

```bash
tail -f logs/product_service.log
tail -f logs/orchestrator_llm.log
```

#### Docker Compose

```bash
# 查看所有日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f orchestrator_agent
```

#### Kubernetes

```bash
# 查看 Pod 日志
kubectl logs -f deployment/product-service -n ad-campaign

# 查看所有服务日志
kubectl logs -f -l app=ad-campaign -n ad-campaign
```

### 指标监控

建议集成：
- **Prometheus** - 指标收集
- **Grafana** - 可视化
- **ELK Stack** - 日志分析
- **Datadog** - APM 和监控

---

## 备份和恢复

### 数据库备份

如果使用数据库（PostgreSQL/MongoDB）：

```bash
# PostgreSQL
pg_dump -h localhost -U user -d ad_campaign > backup.sql

# MongoDB
mongodump --uri="mongodb://localhost:27017/ad_campaign" --out=/backup
```

### 配置备份

```bash
# 备份环境变量
cp .env .env.backup

# 备份 Docker Compose 配置
cp docker-compose.yml docker-compose.yml.backup
```

### 恢复

```bash
# 恢复数据库
psql -h localhost -U user -d ad_campaign < backup.sql

# 恢复配置
cp .env.backup .env
```

---

## 性能优化

### 资源限制

**推荐配置：**

| 服务 | CPU | 内存 | 副本数 |
|------|-----|------|--------|
| orchestrator | 500m | 512Mi | 2 |
| product_service | 200m | 256Mi | 2 |
| creative_service | 500m | 1Gi | 2 |
| strategy_service | 200m | 256Mi | 2 |
| meta_service | 200m | 256Mi | 2 |
| logs_service | 100m | 128Mi | 1 |
| optimizer_service | 200m | 256Mi | 1 |

### 缓存策略

- 使用 Redis 缓存产品数据
- 缓存策略生成结果
- 缓存创意生成结果（TTL: 1小时）

### 数据库优化

- 使用连接池
- 添加数据库索引
- 定期清理历史数据

---

## 安全建议

1. **API 认证**
   - 实现 API Key 认证
   - 使用 OAuth 2.0
   - JWT Token 验证

2. **网络安全**
   - 使用 HTTPS
   - 配置防火墙规则
   - 限制服务间通信

3. **密钥管理**
   - 使用密钥管理服务（AWS Secrets Manager, HashiCorp Vault）
   - 不在代码中硬编码密钥
   - 定期轮换密钥

4. **访问控制**
   - 实现 RBAC
   - 限制管理员访问
   - 审计日志

---

## 故障恢复

### 服务重启

```bash
# Docker Compose
docker-compose restart orchestrator_agent

# Kubernetes
kubectl rollout restart deployment/orchestrator-agent -n ad-campaign
```

### 回滚部署

```bash
# Kubernetes
kubectl rollout undo deployment/orchestrator-agent -n ad-campaign
```

### 灾难恢复

1. 恢复数据库备份
2. 恢复配置文件
3. 重新部署服务
4. 验证服务健康

---

## 常见问题

### Q: 服务无法启动？

A: 检查：
1. 端口是否被占用
2. 环境变量是否正确
3. 依赖服务是否运行
4. 查看日志文件

### Q: 服务间无法通信？

A: 检查：
1. 网络配置
2. 服务 URL 配置
3. 防火墙规则
4. DNS 解析

### Q: 性能问题？

A: 检查：
1. 资源限制
2. 数据库连接池
3. 缓存配置
4. 日志级别（降低日志量）

---

## 下一步

- [故障排查指南](./TROUBLESHOOTING.md)
- [API 文档](./API_DOCUMENTATION.md)
- [配置指南](./CONFIGURATION.md)

