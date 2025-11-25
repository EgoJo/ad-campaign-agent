# 根目录文件整理建议

## 当前根目录文件分析

### 文档文件（8个）
- `README.md` - 主文档（应保留在根目录）
- `CONFIGURATION.md` - 配置文档
- `DEPLOYMENT_REPORT.md` - 部署报告
- `LLM_ORCHESTRATOR.md` - LLM Orchestrator 文档
- `MAKEFILE_USAGE.md` - Makefile 使用指南
- `OPTIMIZATIONS.md` - 优化总结
- `PROJECT_SUMMARY.md` - 项目总结
- `QUICKSTART.md` - 快速开始指南

### 配置文件（7个）
- `.env` / `.env.example` - 环境变量（应保留）
- `.gitignore` - Git 忽略文件（应保留）
- `docker-compose.yml` - Docker Compose 配置（应保留）
- `Dockerfile` - Docker 镜像配置（应保留）
- `pyproject.toml` - Poetry 配置（应保留）
- `requirements.txt` - Python 依赖（应保留）
- `Makefile` - 构建脚本（应保留）

### 脚本文件（5个）
- `start_services.sh` - 启动所有服务
- `stop_services.sh` - 停止所有服务
- `start_orchestrator.sh` - 启动 orchestrator
- `start_orchestrator_llm.sh` - 启动 LLM orchestrator
- `stop_orchestrator.sh` - 停止 orchestrator

## 整理建议

### 方案 1：创建 docs/ 目录（推荐）

```
ad-campaign-agent/
├── README.md                    # 保留在根目录（项目入口）
├── docs/                        # 新建：所有文档
│   ├── CONFIGURATION.md
│   ├── DEPLOYMENT_REPORT.md
│   ├── LLM_ORCHESTRATOR.md
│   ├── MAKEFILE_USAGE.md
│   ├── OPTIMIZATIONS.md
│   ├── PROJECT_SUMMARY.md
│   └── QUICKSTART.md
├── scripts/                     # 新建：所有脚本（作为 Makefile 的备选）
│   ├── start_services.sh
│   ├── stop_services.sh
│   ├── start_orchestrator.sh
│   ├── start_orchestrator_llm.sh
│   └── stop_orchestrator.sh
├── app/
├── tests/
├── examples/
├── logs/
├── Makefile                     # 保留在根目录
├── pyproject.toml              # 保留在根目录
├── requirements.txt            # 保留在根目录
├── docker-compose.yml          # 保留在根目录
├── Dockerfile                  # 保留在根目录
└── .env.example               # 保留在根目录
```

### 方案 2：更细化的组织（适合大型项目）

```
ad-campaign-agent/
├── README.md
├── docs/
│   ├── guides/                 # 使用指南
│   │   ├── QUICKSTART.md
│   │   ├── MAKEFILE_USAGE.md
│   │   └── CONFIGURATION.md
│   ├── architecture/           # 架构文档
│   │   ├── LLM_ORCHESTRATOR.md
│   │   └── OPTIMIZATIONS.md
│   └── reports/                # 报告文档
│       ├── DEPLOYMENT_REPORT.md
│       └── PROJECT_SUMMARY.md
├── scripts/
│   ├── services/               # 服务管理脚本
│   │   ├── start_services.sh
│   │   └── stop_services.sh
│   └── orchestrator/           # Orchestrator 脚本
│       ├── start_orchestrator.sh
│       ├── start_orchestrator_llm.sh
│       └── stop_orchestrator.sh
└── [其他文件保持不变]
```

## 推荐实施方案

**建议采用方案 1**，原因：
1. 简单清晰，易于维护
2. 文档集中管理，易于查找
3. 脚本保留作为 Makefile 的备选
4. 符合常见 Python 项目结构

## 实施步骤

1. 创建 `docs/` 目录
2. 移动所有文档文件（除 README.md）
3. 创建 `scripts/` 目录
4. 移动所有 .sh 脚本
5. 更新 Makefile 中的脚本路径引用
6. 更新 README.md 中的文档链接

## 文件分类总结

| 类别 | 文件数 | 建议位置 | 理由 |
|------|--------|----------|------|
| 文档 | 8 | `docs/` (7个) + 根目录(1个) | 集中管理，README 作为入口 |
| 脚本 | 5 | `scripts/` | 统一管理，作为 Makefile 备选 |
| 配置 | 7 | 根目录 | 标准位置，便于工具识别 |
| 代码 | - | `app/`, `tests/`, `examples/` | 已组织良好 |

## 预期效果

整理后根目录将只保留：
- **必需文件**：README.md, Makefile, pyproject.toml, requirements.txt
- **配置文件**：docker-compose.yml, Dockerfile, .env.example, .gitignore
- **目录**：app/, tests/, examples/, docs/, scripts/, logs/, venv/

**根目录文件数：从 ~20 个减少到 ~8 个**

