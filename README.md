# business-survey-docx

业务调研问卷 Word 文档生成 Skill。

## 功能

根据调研业务范围与调研对象，自动生成符合标准格式的 Word 调研问卷（.docx）。

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

## 快速开始

```python
from scripts.build_survey_docx import generate_survey_docx

config = {
    'project_name': 'XXX项目',
    'doc_title': '业务调研问卷',
    'info_rows': [...],
    'attending_dept': '...',
    'project_context': '...',
    'toc_items': [...],
    'overview_items': [...],
    'modules': [...],
    'interview_topics': [...],
    'it_systems': [...],
    'data_flows': [...],
    'reports': [...],
    'resources': [...],
    'summary_dims': [...],
    'usage': [...],
    'signers': [...],
}

generate_survey_docx(config, 'output.docx')
```

详细 config 字段定义见 [`references/config_schema.md`](references/config_schema.md)。

## 适用领域

- EAM/设备管理调研
- MES/生产管理调研
- WMS/仓库管理调研
- QMS/质量管理调研
- 其他通用业务调研

## 资源

- `scripts/build_survey_docx.py` - 核心生成器
- `scripts/example_usage.py` - 使用示例（--all / --eam）
- `scripts/verify_survey_docx.py` - 验证脚本（章节/Q编号/表格完整性）
- `references/config_schema.md` - 配置 Schema
- `references/eam_question_bank.md` - EAM 问题库说明
- `assets/eam_v4_data.py` - 完整 EAM 问题库（280条）+ `build_eam_v4_config()` 构建函数

## 快速体验

```bash
# 生成 EAM V4.0 完整版（280条问题）
python scripts/example_usage.py --eam

# 验证生成的文档
python scripts/verify_survey_docx.py --strict output/example_eam_v4_survey.docx
```

## 依赖

- python-docx

```bash
pip install python-docx
```