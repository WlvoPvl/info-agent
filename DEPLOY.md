# 部署指南

## 方式一：Streamlit Cloud（推荐，免费）

1. 访问 https://share.streamlit.io
2. 用GitHub账号登录
3. 点击 "New app"
4. 选择仓库: `WlvoPvl/info-agent`
5. 主文件路径: `app.py`
6. 点击 "Advanced settings"，添加环境变量:
   - `ANTHROPIC_API_KEY`: 你的Claude API Key
7. 点击 "Deploy"

部署完成后会获得一个公开URL，如: `https://info-agent-xxx.streamlit.app`

## 方式二：Render

1. 访问 https://render.com
2. 注册并连接GitHub
3. 创建新的Web Service
4. 选择 `WlvoPvl/info-agent` 仓库
5. 设置:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. 添加环境变量 `ANTHROPIC_API_KEY`
7. 部署

## 注意事项

- 需要有效的 `ANTHROPIC_API_KEY`
- Reddit API在某些地区可能需要代理
- HN API全球可用
