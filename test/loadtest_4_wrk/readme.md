mac 下安装测试工具
```
brew install wrk
```

使用lua 脚本进行post 请求测试
```
$ gunicorn -w 2 -k gevent --worker-connections=1000 -b 0.0.0.0:8000 app.app:application

$ wrk -t12 -c1000 -d30s -shttp_post.lua http://127.0.0.1:8000/app

Running 30s test @ http://127.0.0.1:8000/app
  12 threads and 1000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.36ms   27.03ms   1.76s    99.88%
    Req/Sec     1.31k     0.86k    3.98k    68.58%
  94786 requests in 30.10s, 14.01MB read
  Socket errors: connect 755, read 101, write 0, timeout 682
Requests/sec:   3149.35
Transfer/sec:    476.72KB


$ gunicorn -w 4 -k gevent --worker-connections=1000 -b 0.0.0.0:8000 app.app:application

$ wrk -t12 -c1000 -d30s -shttp_post.lua http://127.0.0.1:8000/app

Running 30s test @ http://127.0.0.1:8000/app
  12 threads and 1000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.39ms   18.97ms   1.94s    99.89%
    Req/Sec     1.14k   433.68     3.55k    82.13%
  121203 requests in 30.10s, 17.92MB read
  Socket errors: connect 755, read 232, write 0, timeout 189
Requests/sec:   4026.05
Transfer/sec:    609.43KB
```
