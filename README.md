# Superisor Agent

基于 **LangChain + DeepSeek** 的多智能体编排框架，采用层级 Supervisor 模式，智能地将任务委派给专门的子智能体。

## 概述

Superisor Agent 实现了 **Supervisor + 子智能体** 架构：

- **Supervisor Agent** 作为中央调度器，分析用户意图并路由任务
- **专业子智能体** 处理特定领域操作（搜索、邮件等）
- 子智能体可通过 **MCP（Model Context Protocol）Server** 访问外部工具和数据源

Supervisor 根据上下文决定调用哪个子智能体 — 例如，查询天气来判断是否需要查询火车票，然后撰写并发送合适的邮件。

## 架构

```
┌────────────────────────────────────────────┐
│           Supervisor Agent                 │
│   (意图路由与任务编排)                      │
├────────────────┬───────────────────────────┤
│  Search Agent  │      Email Agent          │
│  (Bing / 12306 │  (QQ SMTP 邮件发送)       │
│   通过 MCP)    │                           │
└────────────────┴───────────────────────────┘
```

### 分层架构

| 层级 | 模块 | 职责 |
|------|------|------|
| **LLM** | `my_llm.py` | 大模型初始化（DeepSeek via LangChain） |
| **配置** | `config.py` | 基于环境变量的集中配置管理 |
| **工具** | `tools.py` | 原子化工具（SMTP 邮件发送等） |
| **Agent 工厂** | `agent_factory.py` | 创建子智能体和 Supervisor |
| **流式输出** | `stream_output.py` | 智能体输出的流式处理 |
| **入口** | `main.py` | 应用入口，异步编排 |

## 功能特性

- **多智能体编排** — Supervisor 根据意图将任务委派给子智能体
- **MCP 集成** — 连接外部 MCP Server 以获取搜索、数据检索等能力
- **异步流式输出** — 实时流式输出智能体的推理过程和结果
- **工具调用** — 可插拔的工具层（SMTP 邮件、网络搜索、12306 火车票查询）
- **环境变量配置** — 密钥通过 `.env` 管理，绝不硬编码

## 环境要求

- Python 3.10+
- [DeepSeek](https://platform.deepseek.com/) API 密钥
- （可选）用于 MCP Server 访问的 [ModelScope](https://www.modelscope.cn/) Token
- （可选）开启了 SMTP 服务的 QQ 邮箱（用于邮件发送）

## 快速开始

### 1. 克隆并安装依赖

```bash
git clone https://github.com/2577554682/superisor-agent.git
cd superisor-agent
pip install -r requirements.txt
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件：

```ini
# 必填
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# 可选 — 用于 MCP Server 访问
MODELSCOPE_TOKEN=your-modelscope-token

# 可选 — 用于邮件发送（QQ SMTP）
SMTP_USER=your-email@qq.com
SMTP_PASS=your-smtp-authorization-code
```

> **安全提醒：** `.env` 文件已在 `.gitignore` 中，**禁止提交到仓库**。

### 3. 运行

```bash
python main.py
```

示例程序将执行以下工作流：
1. 查询某城市的当天天气
2. 根据天气情况决定是否查询火车票
3. 发送合适的邮件通知

## 配置说明

| 变量 | 必填 | 说明 |
|----------|------|------|
| `DEEPSEEK_API_KEY` | 是 | DeepSeek 平台 API 密钥 |
| `DEEPSEEK_BASE_URL` | 是 | DeepSeek API 基础地址 |
| `MODELSCOPE_TOKEN` | 否 | 用于访问 ModelScope 托管的 MCP Server |
| `SMTP_USER` | 否 | QQ 邮箱地址（用于 SMTP） |
| `SMTP_PASS` | 否 | QQ 邮箱 SMTP 授权码 |

### 自定义 MCP Server

编辑 `config.py` 来添加或修改 MCP Server 配置：

```python
@classmethod
def get_mcp_config(cls) -> dict:
    return {
        "your-mcp-server": {
            "transport": "streamable_http",
            "url": "https://mcp.example.com/path",
            "headers": {"Authorization": f"Bearer {cls.YOUR_TOKEN}"},
        },
    }
```

## 项目结构

```
superisor_agent/
├── superisor_agent_demo/
│   ├── __init__.py
│   ├── config.py           # 配置管理
│   ├── tools.py            # 原子化工具（邮件等）
│   ├── agent_factory.py    # Agent 构建器（工厂模式）
│   ├── stream_output.py    # 流式输出处理
│   └── main.py             # 应用入口
├── env_utils.py            # 环境变量加载工具
├── my_llm.py               # 大模型初始化
├── .env                    # 本地密钥（已 gitignore）
├── .gitignore
└── README.md
```

## 扩展指南

### 添加新工具

1. 在 `tools.py` 中定义 `@tool` 函数
2. 在 `agent_factory.py` 中创建对应的子智能体
3. 在 Supervisor 中注册该智能体

### 添加 MCP Server

1. 在 `config.py` 的 `Config.get_mcp_config()` 中添加 Server 配置
2. `MultiServerMCPClient` 将自动加载其工具

## 许可证

MIT
