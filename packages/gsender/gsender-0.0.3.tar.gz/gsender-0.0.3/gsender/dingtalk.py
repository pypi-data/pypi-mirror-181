"""
    钉钉群聊机器人

    学习链接：https://open.dingtalk.com/document/group/message-types-and-data-format#topic-2098229

    示例：
        d = DingTalkSender(secret=DING_TALK_SECRET, access_token=DING_TALK_ACCESS_TOKEN)
        d.send_text(content='测试消息', at_all=True)
        d.send_text(content='测试消息', at_mobiles='xxx')
        d.send_markdown(title='test', text='测试消息')
        d.send_link(title='test', text='测试消息', message_url="https://www.baidu.com/")
        d.send_feed_card(links=[
            {
                "title": "时代的火车向前开1",
                "messageURL": "https://www.dingtalk.com/",
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            },
            {
                "title": "时代的火车向前开2",
                "messageURL": "https://www.dingtalk.com/",
                "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png"
            }
        ])
        d.send_action_card_only(**{
            "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
            "text": "![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png) \n\n #### 乔布斯 20 年前想打造的苹果咖啡厅 \n\n Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划",
            "btn_orientation": 0,
            "btns": [
                {
                    "title": "内容不错",
                    "actionURL": "https://www.dingtalk.com/"
                },
                {
                    "title": "不感兴趣",
                    "actionURL": "https://www.dingtalk.com/"
                }
            ]
        })
"""
import hmac
import time
import base64
import hashlib
import requests
from loguru import logger
from typing import Union, List
from urllib.parse import quote


