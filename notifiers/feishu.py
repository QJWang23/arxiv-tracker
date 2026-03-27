import requests
from typing import Dict, Optional
import os


def build_instant_card(item: dict, report_url: str) -> dict:
    """Build Feishu message card for instant push."""
    title = item.get("title", "Unknown Title")
    summary = item.get("summary", "")[:200] + "..." if len(item.get("summary", "")) > 200 else item.get("summary", "")
    heat_score = item.get("heat_score", 0)

    return {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "🚀 论文即时推送"},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**{title}**\n\n{summary}\n\n🔥 热度: {heat_score}"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "查看详情"},
                            "url": report_url,
                            "type": "primary"
                        }
                    ]
                }
            ]
        }
    }


def build_weekly_card(stats: dict, report_url: str) -> dict:
    """Build Feishu message card for weekly summary."""
    total = stats.get("total", 0)
    categories = stats.get("categories", {})

    cat_text = "\n".join([f"- **{k}**: {v} 篇" for k, v in categories.items()])

    return {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "📊 本周论文汇总"},
                "template": "green"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**本周共收录 {total} 篇论文**\n\n{cat_text}"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "查看完整报告"},
                            "url": report_url,
                            "type": "primary"
                        }
                    ]
                }
            ]
        }
    }


def send_to_feishu(card: dict, webhook_url: Optional[str] = None) -> bool:
    """Send message card to Feishu webhook."""
    webhook_url = webhook_url or os.environ.get("FEISHU_WEBHOOK_URL")
    if not webhook_url:
        print("Warning: No Feishu webhook URL configured")
        return False

    try:
        response = requests.post(
            webhook_url,
            json=card,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed to send to Feishu: {e}")
        return False
