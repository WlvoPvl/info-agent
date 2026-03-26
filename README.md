# Info Research Agent MVP

🔍 聚合 Hacker News + Reddit，AI智能摘要，快速洞察趋势

## 功能

- **主题研究**: 输入关键词，自动搜索HN和Reddit相关内容
- **AI摘要**: Claude生成结构化研究报告
- **热门趋势**: 查看HN和Reddit热门帖子

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 ANTHROPIC_API_KEY

# 3. 运行
streamlit run app.py
```

## 部署

### Vercel/Render 部署

1. 推送到GitHub
2. 连接Render/Vercel
3. 设置环境变量 `ANTHROPIC_API_KEY`
4. 部署

## 技术栈

- Python 3.10+
- Streamlit (Web界面)
- Anthropic Claude API (摘要生成)
- Hacker News API
- Reddit API

## 变现计划

- 免费版: 每日5次查询
- 付费版: 无限查询 + 定时报送 + 更多数据源

## License

MIT
