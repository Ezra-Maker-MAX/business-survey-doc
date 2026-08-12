"""
business-survey-docx skill 使用示例

演示多业务域专家库的调用方式。

运行方式（从 scripts 目录）:
    python example_usage.py                 # 查看帮助
    python example_usage.py --list          # 列出可用领域
    python example_usage.py --domain eam    # 生成EAM问卷
    python example_usage.py --domain finance  # 生成财务问卷
    python example_usage.py --all           # 生成所有领域问卷
"""

import argparse
import os
import sys

# 添加 scripts / assets 目录到路径
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, _SCRIPT_DIR)
sys.path.insert(0, os.path.join(_SKILL_DIR, 'assets'))

from build_survey_docx import generate_survey_docx


def generate_by_domain(domain_id, output_path=None, project_name='XX项目', customer='XX公司'):
    """按领域专家库生成调研问卷"""
    from domains import load_domain
    from domain_to_config import domain_to_config

    domain = load_domain(domain_id)
    config = domain_to_config(domain, project_name=project_name, customer=customer,
                              date='20260812')

    if output_path is None:
        output_path = os.path.join(_SKILL_DIR, 'output', f'example_{domain_id}_survey.docx')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generate_survey_docx(config, output_path)
    return output_path, config


def verify_output(output_path):
    """生成后校验"""
    from verify_survey_docx import verify_survey_docx
    ok, report = verify_survey_docx(output_path)
    for line in report:
        print(f'    {line}')
    return ok


def main():
    parser = argparse.ArgumentParser(description='business-survey-docx 多领域示例')
    parser.add_argument('--list', action='store_true', help='列出可用领域')
    parser.add_argument('--domain', type=str, default=None, help='指定领域ID生成问卷')
    parser.add_argument('--all', action='store_true', help='生成所有领域问卷')
    parser.add_argument('--project', type=str, default='XX项目', help='项目名称')
    parser.add_argument('--customer', type=str, default='XX公司', help='面向客户')
    args = parser.parse_args()

    if args.list:
        from domains import list_domains
        print('可用领域专家库：')
        for d in list_domains():
            print(f'  - {d["id"]:12s} {d["name"]} (模块:{d["module_count"]}, 问题:{d["question_count"]})')
        print()
        print('按方法论即时设计新领域：阅读 references/question_design_methodology.md')
        return

    if args.domain:
        print(f'=== 生成 {args.domain} 领域调研问卷 ===')
        path, config = generate_by_domain(args.domain, project_name=args.project, customer=args.customer)
        print(f'✅ 生成成功: {path}')
        print(f'   问题总数: {sum(len(qs) for m in config["modules"] for _, qs in m["subs"])}')
        print()
        print('=== 验证 ===')
        verify_output(path)
        return

    if args.all:
        from domains import DOMAIN_REGISTRY
        for did in DOMAIN_REGISTRY:
            print(f'=== {did} ===')
            path, config = generate_by_domain(did, project_name=args.project, customer=args.customer)
            print(f'✅ 生成成功: {path}')
            verify_output(path)
            print()
        return

    print(__doc__)


if __name__ == '__main__':
    main()