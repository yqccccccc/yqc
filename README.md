# Discord Bot for Railway (GitHub Ready)

## 🛠 部署指南

1. 上传本项目到 GitHub 仓库
2. 在 Railway 新建项目 → 选择 `Deploy from GitHub Repo`
3. 设置环境变量：
   - `TOKEN` = 你的 Discord Bot Token
4. 设置启动命令（Start Command）为：
   ```bash
   python discord-bot.py
   ```

## 📁 文件说明

- `discord-bot.py`：你的主程序入口
- `requirements.txt`：Python 依赖
- `.env.example`：环境变量模板
