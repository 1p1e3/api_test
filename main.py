import argparse
from datetime import datetime
import os
import subprocess
import sys
import pytest
from config.paths import REPORTS_DIR, ROOT_DIR
from utils.clean_old_reports import clean_old_reports


def parse_args():
    parser = argparse.ArgumentParser(description='API 自动化测试运行器')
    parser.add_argument('--env', default='sit', choices=['dev', 'sit', 'uat', 'prod'],
                        help='运行环境 (default: sit)')
    parser.add_argument('-k', '--keyword', type=str, default='',help='按关键字过滤测试用例（传递给 pytest -k）')
    parser.add_argument('-m', '--marker', type=str, default='', help='按标记过滤测试用例（传递给 pytest -m）')
    parser.add_argument('--no-report', action='store_true', help='不生成 HTML 报告')
    return parser.parse_args()


def main():
    args = parse_args()
    os.environ['APP_ENV'] = args.env

    from config.settings import Settings
    settings = Settings()

    REPORTS_DIR.mkdir(exist_ok=True)

    from utils.logger import logger
    logger.info(f"🚀 启动自动化测试 | 环境: {args.env.upper()}")

    # 清理 7 天前的报告
    clean_old_reports()
    
    # 测试报告名称, 以当前年月日时分秒命名
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = f"reports/report_{now}.html"


    # 构建 pytest 命令
    cmd = [sys.executable, '-m', 'pytest']
    # 添加测试目录
    cmd.extend(['tests/'])
    # 添加 HTML 报告（除非禁用）
    if not args.no_report:
        cmd.extend([
            f'--html={report_file}',
            '--self-contained-html',
            f'--report-path={report_file}'
        ])
    # 添加过滤条件
    if args.keyword:
        cmd.extend(['-k', args.keyword])
    if args.marker:
        cmd.extend(['-m', args.marker])

    # 增加 verbosity
    cmd.append('-v')

    # 方式一 - pytest 官方执行 api
    # pytest.main([
    #     f'--html={report_file}',
    #     '--self-contained-html',
    #     f'--report-path={report_file}'
    # ])


    # 方式二 - 子进程执行
    try:
        result = subprocess.run(cmd, cwd=ROOT_DIR, check=False)
        exit_code = result.returncode
    except KeyboardInterrupt:
        logger.warning('测试被手动中断')
        exit_code = 130
    except Exception as e:
        logger.error(f'❌ pytest 执行异常: {e}')
        exit_code = 1

    logger.info('🏁 测试运行结束')
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
