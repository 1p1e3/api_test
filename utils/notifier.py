import requests

from config.paths import REPORTS_DIR
from config.settings import Settings
from utils.logger import logger
from core.api_client import unauthorized_client

class Notifier:

    settings = Settings()

    def __init__(self):
        self.webhook_url = self.settings.FEISHU_WEBHOOK_URL

        if not self.webhook_url:
            logger.warning('未配置 WEBHOOK_URL, 跳过测试报告推送')
    

    def build_message(self, stats: dict, report_path: str) -> dict:
        total = stats.get('total', 0)
        passed = stats.get('passed', 0)
        failed = stats.get('failed', 0)
        errors = stats.get('error', 0)
        skipped = stats.get('skipped', 0)

        status = "🟢 全部通过" if failed == 0 and errors == 0 else "🔴 存在失败"

        text = f"""【接口自动化测试报告】- {self.settings.APP_ENV} 环境
        
状态：{status}
总计：{total}
通过：{passed}
失败：{failed}
错误：{errors}
跳过：{skipped}
报告：{report_path}
        """

        return {'msg_type': 'text', 'content': {'text': text}}


    def send_report(self, stats: dict, report_path: str):
        if not self.webhook_url:
            return
        
        try:
            message = self.build_message(stats, report_path)

            headers = {'Content-Type': 'application/json'}

            r = requests.post(url=self.webhook_url, headers=headers, json=message)

            if r.status_code == 200:
                logger.success(f'测试报告 {report_path} 推送成功')
            else:
                logger.error(f'测试报告 {report_path} 推送失败: {r.status_code} - {r.text}')
        except Exception as e:
            logger.error(f'测试报告 {report_path} 推送失败: {e}')