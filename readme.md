启动 gunicorn
```
cd kinesis-http-porducer
gunicorn -w 8 -k gevent -b 0.0.0.0:8000 app.app:application
```

使用 supervisord
```
cd kinesis-http-porducer
supervisord
```

测试
```
curl -H "Content-Type: application/json" -X POST  --data '{"appid":"test"}'  http://127.0.0.1:8000/
```

supervisord 配置  
http://liyangliang.me/posts/2015/06/using-supervisor/

kinesis 介绍
https://blog.insightdatascience.com/getting-started-with-aws-serverless-architecture-tutorial-on-kinesis-and-dynamodb-using-twitter-38a1352ca16d