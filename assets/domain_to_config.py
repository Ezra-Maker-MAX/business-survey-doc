"""
领域专家库 → 调研问卷 config 转换器

将 domains/ 下的 DOMAIN 字典转换为 generate_survey_docx 所需的 config。

用法：
    from domain_to_config import domain_to_config
    from domains import load_domain
    from build_survey_docx import generate_survey_docx

    domain = load_domain('finance')
    config = domain_to_config(domain, project_name='XX项目', customer='XX公司')
    generate_survey_docx(config, 'output.docx')
"""

from docx.shared import RGBColor


def domain_to_config(domain, project_name='XX项目', doc_number='',
                     version='V1.0', date='', customer='',
                     vendor='调研方', subtitle=None):
    """
    将领域专家库 DOMAIN 字典转换为 generate_survey_docx 的 config。

    参数：
        domain: 从 domains 加载的 DOMAIN 字典
        project_name: 项目名称
        doc_number: 文档编号（默认自动生成）
        version: 版本号
        date: 日期
        customer: 面向客户
        vendor: 编制方
        subtitle: 副标题（默认自动生成）

    返回：
        config 字典
    """
    domain_id = domain.get('id', 'domain')
    domain_name = domain.get('name', domain_id)

    if not doc_number:
        doc_number = f'{domain_id.upper()}_V{version.replace("V", "")}_{date.replace("-", "") or "20260812"}'
    if not subtitle:
        subtitle = f'（{version}｜{domain_name}）'

    # 计算问题总数
    total = sum(len(qs) for m in domain.get('modules', []) for _, qs in m['subs'])

    # 构建 info_rows
    info_rows = [
        ('项目名称', f'{project_name}({domain_name}调研)', '', ''),
        ('文档编号', doc_number, '', ''),
        ('版本', version, '日期', date or '2026-08-12'),
        ('编制方', vendor, '面向客户', customer),
        ('调研主题', f'{domain_name}业务现状调研', '', ''),
        ('调研范围', f"{len(domain.get('modules', []))} 大模块 / {total} 条调研问题", '', ''),
    ]

    # 构建 toc_items
    toc_items = []
    for m in domain.get('modules', []):
        sec = m['sec_num']
        # 收集该模块所有问题的idx
        qs = [q for _, qs_list in m['subs'] for q in qs_list]
        if not qs:
            continue
        q_min = min(q['idx'] for q in qs)
        q_max = max(q['idx'] for q in qs)
        q_range = f'Q{q_min}-Q{q_max}' if q_min != q_max else f'Q{q_min}'
        toc_items.append((f'模块{sec[2]}', m['name'], q_range, str(len(qs))))

        # 子项
        for sub_name, sub_qs in m['subs']:
            if not sub_qs:
                continue
            s_min = min(q['idx'] for q in sub_qs)
            s_max = max(q['idx'] for q in sub_qs)
            s_range = f'Q{s_min}-Q{s_max}' if s_min != s_max else f'Q{s_min}'
            toc_items.append((f'　{sec}.{m["subs"].index((sub_name, sub_qs)) + 1}',
                              sub_name, s_range, str(len(sub_qs))))

    # 构建 overview_items
    overview_items = [
        ([
            (f'{domain_name}', {'bold': True, 'color': RGBColor(0x1F, 0x4E, 0x79)}),
            (' 业务现状调研。', {}),
        ], True),
    ]
    if domain.get('overview'):
        overview_items.append(domain['overview'])
    overview_items.append(([
        ('本次调研覆盖', {'bold': True}),
        (f'{len(domain.get("modules", []))} 大模块:', {'bold': True}),
    ], True))
    for m in domain.get('modules', []):
        overview_items.append(([(
            f'  {m["sec_num"]} {m["name"]}：'
            + ' / '.join(sub_name for sub_name, _ in m['subs']),
            {})], True))

    # 构建 modules（转换为 generate_survey_docx 的格式）
    modules = []
    for m in domain.get('modules', []):
        modules.append({
            'sec_num': m['sec_num'],
            'name': m['name'],
            'intro': m.get('intro', ''),
            'subs': m['subs'],
        })

    # 默认 IT 系统/数据接口/报表（若领域未提供则给通用占位）
    it_systems = domain.get('it_systems') or [
        ('ERP系统', '', '', '', ''),
        ('MES系统', '', '', '', ''),
        ('其他', '', '', '', ''),
    ]
    data_flows = domain.get('data_flows') or [
        ('ERP ↔ MES', '', '', ''),
    ]
    reports = domain.get('reports') or [
        ('业务报表', '', '', ''),
    ]

    config = {
        'project_name': f'{project_name}({domain_name}调研)',
        'doc_title': f'{domain_name}调研问卷',
        'subtitle': subtitle,
        'info_rows': info_rows,
        'attending_dept': domain.get('attending_dept', '业务部门、IT部'),
        'project_context': domain.get('overview', ''),
        'toc_items': toc_items,
        'overview_items': overview_items,
        'modules': modules,
        'interview_topics': domain.get('interview_topics', [
            ('1', '战略定位', '业务在公司的战略定位？'),
            ('2', '数字化期望', '对数字化建设的期望？最希望解决什么问题？'),
        ]),
        'it_systems': it_systems,
        'data_flows': data_flows,
        'reports': reports,
        'resources': domain.get('resources', [
            (1, '制度文档', '业务管理制度', '高'),
        ]),
        'summary_dims': domain.get('summary_dims', [
            '1. 业务现状',
            '2. 核心痛点 TOP10',
            '3. 建设建议',
        ]),
        'usage': domain.get('usage', [
            ('调研项目', f'{domain_name}业务调研'),
            ('调研范围', f"{len(domain.get('modules', []))} 个模块"),
            ('调研原则', '先问现状,再看现场'),
        ]),
        'signers': [
            (f'{customer} 业务负责人', '', '', ''),
            (f'{customer} IT负责人', '', '', ''),
            (f'{vendor} 项目经理', '', '', ''),
        ],
    }
    return config


def build_config_from_domain(domain_id, **kwargs):
    """快捷方式：按领域ID加载并转换"""
    from domains import load_domain
    domain = load_domain(domain_id)
    return domain_to_config(domain, **kwargs)