class DingTalkSender:
    """
        钉钉群聊机器人
    """

    def __init__(self, secret: str, access_token: str):
        """

        :param secret: 加签
        :param access_token: webhook 链接内的 access_token
        """
        self.secret = secret
        self.url = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'

    def send(
            self,
            msg_type: str,
            content: dict,
            at_mobiles: Union[List[str], str] = None,
            at_userids: Union[List[str], str] = None,
            at_all: bool = False
    ) -> dict:
        """
        发送自定义消息

        :param msg_type: 消息类型
        :param content: 消息内容
        :param at_mobiles: @ 的手机号
        :param at_userids: @ 的 userid
        :param at_all: 是否 @ 所有人
        :return:
        """
        message = {'msgtype': msg_type}

        # 处理 @
        if at_all or at_mobiles or at_userids:
            message['at'] = {}
        if at_all:
            message['at']['isAtAll'] = at_all
        if at_mobiles:
            if isinstance(at_mobiles, str):
                at_mobiles = [at_mobiles]
            message['at']['atMobiles'] = at_mobiles
        if at_userids:
            if isinstance(at_userids, str):
                at_userids = [at_userids]
            message['at']['atUserIds'] = at_userids

        # 处理消息体
        message.update(content)

        # 发送消息
        try:
            resp = requests.post(self.url, params=self.sign, json=message)

            return resp.json()
        except Exception as e:
            logger.error(e)

    def send_text(
            self,
            content: str,
            at_mobiles: Union[List[str], str] = None,
            at_userids: Union[List[str], str] = None,
            at_all: bool = False
    ) -> dict:
        """
        发送文本消息

        :param content: 消息内容
        :param at_mobiles: @ 的手机号
        :param at_userids: @ 的 userid
        :param at_all: 是否 @ 所有人
        :return:
        """

        return self.send(
            msg_type='text',
            content={'text': {'content': content}},
            at_mobiles=at_mobiles,
            at_userids=at_userids,
            at_all=at_all
        )

    def send_markdown(
            self,
            title: str,
            text: str,
            at_mobiles: Union[List[str], str] = None,
            at_userids: Union[List[str], str] = None,
            at_all: bool = False
    ) -> dict:
        """
        发送 markdown 消息

        :param title: 消息标题
        :param text: 消息内容
        :param at_mobiles: @ 的手机号
        :param at_userids: @ 的 userid
        :param at_all: 是否 @ 所有人
        :return:
        """

        return self.send(
            msg_type='markdown',
            content={'markdown': {'title': title, 'text': text}},
            at_mobiles=at_mobiles,
            at_userids=at_userids,
            at_all=at_all
        )

    def send_link(
            self,
            title: str,
            text: str,
            message_url: str,
            pic_url: str = None,
            at_mobiles: Union[List[str], str] = None,
            at_userids: Union[List[str], str] = None,
            at_all: bool = False
    ) -> dict:
        """
        发送 link 消息

        :param title: 消息标题
        :param text: 消息内容
        :param pic_url: 图片链接
        :param message_url: 跳转的消息链接
        :param at_mobiles: @ 的手机号
        :param at_userids: @ 的 userid
        :param at_all: 是否 @ 所有人
        :return:
        """
        content = {'link': {'title': title, 'text': text, 'messageUrl': message_url}}

        if pic_url:
            content['link'].update({'picUrl': pic_url})

        return self.send(
            msg_type='link',
            content=content,
            at_mobiles=at_mobiles,
            at_userids=at_userids,
            at_all=at_all
        )

    def send_feed_card(
            self,
            links: List[dict],
            at_mobiles: Union[List[str], str] = None,
            at_userids: Union[List[str], str] = None,
            at_all: bool = False
    ) -> dict:
        """
        发送卡片消息

        :param links: [{'title':'', 'messageURL':'', 'picURL':''}] 形式的数据
        :param at_mobiles: @ 的手机号
        :param at_userids: @ 的 userid
        :param at_all: 是否 @ 所有人
        :return:
        """

        return self.send(
            msg_type='feedCard',
            content={'feedCard': {'links': links}},
            at_mobiles=at_mobiles,
            at_userids=at_userids,
            at_all=at_all
        )

    def send_action_card(
            self,
            title: str,
            text: str,
            single_title: str,
            single_url: str,
            at_mobiles: Union[List[str], str] = None,
            at_userids: Union[List[str], str] = None,
            at_all: bool = False
    ) -> dict:
        """
        发送 整体 跳转的 actionCard 消息

        :param title: 首屏会话透出的展示内容
        :param text: markdown 格式消息内容
        :param single_title: 单个按钮的标题
        :param single_url: 单个按钮的链接
        :param at_mobiles: @ 的手机号
        :param at_userids: @ 的 userid
        :param at_all: 是否 @ 所有人
        :return:
        """

        return self.send(
            msg_type='actionCard',
            content={
                'actionCard': {'title': title, 'text': text, 'singleTitle': single_title, 'singleURL': single_url}
            },
            at_mobiles=at_mobiles,
            at_userids=at_userids,
            at_all=at_all
        )

    def send_action_card_only(
            self,
            title: str,
            text: str,
            btn_orientation: Union[int, str],
            btns: List[dict],
            at_mobiles: Union[List[str], str] = None,
            at_userids: Union[List[str], str] = None,
            at_all: bool = False
    ) -> dict:
        """
        发送 独立 跳转的 actionCard 消息

        :param title: 首屏会话透出的展示内容
        :param text: markdown 格式消息内容
        :param btn_orientation: 按钮排序，0 竖直排序，1 横向排序
        :param btns: 按钮 [{'title':'', 'actionURL':''}] 形式
        :param at_mobiles: @ 的手机号
        :param at_userids: @ 的 userid
        :param at_all: 是否 @ 所有人
        :return:
        """

        return self.send(
            msg_type='actionCard',
            content={
                'actionCard': {'title': title, 'text': text, 'btnOrientation': str(btn_orientation), 'btns': btns}
            },
            at_mobiles=at_mobiles,
            at_userids=at_userids,
            at_all=at_all
        )

    @property
    def sign(self) -> dict:
        """

        :return: 返回 sign
        """
        timestamp = str(round(time.time() * 1000))
        secret_bytes = self.secret.encode()
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_bytes = string_to_sign.encode()
        hmac_code = hmac.new(secret_bytes, string_to_sign_bytes, digestmod=hashlib.sha256).digest()

        return {
            'timestamp': timestamp,
            'sign': quote(base64.b64encode(hmac_code))
        }
