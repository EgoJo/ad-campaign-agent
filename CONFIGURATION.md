# 配置说明 (Configuration Guide)

## 概述

系统支持两种部署模式：
- **本地开发环境**: 使用 localhost 默认配置
- **线上生产环境**: 通过环境变量配置生产服务 URL

## 配置方式

### 本地开发环境

本地开发时，**无需任何配置**，系统会自动使用 localhost 默认值：

```python
# 默认配置（app/common/config.py）
PRODUCT_SERVICE_URL: str = "http://localhost:8001"
CREATIVE_SERVICE_URL: str = "http://localhost:8002"
STRATEGY_SERVICE_URL: str = "http://localhost:8003"
META_SERVICE_URL: str = "http://localhost:8004"
LOGS_SERVICE_URL: str = "http://localhost:8005"
SCHEMA_VALIDATOR_SERVICE_URL: str = "http://localhost:8006"
OPTIMIZER_SERVICE_URL: str = "http://localhost:8007"
```

### 线上生产环境

线上部署时，通过环境变量覆盖默认配置：

#### 方式 1: 使用 .env 文件

创建 `.env` 文件：

```bash
# .env
ENVIRONMENT=production

# 服务 URL 配置
PRODUCT_SERVICE_URL=https://product-service.yourdomain.com
CREATIVE_SERVICE_URL=https://creative-service.yourdomain.com
STRATEGY_SERVICE_URL=https://strategy-service.yourdomain.com
META_SERVICE_URL=https://meta-service.yourdomain.com
LOGS_SERVICE_URL=https://logs-service.yourdomain.com
SCHEMA_VALIDATOR_SERVICE_URL=https://validator-service.yourdomain.com
OPTIMIZER_SERVICE_URL=https://optimizer-service.yourdomain.com

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
```

#### 方式 2: 使用系统环境变量

在启动脚本或 Docker 配置中设置：

```bash
export PRODUCT_SERVICE_URL=https://product-service.yourdomain.com
export CREATIVE_SERVICE_URL=https://creative-service.yourdomain.com
# ... 其他服务 URL
```

#### 方式 3: Docker Compose

在 `docker-compose.yml` 中配置：

```yaml
services:
  orchestrator:
    environment:
      - PRODUCT_SERVICE_URL=https://product-service.yourdomain.com
      - CREATIVE_SERVICE_URL=https://creative-service.yourdomain.com
      # ... 其他服务 URL
```

## 配置优先级

环境变量的优先级顺序：

1. **系统环境变量** (最高优先级)
2. **.env 文件中的变量**
3. **默认值** (localhost，用于本地开发)

## 验证配置

### 检查当前配置

```python
from app.common.config import settings

print(f"Product Service URL: {settings.PRODUCT_SERVICE_URL}")
print(f"Environment: {settings.ENVIRONMENT}")
```

### 测试环境变量覆盖

```bash
# 测试环境变量是否生效
PRODUCT_SERVICE_URL=https://test.example.com python3 -c \
  "from app.common.config import settings; print(settings.PRODUCT_SERVICE_URL)"
```

## 配置项说明

### 服务 URL 配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `PRODUCT_SERVICE_URL` | `http://localhost:8001` | 产品服务地址 |
| `CREATIVE_SERVICE_URL` | `http://localhost:8002` | 创意服务地址 |
| `STRATEGY_SERVICE_URL` | `http://localhost:8003` | 策略服务地址 |
| `META_SERVICE_URL` | `http://localhost:8004` | Meta 服务地址 |
| `LOGS_SERVICE_URL` | `http://localhost:8005` | 日志服务地址 |
| `SCHEMA_VALIDATOR_SERVICE_URL` | `http://localhost:8006` | 验证服务地址 |
| `OPTIMIZER_SERVICE_URL` | `http://localhost:8007` | 优化服务地址 |

### 其他配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `ENVIRONMENT` | `development` | 环境标识 (development/production) |
| `GEMINI_API_KEY` | `None` | Google Gemini API 密钥 |
| `GEMINI_MODEL` | `gemini-2.0-flash-exp` | Gemini 模型名称 |
| `LOG_LEVEL` | `INFO` | 日志级别 |

## 使用示例

### 本地开发

```bash
# 直接启动，使用默认 localhost 配置
./start_services.sh
./start_orchestrator.sh
```

### 线上部署

```bash
# 方式 1: 使用 .env 文件
cp .env.example .env
# 编辑 .env 文件，设置生产环境 URL
./start_services.sh
./start_orchestrator.sh

# 方式 2: 使用环境变量
export PRODUCT_SERVICE_URL=https://prod.example.com:8001
export CREATIVE_SERVICE_URL=https://prod.example.com:8002
# ... 设置其他服务 URL
./start_orchestrator.sh
```

### Docker 部署

```yaml
# docker-compose.yml
version: '3.8'
services:
  orchestrator:
    build: .
    environment:
      - ENVIRONMENT=production
      - PRODUCT_SERVICE_URL=https://product-service.example.com
      - CREATIVE_SERVICE_URL=https://creative-service.example.com
      # ... 其他配置
```

## 注意事项

1. **本地开发**: 不需要设置任何环境变量，直接使用默认 localhost 配置
2. **线上部署**: 必须设置所有服务 URL 环境变量
3. **环境变量优先级**: 系统环境变量 > .env 文件 > 默认值
4. **URL 格式**: 确保使用完整的 URL（包含协议 http:// 或 https://）
5. **安全性**: 生产环境中不要将 `.env` 文件提交到版本控制系统

## 故障排查

### 问题：服务无法连接到其他服务

**检查步骤**:
1. 确认环境变量是否正确设置
2. 检查服务 URL 是否可访问
3. 查看日志文件 `logs/orchestrator.log`

**示例**:
```bash
# 检查配置
python3 -c "from app.common.config import settings; print(settings.PRODUCT_SERVICE_URL)"

# 测试服务连接
curl http://localhost:8001/health
```

### 问题：环境变量未生效

**解决方案**:
1. 确认环境变量名称正确（大小写不敏感）
2. 检查 `.env` 文件格式是否正确
3. 重启服务以使配置生效

