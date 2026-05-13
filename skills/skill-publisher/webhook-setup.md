# GitHub Webhook 自动同步设置

本指南说明如何设置 GitHub 仓库与 agentskill.sh 之间的自动同步。

## 为什么设置自动同步？

- **每日同步**（自动）：agentskill.sh 每 24 小时检查一次更改
- **即时同步**（推荐）：每次 `git push` 后立即更新

## 设置说明

1. 导航到你的 GitHub 仓库
2. 进入 **Settings** → **Webhooks** → **Add webhook**
3. 配置 webhook：
   - **Payload URL**：在提交仓库后从 agentskill.sh 提交页面获取
   - **Content type**：`application/json`
   - **Secret**：留空或使用 agentskill.sh 提供的值
   - **Which events**：选择 "Just the push event"
   - **Active**：勾选
4. 点击 **Add webhook** 保存

## 验证

设置完成后，向你的仓库进行一次测试推送，并验证技能在几分钟内就在 agentskill.sh 上更新了。

## 故障排除

- 如果同步失败，请检查 GitHub Settings → Webhooks → [Your webhook] → Recent Deliveries 中的 webhook 交付日志
- 确保 Payload URL 正确且可访问
