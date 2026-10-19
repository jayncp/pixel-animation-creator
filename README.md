# 全流程像素角色动画 Skill

版本：2.1.0。可从文字、普通参考图、像素参考图，或已经完成的任意制作阶段接入。

本仓库交付的是可维护的制作技能与验证工具，不是专用训练模型，也不保证一次生成即达到最终质量。它要求执行 agent 自主研究、制作、看图/播放、发现问题、修复并再验收。原有角色素材不打包进通用 skill；可同时提供先前的项目压缩包继续那个角色。

## 从这里开始

- 技能入口：[`skills/pixel-character-animation/SKILL.md`](skills/pixel-character-animation/SKILL.md)。
- 中文使用说明：[`skills/pixel-character-animation/START_HERE_ZH.md`](skills/pixel-character-animation/START_HERE_ZH.md)。
- 新项目默认每个角色参考视角 **256×256**；用户指定尺寸优先；继续旧项目时保留其现有尺寸。
- 新完整参考集未指定角度时，默认正面、三分之四、侧面、背面。已有参考或仅需部分角度时，不强制重做。
- 动画不设固定帧数上限；按动作、真实时间节奏与信息完整度决定。

你可以在新的对话附上此 ZIP 与角色项目包，说：

> 请使用仓库中的 pixel-character-animation skill，先读取实际素材和恢复索引，从已有阶段继续。为这个角色制作一次蓄力后快速释放的动作，自主研究、逐帧检查、修复并验证。不要改动冻结原件。

也可以只给新描述或普通图片。缺少生图、播放器、原生编辑器等能力时，必须说明具体缺口，不能把未做的步骤记作通过。

## 项目内使用，不默认全局安装

最轻方式：把本仓库放在工作目录，让 agent 读取技能入口。无需安装到个人账号。

若所用客户端明确支持项目级技能发现，可以把 `skills/pixel-character-animation/` 复制到该项目支持的技能目录。例如支持 `.agents/skills/` 的客户端可使用 `.agents/skills/pixel-character-animation/`。先检查目录是否已有同名技能，保留现有版本，不覆盖未知文件。其他 agent 按其真实文档配置，不假设路径通用。

工具适配与项目内 MCP 模板见 [`tool-adapters.md`](skills/pixel-character-animation/references/tool-adapters.md)。配置文件只是模板，不自动运行或注册。仓库没有工具二进制、API 密钥、账号凭据或私有角色图像。

## 工作流

输入/已有阶段检查 → 像素形象与必要多视角 → 动作资料研究与比例适配 → 关键姿势和节奏草稿 → 选择性补帧与完整动画 → 特征/边缘/逐帧与播放验收 → 可编辑源文件和导出 → 可恢复项目。

这不是强制从头执行的流水线。边缘修复可以直接进入修复；仅要参考图就停在参考阶段；已完成 PNG 序列可直接核验和导出。技术校验与审美/动势判断始终分开。

## 内容

- `skills/`：可移植技能、按需参考文档、规格模板、审计与导出脚本。
- `docs/`：需求追踪、研究取舍、维护/发布说明和验证报告。
- `evals/`：不同输入与中途接入的行为测试场景。
- `scripts/`：仓库级验证与打包工具。
- `.git/`：真实 Git 仓库历史。ZIP 包含此隐藏目录；不要只用 `git archive` 代替本发布包。

## 本地开发与测试

要求 Python 3.10+，图像脚本需要 Pillow。优先使用项目内虚拟环境；安装包前遵守当前运行环境授权。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r skills/pixel-character-animation/requirements.txt
.venv/bin/python -m unittest discover -s skills/pixel-character-animation/tests -v
.venv/bin/python scripts/validate_repo.py
```

Windows 可用 `.venv\Scripts\python.exe`。不需要全局 pip、sudo、全局 MCP 注册或 shell 配置修改。已有满足要求的环境可直接运行，不必重复安装。

详见 [维护与发布](docs/MAINTAINING.md)、[验证结果](docs/VALIDATION.md) 与 [变更记录](CHANGELOG.md)。源码仓库：<https://github.com/jayncp/pixel-animation-creator>。skill 不会安装到你的账号。
