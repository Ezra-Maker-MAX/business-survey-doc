# 业务域专家问题库说明

本 skill 采用**多业务域专家库**架构：每个业务领域一个专家问题库文件，由该领域的专业视角设计问题，保证问题质量和覆盖度。

## 已内置领域

| 领域ID | 名称 | 模块数 | 问题数 | 覆盖范围 |
|---|---|---|---|---|
| `eam` | 设备资产管理 | 4 | 280 | 设备管理/TPM/备件/模具 + 工厂设施(厂房/动力/消防/环保/能源) |
| `finance` | 财务与会计 | 6 | 32 | 总账/应收应付/成本/固定资产/资金/预算 |
| `quality` | 质量管理 | 6 | 27 | 体系/来料/过程/成品/实验室/客诉追溯 |
| `procurement` | 采购与供应商管理 | 6 | 25 | 策略/供应商/寻源/执行/结算/分析 |

## 使用方式

```python
from domains import load_domain, match_domain, list_domains

# 1. 列出所有领域
list_domains()

# 2. 按ID加载专家库
domain = load_domain('finance')

# 3. 按用户描述自动匹配
domain_id, domain = match_domain('来料检验和SPC')  # → ('quality', DOMAIN)
```

## 领域专家库格式

每个库文件导出统一的 `DOMAIN` 字典：

```python
DOMAIN = {
    'id': 'eam',                    # 领域ID
    'name': '设备资产管理',           # 领域名称
    'keywords': [...],              # 触发关键词
    'overview': '...',              # 总体概述
    'attending_dept': '...',        # 建议参会部门
    'modules': [...],               # 模块/子项/问题
    'resources': [...],             # 资料索取清单
    'usage': [...],                 # 使用说明
    'summary_dims': [...],          # 调研总结维度
    'interview_topics': [...],      # 高层访谈主题
    'it_systems': [...],            # IT系统
    'data_flows': [...],            # 数据接口
    'reports': [...],               # 标准报表
}
```

## 扩展新领域

1. 复制 `domains/_template.py` 为 `domains/<新领域>.py`
2. 按模板填写 DOMAIN 字典（问题设计方法论见 `references/question_design_methodology.md`）
3. 在 `domains/__init__.py` 的 `DOMAIN_REGISTRY` 中注册
4. 自检：`python domains/<新领域>.py`

## 设计规范

- **每子项 3-8 条问题**，覆盖"对象/主数据/流程/数字化/指标/合规/痛点"维度
- **等级配比**：必问≈50%，应问≈30%，深挖≈20%
- **Q编号全局连续**（1,2,3...），跨子项不跳号
- **每条问题三件套**：问题 + 建议追问 + 需要查看/索取