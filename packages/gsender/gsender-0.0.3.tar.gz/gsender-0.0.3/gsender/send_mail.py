"""
    邮件发送

    示例：
        sender = EmailSender(user='xxx', pwd='xxx')
        sender.send(receiver='', content_text='这是一封测试邮件')

    注意：
        需要邮箱授权码，具体百度
"""
import zmail
from loguru import logger
from typing import Union, List


class EmailSender:
    """
        邮件发送器
    """

    def __init__(self, user: str, pwd: str, **kwargs):
        self.user = user
        self.server = zmail.server(username=user, password=pwd, **kwargs)

    def send(
            self,
            receiver: Union[List[str], str],
            subject: str = 'Palp 报警系统',
            content_text: str = None,
            content_html: Union[List[str], str] = None,
            files: Union[List[str], str] = None,
            headers: dict = None
    ):
        """
        发送邮件

        :param receiver: 接收者
        :param subject: 主体
        :param content_text: 文本内容
        :param content_html: html 内容
        :param files: 文件路径或路径列表
        :param headers: 额外标题
        :return:
        """
        if isinstance(receiver, str):
            receiver = [receiver]

        mail = {'subject': subject, 'from': f'Palp <{self.user}>'}

        if content_text:
            mail.update({'content_text': content_text})

        if content_html:
            if isinstance(content_html, str):
                content_html = [content_html]
            mail.update({'content_html': content_html})

        if files:
            if isinstance(files, str):
                files = [files]
            mail.update({'attachments': files})

        if headers:
            mail.update({'headers': headers})

        try:
            return self.server.send_mail(recipients=receiver, mail=mail, auto_add_from=False)
        except Exception as e:
            logger.error(e)
            return False

    def check_availability(self):
        """
        获取邮箱状态，尝试是否可用

        :return:
        """
        try:
            self.server.stat()
        except:
            raise Exception('邮件服务不可用，请检查账号、授权码！')
