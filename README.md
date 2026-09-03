# AL AI Assistant

基于 Python、FastAPI、MySQL、Redis 和大语言模型 API 构建的 AI Assistant 项目，并完成 Docker 容器化、GitHub Actions CI/CD、阿里云 ECS + ACR 部署，以及 Prometheus + Grafana 应用监控与 Email 告警。

项目不仅实现 AI 对话和用户认证等基础功能，同时将项目完整部署到云服务器，并建立从代码提交、镜像构建、镜像推送到 ECS 自动部署的 CI/CD 流程。

当前正式版本：**v1.4.7**

---

## 1. 项目简介

AL AI Assistant 是一个基于 FastAPI 的 AI 对话服务。

项目采用前后端分离的 API 服务模式，通过大语言模型 API 提供 AI 对话能力，并使用 MySQL 保存业务数据、Redis 提供缓存及相关运行支撑。

在应用开发基础上，项目进一步进行了容器化和云端部署：

* Python + FastAPI 构建后端 API
* MySQL 持久化业务数据
* Redis 提供缓存及运行支撑
* Docker Compose 管理多容器服务
* Alibaba Cloud ECS 作为生产环境
* Alibaba Cloud ACR 存储 Docker 镜像
* GitHub Actions 实现 CI/CD
* Prometheus 采集应用指标
* Grafana 构建监控 Dashboard
* Grafana Alerting + SMTP 实现 Email 告警
* MySQL 自动备份与历史备份清理
* Health Check 检测应用运行状态
* 环境变量与 GitHub Secrets 分离管理敏感信息

---

## 2. 核心功能

### AI 对话

* 集成大语言模型 API
* 支持普通对话请求
* 支持流式响应
* 封装独立 LLM Service

### 用户认证

* 用户注册
* 用户登录
* JWT 身份认证
* Token 黑名单
* 密码安全处理

### 对话历史

* 保存用户对话记录
* 查询历史消息
* MySQL 持久化数据

### Redis

* Redis 缓存
* Token / 运行时数据相关支撑
* Docker 持久化

### 异常处理

* 统一业务异常
* 全局异常处理器
* 请求日志记录
* API 请求限流

---

# 3. 技术栈

| 类型                      | 技术                      |
| ----------------------- | ----------------------- |
| 编程语言                    | Python                  |
| Web Framework           | FastAPI                 |
| API Server              | Uvicorn                 |
| Database                | MySQL 8.4               |
| Cache                   | Redis 7                 |
| ORM / Database Access   | MySQL Connector / SQL   |
| Authentication          | JWT                     |
| Password Security       | bcrypt                  |
| Containerization        | Docker                  |
| Container Orchestration | Docker Compose          |
| CI/CD                   | GitHub Actions          |
| Container Registry      | Alibaba Cloud ACR       |
| Cloud Server            | Alibaba Cloud ECS       |
| Reverse Proxy           | Nginx                   |
| Monitoring              | Prometheus              |
| Visualization           | Grafana                 |
| Alerting                | Grafana Alerting + SMTP |
| Version Control         | Git / GitHub            |

---

# 4. 系统架构

```text
                         GitHub
                            │
                   Push / Tag v1.x.x
                            │
                            ▼
                    GitHub Actions
                            │
              ┌─────────────┴─────────────┐
              │                           │
             Test                   Docker Build
              │                           │
              │                           ▼
              │                    Alibaba Cloud ACR
              │                           │
              └──────────────┬────────────┘
                             │
                        SSH Deploy
                             │
                             ▼
                    Alibaba Cloud ECS
                             │
                        Docker Compose
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     FastAPI App           MySQL              Redis
          │
          │ /metrics
          ▼
     Prometheus
          │
          ▼
       Grafana
          │
          ├── Dashboard
          │
          └── Alerting
                  │
                  ▼
              Email SMTP
```

---

# 5. Docker 架构

生产环境通过 Docker Compose 管理多个服务：

```text
al-ai-assistant
│
├── app
│   └── FastAPI + Uvicorn
│
├── mysql
│   └── MySQL 8.4
│
├── redis
│   └── Redis 7
│
├── prometheus
│   └── Prometheus 3.5.0
│
└── grafana
    └── Grafana
```

