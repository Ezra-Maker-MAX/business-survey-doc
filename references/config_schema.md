# config 配置 Schema

`generate_survey_docx(config, output_path)` 函数所需的完整配置结构。

## 配置字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `project_name` | str | ✓ | 项目名称，显示在封面 |
| `doc_title` | str | ✓ | 文档标题（如"业务调研问卷"） |
| `subtitle` | str | | 副标题（如"（V1.0｜范围说明）"） |
| `info_rows` | list | ✓ | 项目信息表行 `[(k1,v1,k2,v2), ...]` |
| `attending_dept` | str | ✓ | 参会部门描述 |
| `project_context` | str | ✓ | 项目背景段落 |
| `toc_items` | list | ✓ | 调研目录 `[(模块, 业务, Q范围, 问题数), ...]` |
| `overview_items` | list | ✓ | 总体概述段落 |
| `core_upgrade` | str | | 核心升级说明（红色突出） |
| `modules` | list | ✓ | 现状描述模块 |
| `interview_topics` | list | ✓ | 高层访谈主题 |
| `it_systems` | list | ✓ | IT系统列表 |
| `data_flows` | list | ✓ | 数据接口流向 |
| `reports` | list | ✓ | 标准报表列表 |
| `resources` | list | ✓ | 资料索取清单 |
| `summary_dims` | list | ✓ | 调研总结维度 |
| `usage` | list | ✓ | 使用说明 |
| `signers` | list | ✓ | 签字人列表 |

## 各字段详细格式

### `info_rows`
```python
[
    ('项目名称', 'XXX项目', '', ''),  # k2, v2 空表示单列合并
    ('版本', 'V1.0', '日期', '2026-08-12'),  # k2, v2 有值表示双列
]
```

### `toc_items`
```python
[
    ('模块一', '业务模块A', 'Q1-Q10', '10'),  # 主模块：mod 不以空格开头
    ('\u30001.1', '子项1', 'Q1-Q5', '5'),  # 子项：mod 以 \u3000 开头
]
```

### `overview_items`
```python
[
    "段落1（普通段落）",
    [("粗体", {"bold": True}), ("普通", {})],  # 混合段落
    ([("粗体", {"bold": True}), ("段落", {})], True),  # (parts, indent_first)
]
```

### `modules`（核心字段）
```python
[
    {
        'sec_num': '5.1',
        'name': '业务模块A',
        'intro': '模块简介段落...',
        'module_note_parts': [  # 可选：模块级特殊说明
            ('★ 升级说明:', {'bold': True, 'color': RGBColor(0xC0, 0x00, 0x00)}),
            ('说明内容', {}),
        ],
        'subs': [  # 子项列表
            ('子项名1', [q_item1, q_item2, ...]),
            ('子项名2', [q_item3, ...]),
        ],
        # 可选：仅对指定子项加灰色小注
        'sub_intro_for_index': 1,  # 1 表示第1个子项
        'sub_intro_for_text': '该子项的补充说明...',
    },
]
```

### `q_item` 单条问题格式
```python
{
    'idx': 1,             # 问题编号
    'level': '必问',       # '必问' / '应问' / '深挖'
    'q': '问题内容',
    'follow': '建议追问（可选）',
    'need': '需要查看/索取的资料（可选）',
}
```

### `interview_topics`
```python
[
    ('1', '战略定位', '战略定位的访谈要点...'),
    ('2', '业务协同', '...'),
]
```

### `it_systems`
```python
[
    ('系统名称1', '', '', '', ''),  # 仅第一列预填，后4列空
    ('系统名称2', '', '', '', ''),
]
```

### `data_flows`
```python
[
    ('系统A ↔ 系统B', '', '', ''),  # 仅第一列预填
]
```

### `reports`
```python
[('报表名称', '', '', ''), ...]
```

### `resources`
```python
[
    (1, '类别', '资料名称', '优先级'),  # 优先级: '高' / '中' / '低'
]
```

### `summary_dims`
```python
['1. 维度1', '2. 维度2', ...]
```

### `usage`
```python
[
    ('调研项目', 'XXX业务调研'),
    ('调研范围', 'X 个模块'),
    ('调研原则', '先问现状,再看现场'),
]
```

### `signers`
```python
[
    ('甲方 业务负责人', '', '', ''),
    ('乙方 项目经理', '', '', ''),
]
```

## 完整调用示例

```python
from build_survey_docx import generate_survey_docx

config = {
    'project_name': '亚新科NVH全球模板及ERP实施项目',
    'doc_title': '业务调研问卷',
    'subtitle': '（V1.0｜4模块20子项）',
    'info_rows': [...],
    'attending_dept': '设备部、生产部、IT部',
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

generate_survey_docx(config, '/path/to/output.docx')
```