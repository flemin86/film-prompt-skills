# Film Prompt Skills

面向历史剧情片、人物传记及严肃剧情的 Seedance 2.5 中文分镜提示词技能。重点处理人物互动、动作因果、场景动线、光线连续性，以及跨镜头的连续对白。

## 使用限制

本仓库公开供个人非商业学习和使用，**不授权修改、转载或商用**，不采用 MIT 等开源许可证。完整条件见 [LICENSE](LICENSE)。请从本仓库下载完整原版，不重新分发副本。

## 在 Codex 中安装

将以下内容发给 Codex：

```text
请使用 $skill-installer 安装这个 GitHub 仓库里的技能：
https://github.com/flemin86/film-prompt-skills/tree/main/skills/seedance-cinematic-film-prompts
```

安装完成后，在下一轮对话中调用；如果未出现，重启 Codex 后再试。安装命令是对 Codex 的请求，不是终端命令。目标目录已有同名技能时，先处理版本选择，不直接覆盖本地修改。

## 调用示例

```text
使用 $seedance-cinematic-film-prompts，把下面的剧本生成一组30秒以内的分镜提示词。
保留原对白，让人物通过实际动作互动，保持轴线、灯位和道具连续。
不要字幕和配乐。按“景别、机位、运镜、构图、场景氛围、画面动作、音频状态”等字段输出。

（在此粘贴剧本）
```

## 完整使用案例

- [原创输入剧本：《夜仓分粮》](examples/夜仓分粮/01_输入剧本.md)
- [对应提示词输出](examples/夜仓分粮/02_分镜提示词.md)

案例仅展示输出格式与导演方法，并非实际视频生成效果或效果保证。它使用独立虚构人物，不包含项目剧本、客户资料、图片、视频或聊天记录。

## 技能目录

```text
skills/seedance-cinematic-film-prompts/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── film-language.md
│   ├── spatial-continuity.md
│   └── output-format.md
└── scripts/
    ├── check_seedance_timing.py
    └── check_dialogue_exact.py
```

请保留整个技能目录，参考文件与脚本供技能按需调用。技能负责编写提示词，视频生成需在用户选择的平台另行完成。自动检查脚本需要 Python 3。
