"""
business-survey-docx skill 使用示例

演示如何调用 build_survey_docx.generate_survey_docx() 生成调研问卷。
"""

import os
import sys

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from build_survey_docx import generate_survey_docx


def example_minimal():
    """示例1：最简配置 - 手工指定少量问题"""

    config = {
        'project_name': 'XX公司ERP实施项目',
        'doc_title': '生产管理业务调研问卷',
        'subtitle': '（V1.0｜2模块）',
        'info_rows': [
            ('项目名称', 'XX公司ERP实施项目', '', ''),
            ('文档编号', 'XX_V1.0_20260812', '', ''),
            ('版本', 'V1.0', '日期', '2026-08-12'),
            ('编制方', '咨询方', '面向客户', 'XX公司'),
            ('调研主题', '生产管理业务现状', '', ''),
            ('调研范围', '2 模块 6 个子项 / 30 条问题', '', ''),
        ],
        'attending_dept': '生产部、计划部、车间主任',
        'project_context': (
            'XX公司ERP实施项目旨在通过数字化转型提升生产管理效率。'
            '本次调研重点了解生产计划、车间执行、工序管理三大业务的现状、'
            '问题与需求,为后续ERP-MES蓝图设计提供输入。'
        ),

        'toc_items': [
            ('模块一', '生产计划管理', 'Q1-Q15', '15'),
            ('　1.1', '主计划管理', 'Q1-Q8', '8'),
            ('　1.2', '物料需求计划', 'Q9-Q15', '7'),
            ('模块二', '车间执行管理', 'Q16-Q30', '15'),
            ('　2.1', '工单管理', 'Q16-Q22', '7'),
            ('　2.2', '工序报工', 'Q23-Q30', '8'),
        ],

        'overview_items': [
            '本次生产管理业务调研覆盖主计划、MRP、工单管理、工序报工四大子领域。',
            ([
                ('调研方法:', {'bold': True}),
                ('现场访谈 + 资料收集 + 系统演示,预计3个工作日完成。', {}),
            ], True),
        ],

        'modules': [
            {
                'sec_num': '5.1',
                'name': '生产计划管理',
                'intro': '生产计划是ERP/MES的核心,涵盖主生产计划(MPS)和物料需求计划(MRP)。',
                'subs': [
                    ('主计划管理', [
                        {'idx': 1, 'level': '必问', 'q': '主生产计划的编制频率和周期？计划周期长度？',
                         'follow': '计划变更的频次？', 'need': '主计划样例'},
                        {'idx': 2, 'level': '必问', 'q': '主计划的数据来源（订单/预测/库存）？',
                         'follow': '订单和预测的占比？', 'need': '数据源说明'},
                        {'idx': 3, 'level': '应问', 'q': '计划冻结区的设置规则？', 'need': '冻结规则文档'},
                        # ... 更多问题
                    ]),
                    ('物料需求计划', [
                        {'idx': 9, 'level': '必问', 'q': 'MRP计算的频率和逻辑？', 'need': 'MRP逻辑说明'},
                        {'idx': 10, 'level': '应问', 'q': 'MRP异常的处理流程？', 'need': '异常处理流程'},
                        # ...
                    ]),
                ],
            },
            {
                'sec_num': '5.2',
                'name': '车间执行管理',
                'intro': '车间执行包括工单下达、报工、完工入库等业务。',
                'subs': [
                    ('工单管理', [
                        {'idx': 16, 'level': '必问', 'q': '工单的下达、变更、关闭流程？', 'need': '工单流程文档'},
                        # ...
                    ]),
                ],
            },
        ],

        'interview_topics': [
            ('1', '战略定位', '生产管理在公司的战略定位...'),
            ('2', '数字化期望', '对MES系统的期望...'),
        ],

        'it_systems': [
            ('ERP系统', '', '', '', ''),
            ('MES系统', '', '', '', ''),
            ('WMS系统', '', '', '', ''),
        ],

        'data_flows': [
            ('ERP ↔ MES', '', '', ''),
            ('MES ↔ WMS', '', '', ''),
        ],

        'reports': [
            ('生产计划报表', '', '', ''),
            ('车间执行报表', '', '', ''),
        ],

        'resources': [
            (1, '生产计划', '主计划样例', '高'),
            (2, '工艺路线', '工艺路线文档', '高'),
        ],

        'summary_dims': [
            '1. 生产计划管理',
            '2. 车间执行管理',
            '3. 系统集成',
            '4. 核心痛点 TOP10',
        ],

        'usage': [
            ('调研项目', '生产管理业务调研'),
            ('调研范围', '2 模块 6 个子项'),
            ('调研原则', '先问现状,再看现场'),
        ],

        'signers': [
            ('甲方 业务负责人', '', '', ''),
            ('乙方 项目经理', '', '', ''),
        ],
    }

    output_path = '/tmp/example_minimal.docx'
    generate_survey_docx(config, output_path)
    print(f'生成成功: {output_path}')
    return output_path


def example_from_eam_data():
    """示例2：使用 V4.0 EAM 数据生成完整文档"""

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'assets'))
    from eam_v4_data import EAM_V4_CONFIG_SKELETON, FACTORY_QS_ORGANIZED

    # V3.0 设备问题加载（这里仅演示结构，实际需要从 xlsx 加载155条）
    # 此处仅用工厂设施125条作为演示
    factory_questions = []
    idx = 156  # 工厂设施问题从156开始
    for sub_full, qs_list in FACTORY_QS_ORGANIZED.items():
        for orig_idx, sub_sub, level, q, follow, need in qs_list:
            factory_questions.append({
                'idx': idx,
                'level': level,
                'q': q,
                'follow': follow,
                'need': need,
            })
            idx += 1

    # 构建 1.7 工厂设施模块
    factory_modules = []
    factory_sub_groups = {}
    for q in factory_questions:
        # 提取二级子项代码
        # 简化：每个FACTORY_QS_ORGANIZED的key作为子项
        pass

    # 简化为示例演示
    config = dict(EAM_V4_CONFIG_SKELETON)
    # modules 需要根据完整问题构建（详见 build_doc_v4.py 完整脚本）

    print('请参考 /sandbox/workspace/nvh_survey/build_doc_v4.py 查看完整的V4.0文档生成逻辑')
    print('本示例仅展示配置结构，不实际运行（需要V3.0设备问题数据）')


if __name__ == '__main__':
    print('=== 示例1：最小配置 ===')
    example_minimal()

    print()
    print('=== 示例2：V4.0 EAM 数据（需要完整数据） ===')
    example_from_eam_data()