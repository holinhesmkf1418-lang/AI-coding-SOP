## 项目家规

# AI规划工作台 - claude.md

## 技术栈
前端: Vite + Vue3(Composition API) + TypeScript + Element Plus + Pinia + unplugin-auto-import
后端: FastAPI + Python + Pydantic v2 + SQLModel
数据库: SQLite(MVP) / PostgreSQL(生产)
部署: Nginx + 腾讯云轻量服务器

## 绝对红线
1. 零硬编码：所有模型标识、提示词内容、步骤规则、状态枚举必须由数据库或配置驱动，代码中禁止出现"gemini"等业务字符串字面量
2. 数据完整性：step_outputs的edited_output为空时必须fallback到ai_output，禁止丢失数据
3. API Key加密：禁止日志打印、前端传输明文Key，后端加解密使用Fernet对称加密
4. 变量注入必须校验：模板变量为空时阻断调用并报错，禁止发送残缺提示词
5. 步骤可扩展：步骤条从step_configs动态渲染，新增步骤只改数据库不改代码

## 编程行为约束
1. 谋定而后动：输出代码前先陈述假设，遇模糊需求列出选项不猜测
2. 配置化优先：新增模型/步骤/提示词只需改数据库，不改代码
3. 极简精准：只写解决当前问题的最少代码，不过度设计
4. 目标驱动：先写验证标准，再实现，再验证通过

---

## 当前任务：Task 1.3 创建projects和step_outputs两张表

**目标：** 用SQLModel定义数据模型，Alembic迁移建表

**具体要求：**

projects 表：
| 字段 | 类型 | 说明 |
|---|---|---|
| id | UUID | 主键 |
| name | String(100) | 项目名称 |
| initial_requirement | Text | 用户原始需求 |
| current_step | Integer | 当前步骤(1-7)，默认1 |
| status | String(20) | 状态：draft/active/delivered，默认draft |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

step_outputs 表：
| 字段 | 类型 | 说明 |
|---|---|---|
| id | UUID | 主键 |
| project_id | UUID | 外键→projects |
| step | Integer | 步骤编号(1-7) |
| model_key | String(50) | 使用的模型标识（配置化） |
| prompt_template_id | UUID | 使用的提示词模板ID（配置化） |
| ai_output | Text | AI原始产出 |
| edited_output | Text | 人工编辑后产出（为空则fallback到ai_output） |
| human_edit_diff | Text | 人工修改标注（JSON格式） |
| status | String(20) | 状态：pending/generating/generated/confirmed，默认pending |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

**关键约束：** SQLite开启WAL模式，写Alembic迁移脚本

**验收标准：** alembic upgrade head成功建表，字段完整，外键正确

**完成后提交git。**