应用及基础设施均通过 Docker 容器运行。

核心服务：

```text
app
    127.0.0.1:8000 → 8000

prometheus
    127.0.0.1:9091 → 9090

grafana
    127.0.0.1:3001 → 3000
```

监控服务只绑定 ECS 本机地址，不直接暴露到公网。

---

# 6. CI/CD

项目使用 GitHub Actions 实现自动化 CI/CD。

## main 分支

向 `main` 推送代码时执行测试流程：

```text
git push
    │
    ▼
GitHub Actions
    │
    ▼
Run Tests
```

用于验证代码提交是否能够通过基础测试。

---

## Git Tag 发布

创建正式版本 Tag 后触发完整部署流程：

```text
git tag v1.4.7
git push origin v1.4.7
        │
        ▼
GitHub Actions
        │
        ├── Test
        │
        ├── Docker Build
        │
        ├── Push Image → ACR
        │
        └── Deploy ECS
                 │
                 ▼
          docker compose pull
                 │
                 ▼
          docker compose up -d
```

Docker 镜像 Tag 与 Git Release Tag 保持一致。

例如：

```text
Git Tag:
v1.4.7

Docker Image:
al-ai-assistant:v1.4.7
```

---

# 7. IMAGE_TAG 部署机制

生产环境的 `.env` 不保存 `IMAGE_TAG`。

部署时由 GitHub Actions 根据当前 Git Tag 动态传递：

```text
github.ref_name
        │
        ▼
IMAGE_TAG=v1.4.7
        │
        ▼
ECS docker compose
        │
        ▼
ACR:
al-ai-assistant:v1.4.7
```

这样可以避免将具体发布版本写死在 ECS 环境配置中。

---

# 8. Health Check

应用提供：

```text
GET /health
```

正常情况下返回：

```json
{
  "status": "ok"
}
```

Docker Compose 同时配置了容器级 Health Check：

```text
Docker
   │
   ▼
http://127.0.0.1:8000/health
   │
   ├── 正常 → healthy
   │
   └── 异常 → unhealthy
```

Health Check 用于判断应用容器是否真正能够正常响应，而不仅仅是进程是否存在。

---

# 9. Prometheus 应用监控

应用暴露 Prometheus Metrics：

```text
/metrics
```

Prometheus 定期抓取：

```text
app:8000/metrics
```

当前已经验证：

```text
job      = al-ai-assistant
instance = app:8000
health   = up
```

应用指标包括：

* HTTP 请求总数
* HTTP 请求耗时
* HTTP 响应状态
* HTTP 请求速率
* HTTP 5xx 请求
* P95 Request Latency
* Python Process Metrics
* Python GC Metrics
* Prometheus Scrape Metrics

---

# 10. Grafana Dashboard

Grafana 用于展示 AL AI Assistant 应用运行状态。

当前 Dashboard 包含：

### HTTP Request Rate

用于观察 API 请求流量。

### HTTP 5xx Error Rate

用于观察服务器端错误比例。

### P95 Request Latency

用于观察 95% 请求的响应延迟。

### Application Status

通过 Prometheus `up` 指标观察应用是否正常运行。

---

# 11. Grafana Alerting

当前已经配置：

## Application Down

核心判断依据：

```text
Prometheus up == 0
```

告警状态：

```text
Normal
   │
   ▼
Pending
   │
   ▼
Firing
```

当应用恢复：

```text
Firing
   │
   ▼
Normal
```

已经在 ECS 生产环境进行实际故障测试。

测试过程：

```text
docker stop al-ai-assistant
        │
        ▼
Prometheus 检测应用不可用
        │
        ▼
Grafana Pending
        │
        ▼
Grafana Firing
        │
        ▼
Email Alert
        │
        ▼
docker start al-ai-assistant
        │
        ▼
Grafana 恢复 Normal
```

**该告警链路已经完成实际验证。**

---

# 12. Email Notification

Grafana Alerting 使用 SMTP 发送 Email 通知。

已实际完成：

```text
Grafana Alert
      │
      ▼
Contact Point
      │
      ▼
SMTP
      │
      ▼
QQ Mail
```

并成功收到测试邮件及 Application Down 告警邮件。

SMTP 凭据不会提交到 Git 仓库。

---

# 13. MySQL 自动备份

