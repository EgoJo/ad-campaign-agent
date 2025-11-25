# 文件组织说明

## 📁 目录结构

```
ad-campaign-agent/
├── 📄 README.md              # 项目主文档
├── 📄 Makefile               # 统一命令管理
├── 📄 pyproject.toml         # Poetry 配置
├── 📄 requirements.txt       # Python 依赖
├── 📄 docker-compose.yml     # Docker 配置
├── 📄 Dockerfile             # 容器定义
├── 📄 .env.example           # 环境变量模板
│
├── 📂 app/                   # 应用代码
│   ├── orchestrator/         # Orchestrator 服务
│   ├── services/             # 微服务
│   └── common/               # 共享模块
│
├── 📂 docs/                  # 📚 文档目录
│   ├── CONFIGURATION.md
│   ├── DEPLOYMENT_REPORT.md
│   ├── LLM_ORCHESTRATOR.md
│   ├── MAKEFILE_USAGE.md
│   ├── OPTIMIZATIONS.md
│   ├── PROJECT_SUMMARY.md
│   ├── QUICKSTART.md
│   └── REORGANIZATION_PLAN.md
│
├── 📂 scripts/               # 🔧 脚本目录
│   ├── start_services.sh
│   ├── stop_services.sh
│   ├── start_orchestrator.sh
│   ├── start_orchestrator_llm.sh
│   └── stop_orchestrator.sh
│
├── 📂 tests/                 # 测试代码
├── 📂 examples/              # 示例代码
└── 📂 logs/                  # 日志文件
```

## 📊 整理效果

- **整理前**: ~20 个文件在根目录
- **整理后**: ~8 个核心文件在根目录
- **减少**: ~60% 的文件数量

## 🎯 文件分类

| 类别 | 位置 | 文件数 |
|------|------|--------|
| 核心配置 | 根目录 | 7 |
| 文档 | `docs/` | 8 |
| 脚本 | `scripts/` | 5 |
| 代码 | `app/` | - |
| 测试 | `tests/` | - |

## 💡 使用建议

1. **查看文档**: `cat docs/QUICKSTART.md`
2. **运行命令**: `make help` 查看所有命令
3. **启动服务**: `make start-services`
4. **查看日志**: `make logs-creative`

