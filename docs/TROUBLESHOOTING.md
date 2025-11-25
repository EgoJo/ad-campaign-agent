# 故障排查指南

本文档提供 Ad Campaign Agent 系统的常见问题和解决方案。

## 目录

- [服务启动问题](#服务启动问题)
- [服务间通信问题](#服务间通信问题)
- [API 调用问题](#api-调用问题)
- [性能问题](#性能问题)
- [日志和调试](#日志和调试)
- [Docker 相关问题](#docker-相关问题)
- [环境配置问题](#环境配置问题)

---

## 服务启动问题

### 问题 1: 端口已被占用

**症状：**
```
Error: Address already in use
OSError: [Errno 48] Address already in use
```

**解决方案：**

1. **查找占用端口的进程：**
```bash
# macOS/Linux
lsof -i :8001
# 或
netstat -an | grep 8001

# 终止进程
kill -9 <PID>
```

2. **修改端口配置：**
```bash
# 在启动脚本中修改端口
# 或在 .env 文件中配置
PORT=8001
```

3. **使用 Docker：**
```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "18001:8001"  # 使用不同的主机端口
```

### 问题 2: 模块导入错误

**症状：**
```
ModuleNotFoundError: No module named 'app'
ImportError: cannot import name 'X' from 'Y'
```

**解决方案：**

1. **检查 Python 路径：**
```bash
# 确保在项目根目录
cd ad-campaign-agent

# 检查 PYTHONPATH
echo $PYTHONPATH
export PYTHONPATH=/path/to/ad-campaign-agent:$PYTHONPATH
```

2. **重新安装依赖：**
```bash
pip install -r requirements.txt
```

3. **检查虚拟环境：**
```bash
# 确保虚拟环境已激活
which python
# 应该指向 venv/bin/python
```

### 问题 3: 依赖服务未启动

**症状：**
```
Connection refused
Service unavailable
```

**解决方案：**

1. **检查服务状态：**
```bash
# 检查所有服务
make health-check

# 或手动检查
curl http://localhost:8001/health
curl http://localhost:8002/health
# ... 其他服务
```

2. **按顺序启动服务：**
```bash
# 先启动所有微服务
make start-services

# 等待服务就绪（约 10 秒）
sleep 10

# 再启动 orchestrator
make start-orchestrator
```

---

## 服务间通信问题

### 问题 1: 服务无法连接到其他服务

**症状：**
```
ConnectionError: Failed to connect to http://localhost:8001
httpx.ConnectError: [Errno 61] Connection refused
```

**解决方案：**

1. **检查服务 URL 配置：**
```bash
# 在 Docker 环境中，使用服务名
PRODUCT_SERVICE_URL=http://product_service:8001

# 在本地开发中，使用 localhost
PRODUCT_SERVICE_URL=http://localhost:8001
```

2. **验证网络连接：**
```bash
# 从 orchestrator 容器测试连接
docker exec -it orchestrator_agent curl http://product_service:8001/health
```

3. **检查防火墙：**
```bash
# 确保端口未被防火墙阻止
sudo ufw status
# 或
sudo iptables -L
```

### 问题 2: 服务响应超时

**症状：**
```
TimeoutError: Request timed out
httpx.ReadTimeout: Read timeout
```

**解决方案：**

1. **增加超时时间：**
```python
# 在 http_client.py 中
client = httpx.AsyncClient(timeout=30.0)  # 增加到 30 秒
```

2. **检查服务性能：**
```bash
# 查看服务日志
tail -f logs/product_service.log

# 检查资源使用
docker stats
# 或
kubectl top pods
```

3. **优化服务性能：**
- 增加服务资源限制
- 优化数据库查询
- 添加缓存

---

## API 调用问题

### 问题 1: 验证错误

**症状：**
```json
{
  "status": "error",
  "error_code": "VALIDATION_ERROR",
  "message": "Request validation failed"
}
```

**解决方案：**

1. **检查请求格式：**
```bash
# 查看 API 文档
curl http://localhost:8001/docs

# 验证请求体格式
# 确保所有必需字段都存在
# 确保字段类型正确
```

2. **使用正确的 Content-Type：**
```bash
curl -X POST http://localhost:8001/select_products \
  -H "Content-Type: application/json" \
  -d '{"campaign_objective": "sales", ...}'
```

### 问题 2: 404 Not Found

**症状：**
```
404 Not Found
```

**解决方案：**

1. **检查端点路径：**
```bash
# 查看服务文档
curl http://localhost:8001/docs

# 确保使用正确的 HTTP 方法
# GET vs POST
```

2. **检查服务版本：**
```bash
# 某些端点可能在不同版本中
# 检查 API 版本
```

### 问题 3: 500 Internal Server Error

**症状：**
```
500 Internal Server Error
```

**解决方案：**

1. **查看服务日志：**
```bash
# 本地开发
tail -f logs/product_service.log

# Docker
docker-compose logs -f product_service

# Kubernetes
kubectl logs -f deployment/product-service
```

2. **检查环境变量：**
```bash
# 确保所有必需的环境变量已设置
env | grep GEMINI_API_KEY
```

3. **检查依赖服务：**
```bash
# 确保依赖服务正常运行
curl http://localhost:8000/services/status
```

---

## 性能问题

### 问题 1: 响应时间慢

**症状：**
- API 响应时间 > 5 秒
- 服务超时

**解决方案：**

1. **检查资源使用：**
```bash
# Docker
docker stats

# Kubernetes
kubectl top pods
```

2. **优化数据库查询：**
- 添加索引
- 使用连接池
- 优化查询语句

3. **添加缓存：**
```python
# 使用 Redis 缓存
import redis
cache = redis.Redis(host='localhost', port=6379)
```

4. **增加服务资源：**
```yaml
# docker-compose.yml
resources:
  limits:
    cpus: '2'
    memory: 2G
```

### 问题 2: 内存泄漏

**症状：**
- 内存使用持续增长
- 服务崩溃

**解决方案：**

1. **检查日志：**
```bash
# 查找内存相关错误
grep -i "memory" logs/*.log
```

2. **使用内存分析工具：**
```python
# 使用 memory_profiler
pip install memory-profiler
python -m memory_profiler app/services/product_service/main.py
```

3. **设置内存限制：**
```yaml
# docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G
```

---

## 日志和调试

### 问题 1: 日志不显示

**症状：**
- 日志文件为空
- 控制台无输出

**解决方案：**

1. **检查日志级别：**
```bash
# 设置环境变量
export LOG_LEVEL=DEBUG

# 或在 .env 文件中
LOG_LEVEL=DEBUG
```

2. **检查日志配置：**
```python
# 在 main.py 中
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. **检查日志文件权限：**
```bash
# 确保有写入权限
chmod 755 logs/
touch logs/product_service.log
```

### 问题 2: 日志过多

**症状：**
- 日志文件过大
- 磁盘空间不足

**解决方案：**

1. **调整日志级别：**
```bash
# 生产环境使用 INFO 或 WARNING
LOG_LEVEL=INFO
```

2. **配置日志轮转：**
```python
# 使用 logging.handlers.RotatingFileHandler
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/product_service.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

3. **清理旧日志：**
```bash
# 删除 7 天前的日志
find logs/ -name "*.log" -mtime +7 -delete
```

---

## Docker 相关问题

### 问题 1: 容器无法启动

**症状：**
```
Error: Container failed to start
Exit code: 1
```

**解决方案：**

1. **查看容器日志：**
```bash
docker-compose logs orchestrator_agent
```

2. **检查镜像：**
```bash
# 重新构建镜像
docker-compose build --no-cache

# 检查镜像
docker images | grep ad-campaign
```

3. **检查配置：**
```bash
# 验证 docker-compose.yml
docker-compose config
```

### 问题 2: 容器间无法通信

**症状：**
```
Connection refused between containers
```

**解决方案：**

1. **检查网络：**
```bash
# 查看网络
docker network ls
docker network inspect ad-campaign-agent_ad_campaign_network
```

2. **使用服务名：**
```bash
# 在 docker-compose.yml 中
# 使用服务名而不是 localhost
PRODUCT_SERVICE_URL=http://product_service:8001
```

3. **检查 depends_on：**
```yaml
# 确保依赖关系正确
depends_on:
  product_service:
    condition: service_healthy
```

### 问题 3: 健康检查失败

**症状：**
```
Health check failed
Container unhealthy
```

**解决方案：**

1. **检查健康检查端点：**
```bash
# 手动测试
docker exec -it product_service curl http://localhost:8001/health
```

2. **调整健康检查配置：**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
  interval: 10s
  timeout: 5s
  retries: 5  # 增加重试次数
  start_period: 30s  # 增加启动等待时间
```

---

## 环境配置问题

### 问题 1: 环境变量未生效

**症状：**
- 配置未应用
- 使用默认值

**解决方案：**

1. **检查 .env 文件：**
```bash
# 确保 .env 文件存在
ls -la .env

# 检查格式
cat .env
# 确保没有空格和引号
GEMINI_API_KEY=your_key_here
```

2. **重新加载环境变量：**
```bash
# Docker Compose
docker-compose down
docker-compose up -d

# 本地开发
# 重启服务
```

3. **验证环境变量：**
```bash
# 在容器中检查
docker exec -it orchestrator_agent env | grep GEMINI
```

### 问题 2: API Key 无效

**症状：**
```
Authentication failed
Invalid API key
```

**解决方案：**

1. **验证 API Key：**
```bash
# 检查 API Key 格式
echo $GEMINI_API_KEY

# 测试 API Key
curl https://generativelanguage.googleapis.com/v1/models?key=$GEMINI_API_KEY
```

2. **检查 API Key 权限：**
- 确保 API Key 有正确的权限
- 检查 API 配额

3. **重新生成 API Key：**
- 在 Google Cloud Console 中重新生成
- 更新 .env 文件

---

## 调试技巧

### 1. 启用详细日志

```bash
# 设置环境变量
export LOG_LEVEL=DEBUG

# 或在代码中
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. 使用交互式调试

```python
# 在代码中添加断点
import pdb; pdb.set_trace()

# 或使用 IPython
from IPython import embed; embed()
```

### 3. 测试单个服务

```bash
# 直接运行服务
python -m app.services.product_service.main

# 使用 curl 测试
curl -X POST http://localhost:8001/select_products \
  -H "Content-Type: application/json" \
  -d '{"campaign_objective": "sales", "target_audience": "test", "budget": 1000}'
```

### 4. 使用 Postman/Insomnia

- 导入 OpenAPI 规范
- 测试各个端点
- 查看请求/响应详情

---

## 获取帮助

如果问题仍未解决：

1. **查看日志：**
   - 服务日志：`logs/*.log`
   - Docker 日志：`docker-compose logs`
   - Kubernetes 日志：`kubectl logs`

2. **检查文档：**
   - [API 文档](./API_DOCUMENTATION.md)
   - [部署指南](./DEPLOYMENT_GUIDE.md)
   - [配置指南](./CONFIGURATION.md)

3. **提交 Issue：**
   - 包含错误日志
   - 包含环境信息
   - 包含复现步骤

---

## 常见错误代码

| 错误代码 | 说明 | 解决方案 |
|---------|------|---------|
| `VALIDATION_ERROR` | 请求验证失败 | 检查请求格式 |
| `NOT_FOUND` | 资源未找到 | 检查资源 ID |
| `INTERNAL_ERROR` | 服务器错误 | 查看服务日志 |
| `SERVICE_UNAVAILABLE` | 服务不可用 | 检查依赖服务 |
| `AUTHENTICATION_ERROR` | 认证失败 | 检查 API Key |
| `AUTHORIZATION_ERROR` | 授权失败 | 检查权限配置 |

---

## 预防措施

1. **监控服务健康：**
   - 定期检查 `/health` 端点
   - 设置告警

2. **日志管理：**
   - 配置日志轮转
   - 定期清理旧日志

3. **资源监控：**
   - 监控 CPU/内存使用
   - 设置资源限制

4. **备份配置：**
   - 定期备份配置文件
   - 版本控制配置

