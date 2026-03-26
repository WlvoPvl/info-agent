"""
Info Research Agent MVP
多平台信息聚合 + AI智能摘要
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 配置
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "InfoResearchAgent/1.0")

# HN API
HN_BASE_URL = "https://hacker-news.firebaseio.com/v0"

# 限制
MAX_POSTS_PER_SOURCE = 10
MAX_CONTENT_LENGTH = 50000
