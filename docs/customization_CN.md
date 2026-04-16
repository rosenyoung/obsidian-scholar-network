# 自定义指南

这个仓库默认附带的是一套 **金融经济学** 主题词汇表和示例笔记，但整体结构本身是刻意做成与学科无关的。本文档说明如何把它迁移到你自己的研究领域。

---

## 1. 替换主题词汇表

最重要、最需要先改的文件是：

```
vault-starter/Scholars/_Scholar Topic Vocabulary.md
```

保留结构，替换内容：

- `###` 标题定义的是 **broad families**（大类）——它们决定颜色分组和布局上的相对邻近关系
- 表格中的每一行定义一个该 family 下的合法 topic
- 可视化脚本会直接读取这些 family，代码里没有写死任何主题结构

一个 family 的示例大致如下：


### Pricing & Returns {color=#1F77B4}

| Topic | Describes a Scholar Known For... | Example Gatekeepers |
|-------|----------------------------------|---------------------|
| `factor models` | Building/testing cross-sectional pricing models | Eugene Fama |
| `return predictability` | Time-series and cross-sectional forecasting | John Cochrane |


### 为什么 `###` 标题很重要

脚本会把每个 `###` 标题当成一个 family 名称，并据此推导出：

- 这个 family 的 **基础颜色**（自动从调色板分配，或通过 `{color=#HEX}` 手动指定）
- 该 family 内每个 topic 的 **相近色阶** —— 这样 `factor models` 和 `return predictability` 看起来像“同一家族”，而不是彼此毫无关系
- 同一 family 内不同 topic anchor 之间的 **弱隐藏布局连接**，让相关 cluster 在视觉上彼此靠近，但又不会压过真实的合作关系结构

如果你把整个词汇表压平成一个没有 `###` 标题的单列表，网络图就会失去语义结构：每个 topic 都会拿到一个独立颜色，并在布局中自由漂移。family 的存在，决定了这张图是“有信息含义”，而不只是“看起来好看”。

---

## 2. 选择合适的主题粒度

Scholar topic 应该回答的问题是：**“这个人是因为什么而被大家记住的？”**

**合适的粒度：**
- `attention` —— 足够具体，能够识别一个研究圈层
- `fund flows` —— 对应一个真实存在的研究社群
- `climate finance` —— 一个明确且持续扩张的子领域

**过宽（避免）：**
- `behavioral finance` —— 里面包含太多彼此不同的子社群
- `corporate finance` —— 会让大量本不相关的学者共用同一个标签

**过窄（避免）：**
- `EDGAR download patterns` —— 这是数据来源，不是学术身份
- `SPAC lockup expiration` —— 这更像一篇论文题目，不是一个学者“以此著称”的方向

一个实用判断标准：如果你做了 30+ 个 scholar profile 之后，某个 topic 仍然只有不到 2 位学者会共享，那这个 topic 很可能太窄，应该考虑并入更宽一级的主题。

---

## 3. 调整 Profiler Prompt

AI 处理用的 prompt 在这里：

```
vault-starter/Agent Prompt/Scholar-profiler.md
```

当你迁移到一个新学科时，通常需要调整：

| 需要修改的内容 | 原因 |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| 金融领域特定的期刊名称（JF、JFE、RFS...） | 换成你所在学科的顶级发表渠道 |
| `fields` 里的金融领域标签 | 改成你所在学科的 broad categories |
| literature note 的交叉引用路径 | 指向你自己的文献笔记目录；如果你没有这套体系，也可以删掉 |
| role 相关措辞和职业阶段标记 | 如果你的领域职级体系不同，需要同步调整 |
| gatekeeper 的判断标准 | 按你所在学科重设，因为“什么叫定义一个主题”在不同学科里并不相同 |

这个 profiler prompt 的设计目标是适配 **任何** LLM。你不需要绑定某一个 AI 服务——ChatGPT、Claude、Gemini，或者任何能遵循结构化指令的模型都可以使用。

---

## 4. 调整可视化聚类强度

在 `scripts/scholar_network.py` 中，有两个常量控制布局把相关学者拉在一起的强度：

```python
TOPIC_GLUE_LENGTH = 300    # same topic → weak attraction
FAMILY_GLUE_LENGTH = 420   # same family, different topic → weaker attraction
```

**值越小 = 拉力越强**（节点聚得更紧）。**值越大 = 布局越松**（节点分得更开）。

什么时候需要调整：

| 现象 | 处理方式 |
|---------|-----|
| 同一 topic 的学者散落在图的不同位置 | 降低 `TOPIC_GLUE_LENGTH`（可先试 200） |
| 同一 family 下的相关 topic 距离太远 | 降低 `FAMILY_GLUE_LENGTH`（可先试 350） |
| topic cluster 过于紧密，彼此重叠 | 同时调高两个值 |
| 布局看起来被 topic 标签主导，而不是由合作关系主导 | 同时调高两个值 —— coauthorship edge 应该始终是主要布局驱动 |

核心原则是：**coauthorship edges 必须始终主导布局。** 这些 glue links 的作用，是防止相关 cluster 随机漂到图的两端，而不是强行制造一个人为分组。

---

## 5. 覆盖 Family 颜色

默认情况下，脚本会从内置调色板里为每个 family 自动分配颜色。如果你希望某个 family 使用指定颜色，可以直接在词汇表文件里写：

```md
### Behavioral & Information {color=#8E24AA}
```

脚本会把这个颜色当作该 family 的基色，然后继续为 family 内各个 topic 生成相近色阶。例如，如果这个 family 下有 4 个 topic，它们可能会得到从浅紫到深紫的一组渐变色。

如果没有写 `{color=...}`，脚本就会按 family 在文件中出现的顺序自动分配颜色。

---

## 6. 修改节点语义

默认的视觉编码规则如下：

| 视觉属性 | 由什么决定 |
|----------------|-----------|
| 节点 **颜色** | `primary_topics` 的第一个条目（先映射到 family，再映射到该 family 下的色阶） |
| 节点 **大小** | `role` —— gatekeeper > active > emerging > peripheral |
| 金色 **边框** | `role == "gatekeeper"` |
| **边** 是否显示 | 仅显示那些在 vault 中也有 scholar note 的 coauthor |
| 边的 **粗细** | 合作论文数量（`coauthor_papers`） |
| **隐藏边** | 同 topic glue + 同 family glue（只用于布局，不可见） |

如果你想修改其中任意一项，`scholar_network.py` 里对应的位置是：

- `ROLE_SIZES` 字典 —— 把 role 名称映射到像素大小
- `build_graph()` 函数 —— 构造节点、可见边和隐藏 glue 边
- `build_graph()` 里的 tooltip HTML 拼接逻辑 —— 控制鼠标悬停时显示什么内容

---

## 7. 让示例数据和你的真实数据分离

`examples/` 文件夹是文档示例 —— 用来展示什么样的 scholar note 才算格式正确。它 **不是** 你的脚本实际读取的数据集。

你真实的 scholar notes 应该放在：

```
<your vault>/Scholars/*.md
```

这种分离方式的好处是：你可以公开发布这个 repo，而不会强迫用户把你的示例学者一并继承到他们自己的图谱里。如果你想试用这些示例，请手动把它们复制到你自己的 vault 的 `Scholars/` 文件夹中。
