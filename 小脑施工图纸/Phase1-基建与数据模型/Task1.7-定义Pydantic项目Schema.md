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

## 当前任务：Task 1.7 定义Pydantic项目相关Schema

**目标：** 定义项目、步骤产出、步骤配置的Pydantic v2请求/响应模型

**具体要求：**
1. ProjectCreate: name(必填), initial_requirement(必填)
2. ProjectUpdate: name(可选), initial_requirement(可选), status(可选)
3. ProjectResponse: id, name, initial_requirement, current_step, status, created_at, updated_at, step_outputs(列表)
4. StepOutputResponse: id, project_id, step, model_key, prompt_template_id, display_content(fallback逻辑), has_edited(bool), status, created_at, updated_at
5. StepConfigResponse: id, step, name, brain_type, need_model, need_terminal, is_active, sort_order

**关键约束：** display_content = edited_output if edited_output else ai_output（fallback）。has_edited = edited_output is not None and edited_output != ai_output。使用Pydantic v2的model_config = ConfigDict(from_attributes=True)

**验收标准：** 所有Schema定义完整无报错，fallback逻辑正确，Pydantic v2语法规范

**完成后提交git。**
