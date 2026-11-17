# 长明最终设计交付

先读FINAL_DESIGN.md，它是可独立阅读的完整合并版。FINAL_DECISIONS.md是全局最终裁决；MODULE_DECISIONS.md是24模块逐项裁决；modules/是每模块18节详细机制、例子及验收需求。contracts/包含公共接口、分库、DDL、接线和参考资料，旧版本标识用于兼容追溯。

规范优先级：最终裁决→公共契约→逐模块细则。原864项是需求目录，40项是链路验收设计，均未执行；不得引用为通过证据。reference/v6_design_audit.md和evidence/是历史记录，保留原失败，不代表本轮状态。

本轮实际：verification/test_reference.py的25项隔离参考测试通过；verification/validate_bundle.py的94项文档/目标SQLite结构检查通过。两组不能合并成系统通过率。参考代码只支持可信结构化锚下的逐字证据供应，以及显式情绪表达的内存状态归约；不是全系统运行软件。

可运行：

```sh
python3 verification/test_reference.py
python3 verification/validate_bundle.py
```

无第三方Python依赖；需要Python自带SQLite支持JSON函数。运行会在verification/写对应报告。没有真实DSH调用、开放语义验证、外部模型调用、生产变更或后台部署；production_approved=false。

设计覆盖工作/情感/社交成长、关系、愿望、八方向和A–F专项机制。完整自动执行需要宿主真实hook、持久调度器、受权读源、统一供应出口和可信回执；不存在仅靠文档就能启动的自动化。
