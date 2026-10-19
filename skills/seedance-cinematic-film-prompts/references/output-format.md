# Copy-Ready Output Format

Use this format when delivering full Seedance 2.5 prompt groups.

````markdown
### 第01组｜全片00:00–00:30｜场景名称｜30秒

```text
总时长：30s
统一视觉描述：时代、地域、电影或动画质感、角色身份锚点、现实空间地理、世界空间光源、天气、色彩、字幕与BGM规则。
对白连续性：仅在一条对白跨多个镜头时添加。说明完整音轨的时间范围、同步口型镜头、反应镜头中的同空间画外音，以及落句镜头。

片段01｜0–5s｜叙事落点
景别：
机位：
运镜：
构图：
场景氛围：
画面动作：
表演细节：
声音表演：
对白/音效：

片段02｜5–10s｜叙事落点
景别：
机位：
运镜：
构图：
场景氛围：
画面动作：
表演细节：
对白/音效：
```
````

## Exact dialogue spanning several visual shots

Do not create several sibling `片段` entries that each mention the continuing speaker. Some video models interpret every new segment or repeated `对白/音效` field as a fresh speech event. Use one parent dialogue segment with internal visual shots:

```text
片段01｜0–14s｜人物甲唯一连续发声
唯一发声规则：本片段只有一条人物甲对白音轨。画面切换不切换声音，不得重新起句，不得重复任何局部短语。

画面镜头A｜0–5s｜说话者开始施压
景别：双人中景
画面动作：人物甲开口，人物乙闭口聆听
音频状态：使用唯一对白音轨0–5s区间；人物甲同步当前时点口型

画面镜头B｜5–10s｜听者反应
景别：人物乙近景
画面动作：人物甲在画外继续，人物乙全程闭口
音频状态：无新对白事件；直接继承唯一对白音轨5–10s区间，保持同空间画外音，禁止回到0s

画面镜头C｜10–14s｜说话者落句
景别：人物甲近景
画面动作：人物甲完成落句后闭口等待
音频状态：无新对白事件；唯一对白音轨从10s当前位置继续至14s结束，恢复当前尾段同步口型

声音表演：整句在0–14s内一口逻辑完成，画面切换时语速和呼吸不中断。
对白/音效：人物甲：这里放完整、逐字保留的源对白
```

The exact line appears once and only once. Internal shots never contain `对白/音效`, a repeated speaker label, quoted source fragments, or the phrase `同一句对白持续`; they contain only `音频状态` tied to the single parent track's current time window.

## Group-level rules

- One fenced block is one generation request.
- Put one `统一视觉描述` in each group.
- Local timestamps start at zero and remain continuous.
- The last local timestamp equals `总时长`.
- Keep each group at or below 30 seconds.
- Use stable group and shot identifiers when the source already has them.
- Omit audit tables, scene-state tracking, and causal planning from the default user-facing prompt unless requested; carry their conclusions into concise shot instructions.
- Describe only lighting and performance details relevant to each shot. Shared rules belong in the group description; do not multiply prohibitions to compensate for unclear staging.
- A continuous take can contain several linked actions with one camera path. Do not introduce cuts merely to satisfy the template.
- Carry the last approved image/action into the next group. Do not repeat an entrance, exit, or transition the user has already completed.

## Dialogue TSV format

For long or high-risk work create:

```text
shot_id<TAB>speaker<TAB>dialogue
```

Use identical row order and identifiers in `source_dialogue.tsv` and `prompt_dialogue.tsv`, then run the dialogue checker.

## Full fields for internal images and continuous-take phases

Keep this structure for each internal image, including reaction shots, inserts, and time markers inside a long take:

```text
画面镜头A｜0–4s｜当前画面任务
景别：
机位：
运镜：
构图：
场景氛围：
画面动作：
表演细节：有重要表演任务时填写。
音频状态：本组0–4s，对应父音轨0–4s，继续同一发声事件。
```

For a continuous take, explicitly state that the labeled images are phases of one uninterrupted camera movement, not cuts. Each phase still names framing, position, movement, composition, environment, action, and audio state. Identify the follow-to-independent-camera transition when attention changes. For silent phases, audio state describes continuous location sound and no new dialogue. Do not insert repeated dialogue fields inside these images.

Shared lighting, weather, and prop continuity can be concise group-level descriptions. Per-image instructions need only their visible implications, not repeated prohibitions. During revisions preserve this field structure instead of collapsing it into unstructured timed prose.
