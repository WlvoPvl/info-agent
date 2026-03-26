"""
Info Research Agent MVP
信息聚合 + AI智能摘要

运行: streamlit run app.py
"""
import streamlit as st
from datetime import datetime
from typing import List, Dict

from config import MAX_POSTS_PER_SOURCE
from hn_fetcher import search_hn, get_trending
from reddit_fetcher import search_reddit, get_subreddit_hot
from summarizer import generate_summary, generate_brief_summary


# 页面配置
st.set_page_config(
    page_title="Info Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .post-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
    }
    .hn-card {
        border-left-color: #FF6600;
    }
    .reddit-card {
        border-left-color: #FF4500;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def display_post(post: Dict):
    """显示单个帖子卡片"""
    source = post.get("source", "")
    card_class = "hn-card" if source == "Hacker News" else "reddit-card"

    with st.container():
        st.markdown(f'<div class="post-card {card_class}">', unsafe_allow_html=True)

        col1, col2 = st.columns([4, 1])

        with col1:
            # 标题和链接
            title = post.get("title", "")
            url = post.get("url", "")
            st.markdown(f"**[{title}]({url})**")

            # 来源信息
            if source == "Reddit":
                subreddit = post.get("subreddit", "")
                st.caption(f"📍 r/{subreddit}")

        with col2:
            # 统计
            score = post.get("score", 0)
            comments = post.get("comments", 0)
            st.metric("⬆️", score)
            st.caption(f"💬 {comments}")

        st.markdown('</div>', unsafe_allow_html=True)


def main():
    # 头部
    st.markdown('<p class="main-header">🔍 Info Research Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">聚合 HN + Reddit，AI智能摘要，快速洞察趋势</p>', unsafe_allow_html=True)

    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 设置")

        mode = st.radio(
            "模式选择",
            ["🎯 主题研究", "🔥 热门趋势"],
            index=0
        )

        limit = st.slider(
            "每来源帖子数",
            min_value=5,
            max_value=20,
            value=MAX_POSTS_PER_SOURCE
        )

        st.markdown("---")
        st.markdown("### 📖 使用说明")
        st.markdown("""
        1. 选择模式：主题研究或热门趋势
        2. 输入关键词或选择板块
        3. 点击搜索获取结果
        4. AI自动生成摘要报告
        """)

        st.markdown("---")
        st.caption(f"最后更新: {datetime.now().strftime('%H:%M:%S')}")

    # 主内容区
    if mode == "🎯 主题研究":
        # 搜索输入
        col1, col2 = st.columns([4, 1])

        with col1:
            keyword = st.text_input(
                "输入研究主题",
                placeholder="例如: AI Agent, Rust, Startup...",
                label_visibility="collapsed"
            )

        with col2:
            search_btn = st.button("🔍 搜索", type="primary", use_container_width=True)

        # 执行搜索
        if search_btn and keyword:
            with st.spinner("正在收集信息..."):
                progress_bar = st.progress(0)

                # 抓取HN
                progress_bar.progress(30)
                hn_posts = search_hn(keyword, limit)

                # 抓取Reddit
                progress_bar.progress(60)
                reddit_posts = search_reddit(keyword, limit)

                # 合并结果
                all_posts = hn_posts + reddit_posts
                progress_bar.progress(80)

                if all_posts:
                    # 生成摘要
                    summary = generate_summary(keyword, all_posts)
                    progress_bar.progress(100)

                    # 显示统计
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📊 总帖子数", len(all_posts))
                    with col2:
                        st.metric("📰 HN帖子", len(hn_posts))
                    with col3:
                        st.metric("💬 Reddit帖子", len(reddit_posts))

                    # 显示摘要
                    st.markdown("---")
                    st.markdown("### 📝 AI摘要报告")
                    st.markdown(summary)

                    # 显示帖子列表
                    st.markdown("---")
                    st.markdown("### 📋 详细帖子列表")

                    tab1, tab2 = st.tabs(["Hacker News", "Reddit"])

                    with tab1:
                        if hn_posts:
                            for post in hn_posts:
                                display_post(post)
                        else:
                            st.info("HN未找到相关帖子")

                    with tab2:
                        if reddit_posts:
                            for post in reddit_posts:
                                display_post(post)
                        else:
                            st.info("Reddit未找到相关帖子")

                else:
                    st.warning(f"未找到关于「{keyword}」的相关内容。请尝试其他关键词。")

        elif search_btn and not keyword:
            st.warning("请输入研究主题")

    else:  # 热门趋势模式
        st.markdown("### 🔥 今日热门")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Hacker News")
            if st.button("刷新HN热门", key="hn_refresh"):
                st.rerun()

            with st.spinner("加载中..."):
                hn_trending = get_trending(limit)
                for post in hn_trending[:5]:
                    display_post(post)

        with col2:
            st.markdown("#### Reddit")
            subreddit = st.selectbox(
                "选择板块",
                ["programming", "technology", "MachineLearning", "artificial", "startups"]
            )

            if st.button("刷新Reddit热门", key="reddit_refresh"):
                st.rerun()

            with st.spinner("加载中..."):
                reddit_trending = get_subreddit_hot(subreddit, limit)
                for post in reddit_trending[:5]:
                    display_post(post)


if __name__ == "__main__":
    main()
