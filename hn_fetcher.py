"""
Hacker News 抓取模块
使用HN官方API获取热门帖子
"""
import requests
from typing import List, Dict
from config import HN_BASE_URL, MAX_POSTS_PER_SOURCE


def get_top_stories(limit: int = MAX_POSTS_PER_SOURCE) -> List[int]:
    """获取热门故事ID列表"""
    url = f"{HN_BASE_URL}/topstories.json"
    response = requests.get(url)
    return response.json()[:limit]


def get_story_details(story_id: int) -> Dict:
    """获取单个故事详情"""
    url = f"{HN_BASE_URL}/item/{story_id}.json"
    response = requests.get(url)
    return response.json()


def search_hn(keyword: str, limit: int = MAX_POSTS_PER_SOURCE) -> List[Dict]:
    """
    搜索HN帖子（基于关键词过滤热门帖子）

    Args:
        keyword: 搜索关键词
        limit: 返回数量限制

    Returns:
        匹配的帖子列表
    """
    # 获取热门帖子
    story_ids = get_top_stories(limit * 3)  # 获取更多用于过滤

    results = []
    keyword_lower = keyword.lower()

    for story_id in story_ids:
        story = get_story_details(story_id)
        if not story:
            continue

        title = story.get("title", "").lower()

        # 关键词匹配
        if keyword_lower in title:
            results.append({
                "source": "Hacker News",
                "title": story.get("title", ""),
                "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                "score": story.get("score", 0),
                "comments": story.get("descendants", 0),
                "id": story_id
            })

        if len(results) >= limit:
            break

    return results


def get_trending(limit: int = MAX_POSTS_PER_SOURCE) -> List[Dict]:
    """
    获取HN热门帖子

    Args:
        limit: 返回数量

    Returns:
        热门帖子列表
    """
    story_ids = get_top_stories(limit)

    results = []
    for story_id in story_ids:
        story = get_story_details(story_id)
        if story:
            results.append({
                "source": "Hacker News",
                "title": story.get("title", ""),
                "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                "score": story.get("score", 0),
                "comments": story.get("descendants", 0),
                "id": story_id
            })

    return results


if __name__ == "__main__":
    # 测试
    print("测试HN模块...")
    trending = get_trending(5)
    for post in trending:
        print(f"[{post['score']}] {post['title']}")
