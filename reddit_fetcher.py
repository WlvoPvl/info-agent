"""
Reddit 抓取模块
使用Reddit API获取相关帖子
"""
import requests
from typing import List, Dict
from config import MAX_POSTS_PER_SOURCE, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT


def search_reddit(keyword: str, limit: int = MAX_POSTS_PER_SOURCE) -> List[Dict]:
    """
    搜索Reddit帖子

    Args:
        keyword: 搜索关键词
        limit: 返回数量限制

    Returns:
        匹配的帖子列表
    """
    # 使用Reddit搜索API (不需要认证的公开端点)
    url = "https://www.reddit.com/search.json"
    params = {
        "q": keyword,
        "limit": limit,
        "sort": "relevance",
        "t": "week"  # 过去一周
    }
    headers = {
        "User-Agent": REDDIT_USER_AGENT
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Reddit API错误: {e}")
        return []

    results = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        results.append({
            "source": "Reddit",
            "subreddit": post.get("subreddit", ""),
            "title": post.get("title", ""),
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "score": post.get("score", 0),
            "comments": post.get("num_comments", 0),
            "author": post.get("author", ""),
            "selftext": post.get("selftext", "")[:500]  # 截取正文
        })

    return results


def get_subreddit_hot(subreddit: str, limit: int = MAX_POSTS_PER_SOURCE) -> List[Dict]:
    """
    获取指定subreddit的热门帖子

    Args:
        subreddit: 子版块名称
        limit: 返回数量

    Returns:
        热门帖子列表
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": limit}
    headers = {
        "User-Agent": REDDIT_USER_AGENT
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Reddit API错误: {e}")
        return []

    results = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        results.append({
            "source": "Reddit",
            "subreddit": post.get("subreddit", ""),
            "title": post.get("title", ""),
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "score": post.get("score", 0),
            "comments": post.get("num_comments", 0),
            "author": post.get("author", ""),
            "selftext": post.get("selftext", "")[:500]
        })

    return results


if __name__ == "__main__":
    # 测试
    print("测试Reddit模块...")
    results = search_reddit("AI agent", 5)
    for post in results:
        print(f"[r/{post['subreddit']}] [{post['score']}] {post['title']}")