生产环境配置 MySQL 自动备份脚本。

备份流程：

```text
MySQL
  │
  ▼
mysqldump
  │
  ▼
gzip 压缩
  │
  ▼
mysql_backups/
```

备份文件格式：

```text
al_ai_YYYYMMDD_HHMMSS.sql.gz
```

例如：

```text
al_ai_20260831_214001.sql.gz
```

同时配置历史备份清理：

```text
保留最近 7 天
        │
        ▼
自动删除过期备份
```

备份脚本已经在 ECS 上实际执行并验证成功。

---

# 14. 数据持久化

生产环境使用宿主机目录保存重要数据。

```text
/data/apps/al-ai-assistant/
│
├── mysql/
├── redis/
├── prometheus/
├── grafana/
└── mysql_backups/
```

因此容器重新创建不会直接导致这些持久化数据丢失。

Grafana 使用：

```text
/data/apps/al-ai-assistant/grafana
        ↓
/var/lib/grafana
```

保存 Dashboard、Data Source、Alert Rule 等 Grafana 数据。

---

# 15. Secrets 安全

项目采用环境变量和 GitHub Secrets 管理敏感信息。

生产环境敏感配置保存在 ECS：

```text
.env
```

示例：

```text
API_KEY
SECRET_KEY
DB_PASSWORD
DB_ROOT_PASSWORD
GRAFANA_SMTP_PASSWORD
```

Git 仓库只保留：

```text
.env.example
```

GitHub Actions 使用：

```text
GitHub Secrets
```

保存：

```text
ECS_HOST
ECS_USER
ECS_SSH_KEY
ACR_USERNAME
ACR_PASSWORD
```

敏感信息不会直接写入应用代码或 Git 仓库。

---

# 16. 项目目录

```text
AL-AI-Assistant/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── history.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exception.py
│   │   ├── exception_handler.py
│   │   ├── logger.py
│   │   ├── middleware.py
│   │   ├── password.py
│   │   ├── rate_limit.py
│   │   ├── redis.py
│   │   ├── security.py
│   │   └── token_blacklist.py
│   │
│   ├── models/
│   ├── repositories/
│   ├── services/
│   │
│   └── main.py
│
├── nginx/
│   └── nginx.conf
│
├── tests/
│   └── test_ci.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── compose.yaml
├── migrate_sqlite_to_mysql.py
├── requirements.txt
└── README.md
```

生产环境中的部分运行时配置，例如 Prometheus 配置、数据库备份脚本和 `.env`，仅部署在 ECS，不提交到 Git 仓库。

---

# 17. 环境配置

项目区分为：

* 本地开发环境
* ECS 生产环境

两种环境使用不同的 `.env`，但均基于 `.env.example` 配置。

---

## 17.1 本地开发环境

本地运行主要用于：

* 编写代码
* 调试 API
* 运行测试
* Docker Compose 验证
* 功能开发

创建配置：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

本地 `.env` 示例：

```env
API_KEY=your_deepseek_api_key

BASE_URL=https://api.deepseek.com

MODEL=deepseek-v4-flash

SECRET_KEY=your_local_secret_key

DB_HOST=mysql
DB_PORT=3306
DB_NAME=al_ai
DB_USER=ai_user
DB_PASSWORD=your_database_password
DB_ROOT_PASSWORD=your_root_password

REDIS_HOST=redis
REDIS_PORT=6379

RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
```

### 本地运行注意事项

本地环境不需要配置 Grafana SMTP。

如果只是运行应用：

```env
GRAFANA_SMTP_USER=
GRAFANA_SMTP_PASSWORD=
```

可以保持为空。

---

## 17.2 本地 Docker Compose

如果使用：

```bash
docker compose up -d
```

则：

```text
DB_HOST=mysql
REDIS_HOST=redis
```

不能填写：

```text
localhost
```

因为应用运行在 Docker 容器中。

Docker Compose 网络结构：

```text
app
 │
 ├── mysql:3306
 │
 └── redis:6379
```

因此：

```env
DB_HOST=mysql
REDIS_HOST=redis
```

是正确配置。

---

## 17.3 IMAGE_TAG 与本地运行

生产环境中的 `IMAGE_TAG` 由 GitHub Actions 在部署时注入。

