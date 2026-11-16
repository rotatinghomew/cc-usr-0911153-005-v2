东盟农业机器人现场反馈迭代仓

发布阶段连接设备升级名额。应用的 fleet_delivery.register 按地区、机型、固件登记不可变设备名单，
canary 分配十分之一名额，rolled_out 分配全部名额；rolled_back 撤回未送达名额，已送达事实保留。
fleet_delivery.delivered 用当前发布意图确认单台设备送达，旧意图和已撤回名额不能确认。
发布意图引用已落库的现场报告版本与评议；inspect 和区域摘要可查看当前名额及历史发布依据。

运行验收：
python3 -m field_feedback run --fixture fixtures/acceptance.json --database /tmp/field_feedback.sqlite3 --output /tmp/field_feedback-output

核验：
python3 -m field_feedback verify --database /tmp/field_feedback.sqlite3 --output /tmp/field_feedback-output

全量测试：
python3 -m unittest discover -s tests -v

按模块测试：
python3 -m unittest tests.observations.test_report -v

构建检查：
python3 -m compileall -q field_feedback tests
