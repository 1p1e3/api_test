# 🚀 API Test 自动化框架

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/1p1e3/api_test/actions)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-yellowgreen.svg)](#)



这是一个基于 Python 的接口自动化测试项目，包含用例管理、HTTP 客户端封装、数据库客户端和测试报告输出等常用功能。

## 主要特性 ✨

 - 测试执行与报告 🧾
	- 基于 `pytest` 的测试执行，易于使用 fixture、标记、参数化和并行化（可在 CI 中无缝集成）。
	- 支持 `pytest-html` 生成结构化 HTML 报告，测试输出保存在 `reports/` 目录，便于归档与审查。

 - 数据驱动与用例管理 🗂️
	- 支持 JSON 与 YAML 格式的测试数据（存放在 `cases/`），通过简单的映射机制把数据注入测试用例，实现同一接口多场景覆盖。
	- 提供 `core/ddt.py`（简单数据驱动实现）用于将数据文件与测试函数绑定，减少样板代码。

 - HTTP 客户端封装 (`core/api_client.py`) 🔌
	- 集中管理 `base_url`、请求头、会话（cookies/session）和鉴权逻辑，测试用例只需描述接口和断言。
	- 内建超时、重试与错误日志策略，统一处理异常与重试逻辑，减少测试不稳定性。
	- 支持请求/响应的统一日志格式，便于在 `logs/` 中定位问题。

 - 数据库支持 (`core/mysql_client.py`) 🗄️
	- 基于 `pymysql`/`sqlalchemy` 的数据库访问封装，支持连接配置、事务控制和常用查询/执行方法。
	- 为测试前置（test setup）与后置清理提供方便的接口，支持测试数据注入与回滚策略。

 - 模型与数据校验 ✅
	- 使用 Pydantic（`pydantic-settings`）或自定义数据模型在 `response_models/` 中定义响应模型，便于对接口返回进行结构化校验与类型转换。

 - 断言与工具函数（`utils/`） 🧰
	- `utils/assertions.py` 提供一致的断言方法（状态码、字段存在性、精确/模糊匹配、正则等），降低测试维护成本。
	- `utils/data_loader.py` 与 `utils/notifier.py` 分别处理测试数据加载与结果通知（邮件/钉钉/Webhook 可拓展）。

 - Mock 与隔离测试 🧪
	- 集成 `responses` 库以便在单元/集成测试中替代外部 HTTP 调用，实现快速、稳定的离线测试。

 - 可配置与环境隔离 🌐
	- 将环境相关配置（如 base URL、数据库连接）放在 `config/settings.py`，支持 `.env` 与环境变量优先级，方便在不同测试环境间切换。

 - 可扩展性与 CI 友好 🔁
	- 设计为模块化结构，便于用例库、客户端或报告插件的扩展。
	- 与主流 CI 系统兼容：在 CI 中可自动执行测试并保存 `reports/` 与 `logs/` 作为构建产物。

 - 可观测性 👀
	- 运行时日志写入到 `logs/`，报告与日志结合便于快速定位失败原因。

 - 安全与敏感信息管理 🔒
	- 不把密钥或密码写入仓库，建议使用 `.env` 或 CI 的秘密存储来注入敏感配置。

 - 示例与模板 📚
	- 项目包含示例测试文件与数据（`tests/`、`cases/`），作为编写新用例的模板，降低新成员上手成本。


## 📁 项目结构概览

- [conftest.py](conftest.py)：pytest 全局配置和固件。
- [main.py](main.py)：项目入口（可用于快速手动触发或集成调试）。
- [pyproject.toml](pyproject.toml)：项目元数据与依赖声明。
- [cases/](cases/)：测试数据目录，包含 `test_login.json`、`test_user.yaml` 等。
- [config/paths.py](config/paths.py)、[config/settings.py](config/settings.py)：配置及路径管理。
- [core/api_client.py](core/api_client.py)：HTTP 客户端封装。
- [core/mysql_client.py](core/mysql_client.py)：MySQL 数据库操作封装。
- [core/ddt.py](core/ddt.py)：数据驱动测试（简单实现）。
- [models/](models/)、[response_models/](response_models/)：请求/响应模型定义与验证。
- [tests/](tests/)：测试用例目录（示例：`tests/test_user_api.py`）。
- [reports/](reports/)：测试报告输出目录。
- [logs/](logs/)：运行日志文件。
- [utils/](utils/)：断言、加载数据、通知和日志封装等工具函数。

## 🛠️ 环境准备
Python: 3.13 或更高版本

uv: 推荐使用 uv 管理项目。

安装命令：
- Windows

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1" 
```
- macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```


## 🚀 快速开始

1. 克隆仓库并进入项目目录：

```bash
git clone <repo-url>
cd api_test
```

2. 建议创建并激活虚拟环境：

使用 uv 一键安装所有依赖并创建虚拟环境：

```bash
# 同步环境并安装依赖
uv sync
```

3. 配置环境

在 `.env` 中配置所需要的环境变量。


## 🧪 运行测试

使用 uv run 可以确保命令在项目虚拟环境中正确执行：

- 运行所有用例：
```bash
uv run pytest
```

- 运行并生成 HTML 报告：
```bash
uv run pytest --html=reports/report.html --self-contained-html
```

- 执行特定模块：
```bash
uv run pytest tests/test_user_api.py -v
```

- 多线程并行执行（需安装 pytest-xdist）：
```bash
uv run pytest -n auto
```


## 🛠️ 开发指南

### 添加新依赖

如果你需要引入新的库，请使用 uv add：
```bash
# 添加运行时依赖
uv add httpx

# 添加开发依赖
uv add --dev faker
```

### 编写新用例

1. 在 cases/ 中准备测试数据。

2. 在 tests/ 中编写以 test_ 开头的函数。

3. 调用 core/api_client.py 发起请求，使用 utils/assertions.py 进行断言。


## 🔒 安全说明

- 敏感信息（密码、密钥）请务必存放在 .env 文件或 CI/CD 的 Secret 变量中。
- **严禁** 将包含真实凭据的 .env 文件提交至公开仓库。