ECS `.env` 不需要保存：

```env
IMAGE_TAG=
```

如果本地需要直接运行当前 ACR 中的应用镜像，则需要提供一个有效的镜像 Tag，例如：

```env
IMAGE_TAG=v1.4.6
```

然后：

```bash
docker compose pull
docker compose up -d
```

如果本地只是使用 Python 直接运行：

```bash
uvicorn app.main:app --reload
```

则不需要 `IMAGE_TAG`。

---

# 18. ECS 生产环境配置

ECS 上的 `.env` 只保存在服务器：

```text
/data/apps/al-ai-assistant/.env
```

**不会提交到 Git 仓库。**

ECS `.env` 包含：

```env
API_KEY=<production-api-key>

BASE_URL=https://api.deepseek.com

MODEL=deepseek-v4-flash

SECRET_KEY=<production-secret-key>

DB_HOST=mysql
DB_PORT=3306
DB_NAME=al_ai
DB_USER=ai_user
DB_PASSWORD=<production-db-password>
DB_ROOT_PASSWORD=<production-root-password>

REDIS_HOST=redis
REDIS_PORT=6379

RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

GRAFANA_SMTP_USER=<smtp-account>
GRAFANA_SMTP_PASSWORD=<smtp-password-or-app-password>
```

其中：

```text
API_KEY
SECRET_KEY
DB_PASSWORD
DB_ROOT_PASSWORD
GRAFANA_SMTP_PASSWORD
```

均属于敏感信息。

不要提交到 GitHub。

---

# 19. ECS 生产环境启动

进入项目目录：

```bash
cd /data/apps/al-ai-assistant
```

检查 `.env`：

```bash
ls -la .env
```

检查 Compose 配置：

```bash
docker compose config
```

如果配置正确，应正常输出 Compose 配置，不出现：

```text
invalid interpolation format
```

或：

```text
variable is not set
```

然后拉取镜像：

```bash
docker compose pull
```

启动：

```bash
docker compose up -d
```

检查：

```bash
docker compose ps
```

---

# 20. ECS 中的 IMAGE_TAG

ECS `.env` 不保存 `IMAGE_TAG`。

生产发布版本由 GitHub Actions 根据 Git Tag 传入。

例如：

```text
Git Tag
v1.4.7
   │
   ▼
GitHub Actions
   │
   ▼
IMAGE_TAG=v1.4.7
   │
   ▼
ECS
   │
   ▼
al-ai-assistant:v1.4.7
```

这样 ECS 上的环境变量与发布版本解耦。

---

# 21. ECS 监控配置

Prometheus 和 Grafana 属于生产环境监控组件。

Prometheus：

```text
127.0.0.1:9091 → 9090
```

Grafana：

```text
127.0.0.1:3001 → 3000
```

Grafana SMTP 配置使用 ECS `.env` 中：

```env
GRAFANA_SMTP_USER=<smtp-account>
GRAFANA_SMTP_PASSWORD=<smtp-password-or-app-password>
```

这些配置不会进入 Git 仓库。

---

# 22. 本地环境与 ECS 环境对比

| 配置                  | 本地              | ECS               |
| ------------------- | --------------- | ----------------- |
| API_KEY             | 本地 API Key      | 生产 API Key        |
| BASE_URL            | 相同              | 相同                |
| MODEL               | 相同              | 相同                |
| SECRET_KEY          | 本地 Secret       | 独立生产 Secret       |
| DB_HOST             | mysql           | mysql             |
| DB_PORT             | 3306            | 3306              |
| DB_NAME             | al_ai           | al_ai             |
| DB_USER             | ai_user         | ai_user           |
| DB_PASSWORD         | 本地数据库密码         | 生产数据库密码           |
| DB_ROOT_PASSWORD    | 本地 Root 密码      | 生产 Root 密码        |
| REDIS_HOST          | redis           | redis             |
| REDIS_PORT          | 6379            | 6379              |
| RATE_LIMIT_REQUESTS | 10              | 10                |
| RATE_LIMIT_WINDOW   | 60              | 60                |
| Grafana SMTP        | 可为空             | 配置                |
| IMAGE_TAG           | 本地 Docker 运行时可选 | GitHub Actions 注入 |

---

