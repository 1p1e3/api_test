from datetime import datetime, timedelta

from config.paths import REPORTS_DIR
from utils.logger import logger

def clean_old_reports(days=7):
    REPORTS_DIR.mkdir(exist_ok=True)
    now = datetime.now()
    cutoff_date = now - timedelta(days=days)

    logger.info(f'--- 正在清理 {days} 天前的旧报告 ---')
    for report in REPORTS_DIR.glob('*.html'):
        file_mtime = datetime.fromtimestamp(report.stat().st_mtime)

        if file_mtime < cutoff_date:
            try:
                report.unlink()
                logger.success(f'已删除过期报告: {report.name} (修改时间: {file_mtime.strftime('%Y-%m-%d')})')
            except Exception as e:
                logger.error(f'无法删除 {report.name}: {e}')
    logger.info('--- 旧报告清理完成 ---\n')
