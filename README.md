# AI编程规划工作台 — 项目大本营

> 项目代号：ai-planning-workbench
> 创建时间：2026-06-23
> 状态：规划完成，待开发

---

## 📂 目录结构

```
ai-planning-workbench/
├── docs/                    ← 项目文档
│   ├── claude.md            ← 家规（每个小脑Task必带）
│   └── 原子化开发计划.md     ← 44个Task清单（打勾用）
├── 小脑施工图纸/             ← 44个独立Task文件
│   ├── Phase1-基建与数据模型/   8个文件
│   ├── Phase2-后端核心API/     15个文件
│   ├── Phase3-前端视图与交互/   18个文件
│   └── Phase4-测试与联调验证/   10个文件
├── frontend/                ← 前端代码（Task1.1创建）
├── backend/                 ← 后端代码（Task1.2创建）
└── README.md                ← 本文件
```

---

## 🚀 怎么开干

1. 打开 `小脑施工图纸/Phase1-基建与数据模型/Task1.1-初始化前端工程.md`
2. 全选复制，粘贴到 Codex/Claude Code 新对话
3. 开头加一句：**项目目录：`~/Desktop/ai-planning-workbench`，前端代码在 `frontend/`，后端代码在 `backend/`**
4. 小脑干活，完成后 git commit
5. 打开下一个Task，重复

---

## 📋 开发节奏

- 每个 Task = 2~4小时可完成的原子单元
- **一个Task一个对话框**，别在同一个对话里连续发
- 每完成一个Task，让小脑 `git commit`
- Task文件自带家规，直接复制粘贴即可
- 小脑跑偏用提示词③（代码审计与重构）纠

---

## 🔑 技术栈

| 层级 | 选型 |
|---|---|
| 前端 | Vite + Vue3 + TS + Element Plus + Pinia + unplugin-auto-import + TailwindCSS |
| 后端 | FastAPI + Python + Pydantic v2 + SQLModel |
| 数据库 | SQLite(MVP) / PostgreSQL(生产) |
| 部署 | Nginx + 腾讯云轻量服务器(4核4G40G) |

---

## 🔴 绝对红线

1. 零硬编码：模型标识/步骤规则/状态枚举全走数据库
2. 数据完整性：edited_output为空fallback到ai_output
3. API Key加密：Fernet对称加密，日志禁止明文
4. 变量注入校验：模板变量为空时阻断报错
5. 步骤可扩展：步骤条从step_configs动态渲染

---

## 📎 相关资源

- 完整项目文档（PRD+架构+前端设计+部署方案）：找旺财要
- 7个SOP提示词完整内容：提示词①②③⑦已提供，④⑤⑥待补充
- 腾讯云服务器：4核4G40G Linux，已有小程序+备案域名
