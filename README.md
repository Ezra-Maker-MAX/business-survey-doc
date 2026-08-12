# business-survey-docx

业务调研问卷 Word 文档生成 Skill —— 支持**任意业务领域**。

## 功能

根据调研业务范围与调研对象，自动生成符合标准格式的 Word 调研问卷（.docx）。
内置**多业务域专家问题库**（EAM/财务/质量/采购），未覆盖领域按专家方法论即时设计问题。

## 文档结构

```
封面 + 项目信息表
├─ 一、参会人员
├─ 二、调研说明
├─ 三、调研目录
├─ 四、总体概述
├─ 五、现状描述（按业务模块分组）
├─ 六、高层访谈
├─ 七、IT系统
├─ 八、数据接口
├─ 九、标准报表
└─ 附录A-E：资料索取/现场抽查/痛点/总结/使用说明
签字确认栏
```

## 内置领域专家库

| 领域ID | 名称 | 问题数 | 覆盖范围 |
|---|---|---|---|
| `eam` | 设备资产管理 | 280 | 设备/TPM/备件/模具 + 工厂设施 |
| `finance` | 财务与会计 | 32 | 总账/应收应付/成本/资产/资金/预算 |
| `quality` | 质量管理 | 27 | 体系/来料/过程/成品/实验室/追溯 |
| `procurement` | 采购与供应商管理 | 25 | 策略/供应商/寻源/执行/结算/分析 |

## 快速开始

```bash
# 列出可用领域
python scripts/example_usage.py --list

# 生成指定领域问卷
python scripts/example_usage.py --domain finance --project "XX项目" --customer "XX公司"

# 生成所有领域
python scripts/example_usage.py --all
```

### 代码调用

```python
from domains import load_domain
from domain_to_config import domain_to_config
from build_survey_docx import generate_survey_docx

domain = load_domain('eam')
config = domain_to_config(domain, project_name='XX项目', customer='XX公司', date='20260812')
generate_survey_docx(config, 'output.docx')

# 验证
python scripts/verify_survey_docx.py --strict output.docx
```

## 扩展新领域

未覆盖领域（如 HR、供应链、销售等）：
1. 按 `references/question_design_methodology.md` 方法论即时设计问题
2. 沉淀为新专家库：复制 `assets/domains/_template.py` → 填写 DOMAIN → 在 `__init__.py` 注册

## 资源

```
assets/
├── domains/              # 多领域专家问题库（核心）
│   ├── __init__.py       # 注册表：load_domain / match_domain / list_domains
│   ├── _template.py      # 新领域模板
│   ├── eam.py            # 设备资产管理（280条）
│   ├── finance.py        # 财务与会计（32条）
│   ├── quality.py        # 质量管理（27条）
│   └── procurement.py    # 采购与供应商管理（25条）
└── domain_to_config.py   # DOMAIN → config 转换器

scripts/
├── build_survey_docx.py  # 核心生成器
├── example_usage.py      # 多领域示例
└── verify_survey_docx.py # 验证脚本

references/
├── config_schema.md                  # 配置 Schema
├── question_design_methodology.md    # 问题设计方法论
└── eam_question_bank.md              # 领域专家库说明
```

## 依赖

```bash
pip install python-docx
```