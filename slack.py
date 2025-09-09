import requests

from database import Databases
from envs import environments as envs

db = Databases()


def send_slack_message(text: str) -> None:
    """
    TODO: 오전 10시 마다 웹축 알림 추가 예정
    slack 알림 기능 Webhook
    """
    requests.post(envs.SLACK_WEBHOOK_URL, json={"text": text})


if __name__ == "__main__":
    # DB에서 키워드 가져오기 (최대 10개)
    rows = db.execute("SELECT keyword FROM naver_fashion LIMIT 10")

    # 튜플에서 값만 꺼내기
    if rows is None:
        today_keywords = []
    else:
        today_keywords = [row[0] for row in rows]

    # TODO: 생활/건강 카테고리도 추가 예정
    # 메시지 만들기
    msg = "📊 [패션의류 인기 키워드 Top 10]\n" + "\n".join(
        [f"{i+1}. {kw}" for i, kw in enumerate(today_keywords)]
    )

    # Slack 전송
    send_slack_message(msg)
