---
name: business-survey-docx
description: 业务调研问卷 Word 文档生成，支持任意业务领域。当用户要求"生成调研问卷"、"做调研文档"、"写调研问题清单"、"业务调研问卷"、"EAM/设备调研"、"财务调研"、"质量调研"、"采购调研"、"MES调研"、"HR调研"等需要结构化问卷输出时触发。内置多业务域专家问题库（EAM/财务/质量/采购），未覆盖领域按专家方法论即时设计问题。不适用于PPT/Excel/纯文本问卷。
---

# Business Survey Docx 业务调研问卷生成

## 概述

将调研业务范围与调研对象转换为符合标准格式的 Word 调研问卷（.docx）。
支持**任意业务领域**：内置多领域专家问题库，未覆盖领域按专家方法论即时设计。

## 核心能力

1. **多领域专家库**：预置 EAM/财务/质量/采购 4 个领域专家问题库，直接输出高质量问卷
2. **任意范围支持**：未覆盖领域按 `references/question_design_methodology.md` 方法论即时设计问题
3. **统一文档格式**：所有领域输出相同结构的 docx（9章+5附录+签字栏）

## 文档结构（强制）

```
封面（项目名称 + 文档标题 + 项目信息表）
├─ 一、参会人员（建议涵盖+12行签到表）
├─ 二、调研说明（项目背景+调研目的+原则+提问分级）
├─ 三、调研目录（模块/业务领域/Q范围/问题数）
├─ 四、总体概述（核心定位+本次升级要点）
├─ 五、现状描述（按模块分组，含调研问题列表）
├─ 六、高层访谈（主题+访谈要点）
├─ 七、IT系统（系统名称+覆盖范围+使用部门）
├─ 八、数据接口（数据流向+接口方式）
├─ 九、标准报表（报表名称+内容+频率）
└─ 附录A：资料索取清单
   附录B：典型对象现场抽查
   附录C：痛点需求池
   附录D：调研总结维度
   附录E：使用说明
签字确认栏
```

## 单条问题格式（强制）

```
Q{n}  [必问/应问/深挖]  问题内容
    建议追问: 追问内容（斜体灰）
    需要查看/索取: 资料清单（斜体灰）
    答复: _______
```

- Q编号：加粗深蓝色（#1F4E79）
- 等级标签：必问红(#C00000) / 应问橙(#ED7D31) / 深挖绿(#70AD47)
- 追问和需要查看：斜体灰色(#595959)
- 答复行：红色加粗

## 工作流程

### Phase 1：识别业务领域

读取用户输入，识别：
1. **调研对象**：公司/项目名称
2. **业务范围**：模块/子项描述
3. **业务领域**：调用 `domains.match_domain(描述)` 识别

```python
from domains import match_domain, list_domains
domain_id, domain = match_domain('财务核算和预算管理')  # → ('finance', DOMAIN)
```

### Phase 2：选择问题来源

| 情况 | 处理方式 |
|---|---|
| **命中专家库** | 直接加载 `domains.load_domain(id)`，按需增删子项 |
| **未命中** | 按 `references/question_design_methodology.md` 方法论即时设计 |
| **部分命中** | 专家库为主，方法论补缺 |

先运行 `--list` 查看可用领域：
```bash
python scripts/example_usage.py --list
```

### Phase 3：构建配置并生成

```python
from domains import load_domain
from domain_to_config import domain_to_config
from build_survey_docx import generate_survey_docx

domain = load_domain('finance')
config = domain_to_config(domain, project_name='XX项目', customer='XX公司', date='20260812')
generate_survey_docx(config, 'output.docx')
```

### Phase 4：验证与输出

```bash
python scripts/verify_survey_docx.py --strict <output.docx>
```

验证内容：章节完整性（15/15）、Q编号连续性、问题总数、表格数、答复行数。
若验证失败，检查问题编号/章节/表格后重新生成。

## 资源目录

### assets/
- `domains/` - **多领域专家问题库**（核心）
  - `__init__.py` - 领域注册表（`load_domain` / `match_domain` / `list_domains`）
  - `_template.py` - 新领域专家库模板（复制即用）
  - `eam.py` - 设备资产管理（280条）
  - `finance.py` - 财务与会计（32条）
  - `quality.py` - 质量管理（27条）
  - `procurement.py` - 采购与供应商管理（25条）
- `domain_to_config.py` - **DOMAIN → config 转换器**

### scripts/
- `build_survey_docx.py` - **核心生成器**（通用，不依赖具体领域）
- `example_usage.py` - 多领域示例（--list / --domain / --all）
- `verify_survey_docx.py` - 验证脚本

### references/
- `config_schema.md` - config 字段定义
- `question_design_methodology.md` - **问题设计方法论**（未覆盖领域时使用）
- `eam_question_bank.md` - EAM 问题库说明（历史参考）

## 设计原则

1. **结构统一**：无论调研领域，文档结构强制 9+5+1
2. **问题分级**：必问/应问/深挖 三级颜色编码
3. **可填写**：每条问题预留"答复"行，便于现场填写
4. **可追溯**：资料索取清单 + 现场抽查表 + 痛点需求池 全流程可追溯
5. **签字闭环**：业务、IT、项目经理三方签字确认

## 扩展新领域

用户提出未覆盖领域时：
1. 按方法论（references/question_design_methodology.md）设计问题
2. 生成问卷后**沉淀为新专家库**：
   - 复制 `domains/_template.py` 为 `domains/<新领域>.py`
   - 填入 DOMAIN 字典
   - 在 `domains/__init__.py` 注册
3. 下次同类调研直接命中专家库

## 注意事项

- **不要修改**问题格式（Q[n] + [等级] + 问题 + 建议追问 + 需要查看 + 答复）
- **不要省略**章节（即使某些章节没有内容也要保留章节标题）
- **Q编号连续**：从 1 开始连续编号，跨子项不能跳号
- **签字栏**：至少包含甲方业务负责人 + 乙方项目经理
- **附录完整**：5个附录必须全部输出，资源清单不可省略