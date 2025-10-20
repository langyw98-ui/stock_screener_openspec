## core principle

Thinking in English，Communicating in Chinese



## 第三方库的API文档

xtquant库的API文档见api/xtquant.md


## 执行测试出错时的应对原则

程序出错，不应去修改数据文件，而应去修改代码，以适应的数据文件。
data下的文件不应该被修改，也不允许添加新的文件。

## 获取股票数据的时间范围

生成的测试代码，在设置获取股票数据的时间范围是必须是2025年1月1日之后的数据。

<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->