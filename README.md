# 长明 Everlight

通用外置记忆系统的完整设计仓库，附可运行的 SQLite 参考实现。不绑定 DSH、模型供应商或聊天界面；普通应用可以从进程内接口或自行实现的 API 接入。

**24 个模块 · 12 类存储职责 · 8 个扩展方向 · 21 个宿主钩子。**

事件和更正进入工作台，工作台与来源进入按需召回，核过的证据进入真实请求，输出和动作回执再进入长期记忆。后台做梦只提出可验证修订；策略候选通过独立对照后才能晋升，回退不覆盖用户更正和真实回执。

## 快速验证

需要 Python 3.11 或更新版本，无第三方依赖。以下命令不联网，不产生生产动作。

```sh
python examples/continue_task.py
python scripts/check.py
```

示例在临时 SQLite 内完成原始记录、定向更正、工作台更新、跨连接读回和旧索引回源；输出显示第二版待查送达，第三版仍禁发。输入已预分类，此示例不调用语言模型、执行器或真实渠道。

## 从哪里读

| 文件 | 内容 |
|---|---|
| [HANDOVER.md](HANDOVER.md) | 统一总设计、权限与数据归属、工作记忆/纠错/情绪/做梦/RSI |
| [HOOKS.md](HOOKS.md)、[hooks.json](hooks.json)、[wiring.json](wiring.json) | 21 个钩子的输入、输出、失败及 71 条声明连线 |
| [PORTABLE_API.md](PORTABLE_API.md) | 通用接入合同，路由目前是规范 |
| [ACCEPTANCE.md](ACCEPTANCE.md) | 各钩子验收、真实宿主关闭/开启/故障三组取证 |
| [baseline/](baseline/) | 原 24 模块详设、过去的研究与原型证据 |
| [research/](research/) | Anima、Claude 做梦、受控 RSI 与情绪研究 |
| [reference/](reference/) | 离线参考代码和回放测试 |

## 实现范围

当前跑通：SQLite 事件、事实时态、明确目标的结构化纠错、争议保留、版本并发、工作台恢复、候选动作检查。全量设计齐备，开放语言理解、线上 API、真实模型请求替换、跨平台适配、后台做梦与 RSI 引擎仍按契约实施和验收。production_approved=false。

## 提交到仓库

在解压得到的 `Everlight` 目录中执行。将最后两条远端命令用于你创建的**空仓库**：

```sh
git init -b main
git add .
git commit -m "Add Everlight universal memory design and offline reference"
git remote add origin <你的远端仓库地址>
git push -u origin main
```

已有历史的项目，请在现有仓库的新分支中导入文件，不要强制覆盖远端。默认未附开源许可证；若要授予开源使用和再分发权，由权利人选定许可证后加入。
