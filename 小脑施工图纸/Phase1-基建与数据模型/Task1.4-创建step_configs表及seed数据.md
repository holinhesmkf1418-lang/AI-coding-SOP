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

## 当前任务：Task 1.4 创建step_configs表及seed数据

**目标：** 建立步骤配置表，控制1~7步的启用状态

**具体要求：**

step_configs 表：id(UUID主键)、step(Integer 1-7唯一)、name(String50配置化)、brain_type(String20)、need_model(Boolean)、need_terminal(Boolean)、is_active(Boolean)、sort_order(Integer)

**seed数据7条：**
1. 磨透需求 | brain | need_model=True | need_terminal=False | is_active=True
2. 定死架构 | brain | need_model=True | need_terminal=False | is_active=True
3. 出开发计划 | brain | need_model=True | need_terminal=False | is_active=True
4. 人工审计 | brain | need_model=True | need_terminal=False | is_active=True
5. 分阶段写码 | cerebellum | need_model=True | need_terminal=True | is_active=False
6. 调BUG | cerebellum | need_model=True | need_terminal=True | is_active=False
7. 测试自愈 | cerebellum | need_model=True | need_terminal=True | is_active=False

**关键约束：** 写seed脚本 backend/seed_step_configs.py 可重复执行（存在则跳过）

**验收标准：** 迁移成功，seed脚本执行后7条数据正确，可重复执行不报错

**完成后提交git。**
