"""
业务域专家库模板（新领域扩展时复制本文件为 <domain>.py）

使用步骤：
1. 复制本文件: cp _template.py your_domain.py
2. 填写 DOMAIN 字典（见下方注释）
3. 在 __init__.py 的 DOMAIN_REGISTRY 中注册: 'your_domain': 'your_domain'
4. 验证: python -c "from domains import load_domain; d = load_domain('your_domain'); print(len(d['modules']))"
"""

DOMAIN = {
    # ---- 必填：基础信息 ----
    'id': 'your_domain',          # 领域ID（kebab-case，与文件名一致）
    'name': '您的业务领域名称',     # 如"财务管理"、"人力资源管理"
    'keywords': [                  # 触发关键词（用户描述中包含即命中）
        '财务', '会计', '总账', '预算',
    ],
    'overview': (
        '领域背景描述：用于"四、总体概述"章节，说明该领域的业务范围与调研价值。'
    ),
    'attending_dept': '建议参会的部门列表',

    # ---- 必填：模块结构（1-N个模块，每个模块1-N个子项）----
    # 问题数量建议：每子项 3-8 条，覆盖"台账/流程/数字化/指标/合规/痛点"维度
    'modules': [
        {
            'sec_num': '5.1',       # 章节号（5.1开始，模块递增）
            'name': '模块一名称',     # 如"总账管理"
            'intro': '模块简介段落（用于五、现状描述）',
            'subs': [
                # ('子项名', [q_item, ...])
                # q_item: {'idx': 全局连续编号, 'level': 必问/应问/深挖,
                #          'q': 问题, 'follow': 建议追问, 'need': 需要查看/索取}
                ('子项1', [
                    {'idx': 1, 'level': '必问', 'q': '问题内容？',
                     'follow': '追问内容？', 'need': '需要查看的资料'},
                    {'idx': 2, 'level': '应问', 'q': '问题内容？',
                     'follow': '', 'need': ''},
                ]),
                ('子项2', [
                    {'idx': 3, 'level': '深挖', 'q': '问题内容？',
                     'follow': '', 'need': ''},
                ]),
            ],
        },
    ],

    # ---- 必填：资料索取清单 ----
    # (序号, 类别, 资料名称, 优先级) 优先级: 高/中/低
    'resources': [
        (1, '类别A', '资料名称', '高'),
        (2, '类别B', '资料名称', '中'),
    ],

    # ---- 必填：使用说明 ----
    # (项目, 说明)
    'usage': [
        ('调研项目', 'XX业务调研'),
        ('调研范围', 'N 个模块'),
        ('调研原则', '先问现状,再看现场'),
    ],

    # ---- 必填：调研总结维度 ----
    'summary_dims': [
        '1. 维度一',
        '2. 维度二',
        '3. 核心痛点 TOP10',
    ],

    # ---- 必填：高层访谈主题 ----
    # (序号, 主题, 访谈要点)
    'interview_topics': [
        ('1', '战略定位', '业务在公司的战略定位...'),
    ],

    # ---- 可选：IT系统 / 数据接口 / 标准报表 ----
    'it_systems': [
        ('系统名称', '', '', '', ''),
    ],
    'data_flows': [
        ('系统A ↔ 系统B', '', '', ''),
    ],
    'reports': [
        ('报表名称', '', '', ''),
    ],
}

if __name__ == '__main__':
    # 自检
    total = sum(len(qs) for m in DOMAIN['modules'] for _, qs in m['subs'])
    print(f"领域: {DOMAIN['name']} ({DOMAIN['id']})")
    print(f"模块数: {len(DOMAIN['modules'])}")
    print(f"问题总数: {total}")
    # 检查编号连续性
    idxs = [q['idx'] for m in DOMAIN['modules'] for _, qs in m['subs'] for q in qs]
    if idxs and idxs != list(range(1, max(idxs) + 1)):
        print(f"⚠️ Q编号不连续: {idxs}")