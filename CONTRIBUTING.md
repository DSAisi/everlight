# 参与长明

从 HANDOVER.md 和 HOOKS.md 开始。改变规范时同时检查契约、故障分支、真实宿主验收要求，以及对应的模块责任。不得把本地模拟记录登记为真实宿主通过。

1. 提交只使用合成或脱敏数据；不要纳入生产记忆、凭据、个人账号链接或真实请求正文。
2. 修改代码后运行 `python scripts/check.py`。变更 hook 要更新 hooks.json、wiring.json、ACCEPTANCE.md 和 fixtures。
3. manifest.json 是交付包文件快照，修改后用 `python scripts/refresh_manifest.py` 更新再验证。
4. DSH 阶段二保持冻结；本仓库的参考代码不启动或修改 DSH。
