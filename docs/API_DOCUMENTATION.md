# API 文档

本文档详细描述了 Ad Campaign Agent 系统的所有 API 端点。

## 目录

- [Orchestrator Agent API](#orchestrator-agent-api)
- [Product Service API](#product-service-api)
- [Creative Service API](#creative-service-api)
- [Strategy Service API](#strategy-service-api)
- [Meta Service API](#meta-service-api)
- [Logs Service API](#logs-service-api)
- [Optimizer Service API](#optimizer-service-api)
- [通用响应格式](#通用响应格式)
- [错误处理](#错误处理)

---

## Orchestrator Agent API

**Base URL:** `http://localhost:8000`  
**API Docs:** http://localhost:8000/docs

### GET /

根路径，返回服务信息。

**响应示例：**
```json
{
  "service": "Ad Campaign Orchestrator Agent (LLM-Enhanced)",
  "version": "2.0.0",
  "status": "running",
  "description": "AI-powered orchestrator with natural language understanding",
  "capabilities": [
    "Natural language intent parsing",
    "Fixed pipeline execution",
    "Intelligent error handling",
    "Human-readable summaries"
  ],
  "endpoints": {
    "health": "/health",
    "create_campaign_nl": "/create_campaign_nl (Natural Language)",
    "create_campaign": "/create_campaign (Structured)",
    "services_status": "/services/status",
    "docs": "/docs"
  }
}
```

### GET /health

健康检查端点。

**响应：**
```json
{
  "status": "healthy",
  "service": "orchestrator_agent"
}
```

### POST /create_campaign_nl

使用自然语言创建广告活动。

**请求体：**
```json
{
  "user_request": "Create a sales campaign for electronics with $5000 budget targeting tech enthusiasts"
}
```

**响应：**
```json
{
  "status": "success",
  "campaigns": [
    {
      "platform": "meta",
      "campaign_id": "camp_abc123",
      "products": [...],
      "creatives": [...],
      "strategy": {...},
      "summary": "Created campaign with 5 products and 6 creative variants"
    }
  ],
  "errors": [],
  "summary": "Successfully created a sales-focused ad campaign..."
}
```

### POST /create_campaign

使用结构化输入创建广告活动。

**请求体：**
```json
{
  "user_query": "Create a campaign for electronics",
  "platform": "meta",
  "budget": 5000.0,
  "objective": "conversions",
  "category": "electronics",
  "time_range": {
    "start": "2025-01-01",
    "end": "2025-01-31"
  }
}
```

**响应：** 同 `/create_campaign_nl`

### GET /services/status

检查所有微服务的状态。

**响应：**
```json
{
  "orchestrator": {
    "status": "healthy",
    "service": "orchestrator_agent"
  },
  "product_service": {
    "status": "healthy",
    "url": "http://localhost:8001"
  },
  "creative_service": {
    "status": "healthy",
    "url": "http://localhost:8002"
  },
  ...
}
```

---

## Product Service API

**Base URL:** `http://localhost:8001`  
**API Docs:** http://localhost:8001/docs

### GET /health

健康检查。

**响应：**
```json
{
  "status": "healthy",
  "service": "product_service"
}
```

### POST /select_products

选择产品用于广告活动。

**请求体：**
```json
{
  "campaign_objective": "sales",
  "target_audience": "tech enthusiasts aged 25-45",
  "budget": 10000.0,
  "max_products": 10
}
```

**响应：**
```json
{
  "product_groups": [
    {
      "priority": "high",
      "products": [
        {
          "product_id": "PROD-001",
          "name": "Wireless Headphones",
          "description": "Premium noise-canceling headphones",
          "price": 199.99,
          "category": "Electronics",
          "image_url": "https://example.com/image.jpg",
          "stock_quantity": 100
        }
      ]
    }
  ],
  "total_products": 5
}
```

---

## Creative Service API

**Base URL:** `http://localhost:8002`  
**API Docs:** http://localhost:8002/docs

### GET /health

健康检查。

### POST /generate_creatives

生成广告创意内容。

**请求体：**
```json
{
  "campaign_spec": {
    "user_query": "Create a campaign for electronics",
    "platform": "meta",
    "budget": 5000.0,
    "objective": "conversions",
    "category": "electronics"
  },
  "products": [
    {
      "product_id": "PROD-001",
      "title": "Wireless Headphones",
      "description": "Premium headphones",
      "price": 199.99,
      "category": "electronics",
      "image_url": "https://example.com/image.jpg"
    }
  ]
}
```

**响应：**
```json
{
  "status": "success",
  "creatives": [
    {
      "creative_id": "creative_123",
      "product_id": "PROD-001",
      "platform": "meta",
      "variant_id": "A",
      "primary_text": "Experience premium sound quality...",
      "headline": "Amazing Headphones",
      "image_url": "https://example.com/generated-image.jpg",
      "style_profile": {...},
      "ab_group": "control"
    }
  ],
  "debug": {
    "copy_prompts": [...],
    "image_prompts": [...],
    "raw_llm_responses": [...],
    "qa_results": [...]
  }
}
```

---

## Strategy Service API

**Base URL:** `http://localhost:8003`  
**API Docs:** http://localhost:8003/docs

### GET /health

健康检查。

### POST /generate_strategy

生成活动策略。

**请求体：**
```json
{
  "campaign_objective": "sales",
  "total_budget": 10000.0,
  "duration_days": 30,
  "target_audience": "tech enthusiasts",
  "platforms": ["facebook", "instagram"]
}
```

**响应：**
```json
{
  "abstract_strategy": "Multi-platform campaign targeting tech-savvy consumers...",
  "platform_strategies": [
    {
      "platform": "facebook",
      "budget_allocation": 50.0,
      "bid_strategy": "lowest_cost",
      "daily_budget": 166.67,
      "targeting_criteria": {...}
    }
  ],
  "estimated_reach": 500000,
  "estimated_conversions": 2500
}
```

---

## Meta Service API

**Base URL:** `http://localhost:8004`  
**API Docs:** http://localhost:8004/docs

### GET /health

健康检查。

### POST /create_campaign

在 Meta 平台创建广告活动。

**请求体：**
```json
{
  "campaign_name": "Electronics Campaign",
  "objective": "conversions",
  "daily_budget": 100.0,
  "targeting": {
    "age_min": 25,
    "age_max": 45,
    "genders": [1, 2],
    "locations": ["US"]
  },
  "creatives": [
    {
      "creative_id": "creative_123",
      "headline": "Amazing Headphones",
      "body_text": "Experience premium sound...",
      "call_to_action": "Shop Now",
      "image_url": "https://example.com/image.jpg"
    }
  ],
  "start_date": "2025-01-01"
}
```

**响应：**
```json
{
  "campaign_id": "CAMP-123456",
  "ad_set_id": "ADSET-123456",
  "ad_ids": [
    {
      "ad_id": "AD-123456",
      "creative_id": "creative_123",
      "status": "PENDING_REVIEW"
    }
  ],
  "status": "ACTIVE"
}
```

---

## Logs Service API

**Base URL:** `http://localhost:8005`  
**API Docs:** http://localhost:8005/docs

### GET /health

健康检查。

### POST /append_event

记录事件。

**请求体：**
```json
{
  "event_type": "campaign_created",
  "message": "Campaign created successfully",
  "campaign_id": "CAMP-123456",
  "metadata": {
    "user_id": "user_123",
    "platform": "meta"
  }
}
```

**响应：**
```json
{
  "status": "ok",
  "event_id": "EVENT-ABC123DEF456"
}
```

**事件类型：**
- `campaign_created`
- `campaign_updated`
- `ad_created`
- `product_selected`
- `creative_generated`
- `strategy_generated`
- `error`
- `warning`
- `info`

---

## Optimizer Service API

**Base URL:** `http://localhost:8007`  
**API Docs:** http://localhost:8007/docs

### GET /health

健康检查。

### POST /summarize_recent_runs

获取活动优化建议。

**请求体：**
```json
{
  "campaign_ids": ["CAMP-001", "CAMP-002"],
  "days": 7
}
```

**响应：**
```json
{
  "summary": "Recent campaigns show strong performance...",
  "total_campaigns": 15,
  "total_spend": 50000.0,
  "total_conversions": 2000,
  "average_cpa": 12.5,
  "suggestions": [
    {
      "category": "budget",
      "suggestion": "Increase budget for high-performing ad sets by 20%",
      "expected_impact": "Estimated 15% increase in conversions",
      "priority": "high"
    }
  ]
}
```

---

## 通用响应格式

### 成功响应

所有成功响应都包含 `status: "success"` 或 `status: "ok"`。

### 错误响应

所有错误响应遵循统一格式：

```json
{
  "status": "error",
  "error_code": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {
    "field": "additional context",
    "request_id": "request-id-for-tracking"
  }
}
```

**常见错误代码：**
- `VALIDATION_ERROR` - 请求验证失败
- `NOT_FOUND` - 资源未找到
- `INTERNAL_ERROR` - 服务器内部错误
- `SERVICE_UNAVAILABLE` - 依赖服务不可用
- `AUTHENTICATION_ERROR` - 认证失败
- `AUTHORIZATION_ERROR` - 授权失败

---

## 错误处理

### HTTP 状态码

- `200 OK` - 请求成功
- `400 Bad Request` - 请求格式错误
- `401 Unauthorized` - 未认证
- `403 Forbidden` - 无权限
- `404 Not Found` - 资源不存在
- `422 Unprocessable Entity` - 验证错误
- `500 Internal Server Error` - 服务器错误
- `502 Bad Gateway` - 依赖服务错误
- `503 Service Unavailable` - 服务不可用

### 请求追踪

所有响应包含 `X-Request-ID` 头，用于请求追踪。

### 重试策略

对于临时性错误（5xx），建议使用指数退避重试：
- 第1次重试：1秒后
- 第2次重试：2秒后
- 第3次重试：4秒后

---

## 认证和授权

当前版本未实现认证。生产环境应添加：
- API Key 认证
- OAuth 2.0
- JWT Token

---

## 速率限制

当前版本未实现速率限制。生产环境建议：
- 每个 API Key：100 请求/分钟
- 每个 IP：1000 请求/小时

---

## 版本控制

当前 API 版本：`v1`

未来版本将通过 URL 路径控制：
- `/v1/...` - 当前版本
- `/v2/...` - 未来版本

---

## 交互式文档

所有服务都提供 Swagger/OpenAPI 交互式文档：

- Orchestrator: http://localhost:8000/docs
- Product Service: http://localhost:8001/docs
- Creative Service: http://localhost:8002/docs
- Strategy Service: http://localhost:8003/docs
- Meta Service: http://localhost:8004/docs
- Logs Service: http://localhost:8005/docs
- Optimizer Service: http://localhost:8007/docs

在文档页面可以：
- 查看所有端点
- 查看请求/响应格式
- 直接测试 API
- 下载 OpenAPI 规范