# 23. 配置安全原则

项目遵循以下原则：

```text
.env.example
     │
     ├── 提供变量名称
     ├── 提供默认非敏感配置
     └── 不包含真实凭据

        ↓

本地 .env
     │
     └── 本地开发配置

ECS .env
     │
     └── 生产环境配置

GitHub Secrets
     │
     └── CI/CD 敏感配置
```

生产环境 `.env` 不进入 Git。

检查：

```bash
git status
```

确认：

```text
.env
```

没有出现在待提交文件中。

同时检查：

```bash
git ls-files
```

应存在：

```text
.env.example
```

但不应存在：

```text
.env
```


# 20. CI/CD 发布示例

以 `v1.4.7` 为例：

```bash
git tag v1.4.7
git push origin v1.4.7
```

GitHub Actions 自动执行：

```text
Test
 ↓
Build Docker Image
 ↓
Push ACR
 ↓
Deploy ECS
```

ECS 使用：

```text
IMAGE_TAG=v1.4.7
```

部署对应镜像：

```text
al-ai-assistant:v1.4.7
```

---

# 21. 版本记录

## v1.4.6

**feat: add prometheus application monitoring**

主要内容：

* 增加 Prometheus 应用监控
* 增加 `/metrics`
* 增加 Prometheus 服务
* 增加 Grafana 服务
* 增加应用 Dashboard
* 增加 Application Down Alert
* 增加 Email Notification
* 完成生产环境监控链路验证

## v1.4.5

**feat: add application health check**

主要内容：

* 增加 `/health`
* 增加 Docker Health Check
* 验证 ECS 应用健康状态

---

# 22. 项目最终验收

当前项目已经完成以下生产环境能力：

| 能力                     | 状态     |
| ---------------------- | ------ |
| FastAPI API            | ✅      |
| MySQL                  | ✅      |
| Redis                  | ✅      |
| Docker                 | ✅      |
| Docker Compose         | ✅      |
| Alibaba Cloud ECS      | ✅      |
| Alibaba Cloud ACR      | ✅      |
| GitHub Actions CI      | ✅      |
| GitHub Actions CD      | ✅      |
| Tag 自动发布               | ✅      |
| Health Check           | ✅      |
| MySQL 自动备份             | ✅      |
| 7 天备份清理                | ✅      |
| Secrets 管理             | ✅      |
| Prometheus             | ✅      |
| Grafana                | ✅      |
| Application Dashboard  | ✅      |
| Application Down Alert | ✅      |
| Email Notification     | ✅      |
| 故障告警实测                 | ✅      |


---

# 23. 项目亮点

### 1. 完整 CI/CD 流程

实现从 Git Tag 到 Docker 镜像构建、ACR 推送以及 ECS 自动部署的完整链路。

### 2. 容器化部署

使用 Docker Compose 管理应用、MySQL、Redis、Prometheus 和 Grafana。

### 3. 云端生产环境

项目实际部署在 Alibaba Cloud ECS，并使用 ACR 管理生产 Docker 镜像。

### 4. 应用级可观测性

通过 Prometheus + Grafana 对 FastAPI 应用进行指标采集和可视化。

### 5. 故障告警闭环

实际验证：

```text
应用停止
   ↓
Prometheus 检测
   ↓
Grafana Pending
   ↓
Grafana Firing
   ↓
Email 告警
   ↓
应用恢复
   ↓
Grafana Normal
```

### 6. 数据安全与运维

通过环境变量、GitHub Secrets、MySQL 自动备份以及持久化存储降低生产环境数据和配置风险。

---

# 24. 当前项目定位

AL AI Assistant 不仅是一个 AI 对话 API 项目，同时作为一个完整的云端部署与 DevOps 实践项目，覆盖：

```text
Application Development
        ↓
Containerization
        ↓
CI/CD
        ↓
Cloud Deployment
        ↓
Health Check
        ↓
Backup
        ↓
Monitoring
        ↓
Alerting
        ↓
Production Verification
```

项目重点体现 Python 后端开发、Docker 容器化、GitHub Actions CI/CD、Alibaba Cloud ECS/ACR、Prometheus/Grafana 监控以及生产环境运维实践能力。

---

## License

本项目仅用于个人学习、技术实践及作品集展示。
