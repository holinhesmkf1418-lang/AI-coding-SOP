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

## 当前任务：Task 1.5 创建model_configs和usage_logs两张表

**目标：** 模型配置表和用量日志表

**具体要求：**

model_configs 表：id、provider(String50配置化)、model_name(String100配置化)、api_url(String500配置化)、api_key_encrypted(Text Fernet加密)、is_active(Boolean默认False)、daily_limit(Integer配置化默认0)、created_at、updated_at

usage_logs 表：id、model_config_id(UUID外键)、project_id(UUID外键)、step(Integer)、input_tokens(Integer默认0)、output_tokens(Integer默认0)、called_at(DateTime)

**关键约束：** api_key_encrypted使用Fernet对称加密，密钥从环境变量ENCRYPTION_KEY读取。暂不实现加密逻辑（Task 2.10实现），此处只建表

**验收标准：** 迁移成功建表，字段完整，外键正确

**完成后提交git。**
