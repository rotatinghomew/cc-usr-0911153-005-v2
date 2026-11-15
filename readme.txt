东盟农业机器人现场反馈迭代仓

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
