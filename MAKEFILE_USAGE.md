# Makefile 使用指南

本项目使用 Makefile 统一管理所有命令，替代分散的 shell 脚本。

## 快速开始

```bash
# 查看所有可用命令
make help

# 完整设置（创建虚拟环境 + 安装依赖）
make setup

# 启动所有服务
make start-services

# 启动 orchestrator
make start-orchestrator
```

## 常用命令

### 开发环境设置

```bash
make venv              # 创建虚拟环境
make install           # 安装依赖
make install-dev       # 安装开发依赖
make setup             # 完整设置（venv + install）
```

### 测试和代码质量

```bash
make test              # 运行所有测试
make test-coverage     # 运行测试并生成覆盖率报告
make lint              # 运行 linter (flake8, mypy)
make format            # 格式化代码 (black)
make format-check      # 检查代码格式（不修改）
```

### 服务管理

```bash
make start-services    # 启动所有微服务
make stop-services     # 停止所有微服务
make start-orchestrator # 启动 orchestrator
make stop-orchestrator  # 停止 orchestrator
make restart-all       # 重启所有服务
make health-check      # 检查所有服务健康状态
```

### 日志查看

```bash
make logs              # 查看所有服务日志
make logs-creative     # 查看 creative service 日志
make logs-orchestrator # 查看 orchestrator 日志
```

### 清理

```bash
make clean             # 清理缓存和临时文件
```

## Poetry 使用（可选）

项目同时支持 Poetry 进行依赖管理：

```bash
# 安装 Poetry (如果还没有)
curl -sSL https://install.python-poetry.org | python3 -

# 使用 Poetry 安装依赖
poetry install

# 使用 Poetry 运行命令
poetry run pytest tests/
poetry run python -m app.services.creative_service.main
```

Poetry 的优势：
- 锁定依赖版本（poetry.lock）
- 更好的依赖解析
- 虚拟环境自动管理
- 支持依赖组（dev, test 等）

## 迁移说明

原有的 shell 脚本仍然可用，但建议使用 Makefile：

| 旧命令 | 新命令 |
|--------|--------|
| `./start_services.sh` | `make start-services` |
| `./stop_services.sh` | `make stop-services` |
| `./start_orchestrator_llm.sh` | `make start-orchestrator` |
| `./stop_orchestrator.sh` | `make stop-orchestrator` |

