# GPT Tools

项目简介：本项目基于GPT完成数据标注、分类、润色等工作，原理是多线程批量处理input的数据，经过GPT处理后输出output数据。


## 如何使用

1. 明确输入输出文件

在config.ini中编辑input和output

```ini
[data]
input=/data/test/classify_test.csv
output=/data/output/classify_test_out.csv
```

2. 修改任务server
不同的任务有不同的处理逻辑，本项目当前支持润色和分类两大类任务，业务逻辑和prompt详见/server文件夹
执行前请选择正确的run.py中的server

```python
# 修改server源
import server.classify_server as server_pool

if __name__ == "__main__":
    # 不同的任务切换不同的server即可
    server = server_pool.classifyServer()
```

3. 执行run.py

```bash
python run.py
```

4. 检查结果
结果按照config.ini的output输出，运行完毕后请检查output是否正确生成
