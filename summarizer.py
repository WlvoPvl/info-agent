"""
Claude 摘要生成模块
使用Claude API对抓取内容进行智能分析
"""
from anthropic import Anthropic
from typing import List, Dict
from config import ANTHROPIC_API_KEY, MAX_CONTENT_LENGTH


def get_client():
    """获取Claude客户端"""
    if not ANTHROPIC_API_KEY:
        raise ValueError("请设置 ANTHROPIC_API_KEY 环境变量")
    return Anthropic(api_key=ANTHROPIC_API_KEY)


def format_posts_for_summary(posts: List[Dict]) -> str:
    """
    格式化帖子列表用于Claude处理

    Args:
        posts: 帖子列表

    Returns:
        格式化后的文本
    """
    formatted = []
    for i, post in enumerate(posts, 1):
        source = post.get("source", "Unknown")
        title = post.get("title", "")
        score = post.get("score", 0)
        comments = post.get("comments", 0)
        url = post.get("url", "")
        subreddit = post.get("subreddit", "")

        if source == "Reddit":
            formatted.append(f"{i}. [r/{subreddit}] {title}\n   ⬆️ {score} | 💬 {comments}\n   🔗 {url}")
        else:
            formatted.append(f"{i}. [{source}] {title}\n   ⬆️ {score} | 💬 {comments}\n   🔗 {url}")

    return "\n\n".join(formatted)


def generate_summary(keyword: str, posts: List[Dict]) -> str:
    """
    生成智能摘要

    Args:
        keyword: 搜索关键词
        posts: 帖子列表

    Returns:
        摘要文本
    """
    if not posts:
        return f"未找到关于「{keyword}」的相关内容。请尝试其他关键词。"

    client = get_client()
    formatted_posts = format_posts_for_summary(posts)

    # 构建prompt
    prompt = f"""你是一个信息研究助手。用户正在研究主题「{keyword}」。

以下是收集到的相关帖子：

{formatted_posts}

请生成一份简洁的研究摘要，包含：

## 📊 整体趋势
（2-3句话描述整体趋势和热度）

## 🔥 热门观点
（列出3-5个主要观点或讨论焦点）

## 💡 关键洞察
（1-2个有价值的发现或建议）

## 📚 推荐阅读
（推荐2-3个最值得深入阅读的帖子，简述理由）

保持简洁专业，突出实用价值。"""

    # 调用Claude API
    message = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def generate_brief_summary(posts: List[Dict]) -> str:
    """
    生成简短摘要（用于快速预览）

    Args:
        posts: 帖子列表

    Returns:
        简短摘要
    """
    if not posts:
        return "暂无内容"

    client = get_client()

    # 构建简单摘要prompt
    titles = [p.get("title", "") for p in posts[:10]]
    titles_text = "\n".join(f"- {t}" for t in titles)

    prompt = f"""以下是从Hacker News和Reddit收集的热门帖子标题：

{titles_text}

请用1-2句话概括这些内容的共同主题和趋势。直接输出，不要额外说明。"""

    message = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


if __name__ == "__main__":
    # 测试
    print("测试摘要模块...")
    test_posts = [
        {"source": "HN", "title": "AI Agents are taking over", "score": 500, "comments": 200, "url": "https://example.com"},
        {"source": "Reddit", "subreddit": "MachineLearning", "title": "New Claude model released", "score": 300, "comments": 150, "url": "https://example.com"}
    ]

    summary = generate_summary("AI Agents", test_posts)
    print(summary)
