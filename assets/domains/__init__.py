"""
业务域专家库注册表

每个业务域一个专家库文件，统一导出 DOMAIN 字典：
    DOMAIN = {
        'id': 'eam',                    # 领域ID（kebab-case）
        'name': '设备资产管理',           # 领域名称
        'keywords': [...],              # 触发关键词（用户描述中识别）
        'modules': [...],               # 模块/子项/问题结构
        'resources': [...],             # 资料索取清单
        'usage': [...],                 # 使用说明
        'summary_dims': [...],          # 调研总结维度
        'interview_topics': [...],      # 高层访谈主题
        'it_systems': [...],            # IT系统清单
        'data_flows': [...],            # 数据接口
        'reports': [...],               # 标准报表
        'attending_dept': '...',        # 建议参会部门
        'overview': '...',              # 总体概述
    }

模块格式：
    modules = [
        {
            'sec_num': '5.1',
            'name': '模块名',
            'intro': '模块简介',
            'subs': [
                ('子项名', [q_item, ...]),  # q_item: {idx, level, q, follow, need}
            ],
        },
    ]

新增专家库步骤：
1. 复制 domains/_template.py 为 domains/<your_domain>.py
2. 按模板填写 DOMAIN 字典
3. 在 DOMAIN_REGISTRY 中注册（本文件）
"""

import importlib
import os

# ============================================================
# 领域注册表：id → 模块名
# ============================================================
DOMAIN_REGISTRY = {
    'eam': 'eam',                # 设备资产管理（280条）
    'finance': 'finance',        # 财务与会计
    'quality': 'quality',        # 质量管理
    'procurement': 'procurement',  # 采购与供应商管理
}


def load_domain(domain_id):
    """
    加载指定领域专家库。

    参数：
        domain_id: 领域ID（见 DOMAIN_REGISTRY）

    返回：
        DOMAIN 字典

    异常：
        ValueError: 领域未注册
    """
    if domain_id not in DOMAIN_REGISTRY:
        raise ValueError(
            f'未注册的领域: {domain_id}。可用领域: {list(DOMAIN_REGISTRY.keys())}'
        )

    module_name = DOMAIN_REGISTRY[domain_id]
    module = importlib.import_module(f'domains.{module_name}')
    return module.DOMAIN


def match_domain(user_input):
    """
    根据用户描述匹配最合适的领域。

    参数：
        user_input: 用户对调研范围的描述

    返回：
        (domain_id, DOMAIN) 或 (None, None) 表示未匹配
    """
    best_domain = None
    best_score = 0

    for domain_id in DOMAIN_REGISTRY:
        try:
            domain = load_domain(domain_id)
        except Exception:
            continue

        score = 0
        for kw in domain.get('keywords', []):
            if kw in user_input:
                score += 1
        if score > best_score:
            best_score = score
            best_domain = (domain_id, domain)

    if best_score > 0:
        return best_domain
    return None, None


def list_domains():
    """列出所有已注册领域"""
    result = []
    for domain_id in DOMAIN_REGISTRY:
        try:
            domain = load_domain(domain_id)
            result.append({
                'id': domain_id,
                'name': domain.get('name', domain_id),
                'keywords': domain.get('keywords', []),
                'module_count': len(domain.get('modules', [])),
                'question_count': sum(
                    len(qs) for m in domain.get('modules', [])
                    for _, qs in m.get('subs', [])
                ),
            })
        except Exception as e:
            result.append({'id': domain_id, 'name': domain_id, 'error': str(e)})
    return result