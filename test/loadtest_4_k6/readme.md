mac 下安装测试工具
```
brew tap loadimpact/k6
brew install k6
```

使用 docker，下载测试工具
```
docker pull loadimpact/k6
```

执行测试
```
k6 run --vus 1 --duration 1s - < http_post.js
k6 run --vus 10 --duration 1s - < http_post.js
```

或者使用docker
```
docker run -i loadimpact/k6 run --vus 1 --duration 1s - < http_post.js
docker run -i loadimpact/k6 run --vus 10 --duration 1s - < http_post.js
```

注：
mac上使用docker时，测试用力不能使用`127.0.0.1`这样的地址。
参数 vus 的意思是 virtual users


测试环境
  处理器名称：	Intel Core i5
  处理器速度：	2.7 GHz
  处理器数目：	1
  核总数：	2
  L2 缓存（每个核）：	256 KB
  L3 缓存：	3 MB
  内存：	8 GB

uwsgi测试结果
```
$ uwsgi --http :8000 --master --processes 2 --gevent 1000 -H /Users/sunxia/.virtualenvs/kinesisporducer --wsgi-file app/app.py

$ docker run -i loadimpact/k6 run --vus 500 --duration 1s - < http_post.js

...

    data_received.........: 49 kB (49 kB/s)
    data_sent.............: 822 kB (822 kB/s)
    http_req_blocked......: avg=79.66ms max=466.07ms med=52.82ms min=757.17µs p(90)=183.7ms p(95)=285.96ms
    http_req_connecting...: avg=77.62ms max=315.06ms med=51.78ms min=632.39µs p(90)=181.65ms p(95)=227.52ms
    http_req_duration.....: avg=86.36ms max=325.27ms med=73.51ms min=2.02ms p(90)=191.11ms p(95)=208.38ms
    http_req_receiving....: avg=12.66ms max=229.7ms med=3.46ms min=65.41µs p(90)=29.56ms p(95)=54.68ms
    http_req_sending......: avg=8.58ms max=203.54ms med=3.01ms min=38.7µs p(90)=19.12ms p(95)=40.73ms
    http_req_waiting......: avg=65.11ms max=312.66ms med=47.95ms min=1.72ms p(90)=141.66ms p(95)=160.96ms
    http_reqs.............: 709 (709/s)
    vus...................: 500
    vus_max...............: 500

$ docker run -i loadimpact/k6 run --vus 500 --duration 30s - < http_post.js

...

    data_received.........: 580 kB (19 kB/s)
    data_sent.............: 9.7 MB (325 kB/s)
    http_req_blocked......: avg=46.23ms max=1.35s med=9.32ms min=4.05µs p(90)=139.91ms p(95)=249.71ms
    http_req_connecting...: avg=45.5ms max=1.35s med=8.78ms min=1.44ms p(90)=139.41ms p(95)=245.19ms
    http_req_duration.....: avg=38.04ms max=537.15ms med=11.86ms min=33.96µs p(90)=96.84ms p(95)=195.82ms
    http_req_receiving....: avg=1.87ms max=131.48ms med=274.12µs min=185.13µs p(90)=4.35ms p(95)=9ms
    http_req_sending......: avg=3.36ms max=169.47ms med=366.82µs min=32.04µs p(90)=7.53ms p(95)=16.15ms
    http_req_waiting......: avg=32.79ms max=525.58ms med=9.37ms min=1.46ms p(90)=87.69ms p(95)=182.92ms
    http_reqs.............: 8411 (280.3666666666667/s)
    vus...................: 500
    vus_max...............: 500
...
    
```

gunicorn 测试
```
$ gunicorn -w 2 -k gevent --worker-connections=2000 -b 0.0.0.0:8000 app.app:application
$ docker run -i loadimpact/k6 run --vus 500 --duration 30s - < http_post.js
...

    data_received.........: 23 kB (754 B/s)
    data_sent.............: 169 kB (5.6 kB/s)
    http_req_blocked......: avg=817.42µs max=206.46ms med=4.24µs min=1.33µs p(90)=6.81µs p(95)=9µs
    http_req_connecting...: avg=809.91µs max=206.39ms med=0s min=0s p(90)=0s p(95)=0s
    http_req_duration.....: avg=103.1ms max=455.63ms med=103.4ms min=1.28ms p(90)=189.92ms p(95)=217.65ms
    http_req_receiving....: avg=19.83ms max=219.44ms med=230.43µs min=16.16µs p(90)=49.04ms p(95)=51.88ms
    http_req_sending......: avg=122.02µs max=91.22ms med=34.14µs min=11.73µs p(90)=96.55µs p(95)=177.42µs
    http_req_waiting......: avg=83.14ms max=416.92ms med=85.45ms min=1.15ms p(90)=159.42ms p(95)=180.76ms
    http_reqs.............: 28233 (941.1/s)
    vus...................: 500
    vus_max...............: 500



$ gunicorn -w 4 -k gevent --worker-connections=1000 -b 0.0.0.0:8000 app.app:application
$ docker run -i loadimpact/k6 run --vus 1000 --duration 30s - < http_post.js
...
    data_received.........: 22 kB (728 B/s)
    data_sent.............: 163 kB (5.4 kB/s)
    http_req_blocked......: avg=5.67ms max=1.13s med=4.41µs min=1.36µs p(90)=7.04µs p(95)=9.05µs
    http_req_connecting...: avg=5.66ms max=1.13s med=0s min=0s p(90)=0s p(95)=0s
    http_req_duration.....: avg=77.21ms max=560.33ms med=58.52ms min=1.37ms p(90)=179.7ms p(95)=215.42ms
    http_req_receiving....: avg=13.82ms max=222.83ms med=105.47µs min=14.75µs p(90)=48.79ms p(95)=52.67ms
    http_req_sending......: avg=341.82µs max=325.47ms med=35.07µs min=12.09µs p(90)=113.98µs p(95)=274.96µs
    http_req_waiting......: avg=63.04ms max=518.07ms med=43.65ms min=1.11ms p(90)=151.18ms p(95)=186.24ms
    http_reqs.............: 25870 (862.3333333333334/s)
    vus...................: 1000
    vus_max...............: 1000

```


为啥我的测试结果是gunicorn 比uwsgi 好很多？？？
而且uwsgi测试中抛出大量异常


之前的测试为纯 http 性能的测试，打开kinesis producer 功能后，重新测试

首先使用来一条发送一条 sync 发送方式
```
$ gunicorn -w 4 -k gevent --worker-connections=2000 -b 0.0.0.0:8000 app.app:application
$ docker run -i loadimpact/k6 run --vus 1000 --duration 30s - < http_post.js
...
    data_received.........: 23 kB (754 B/s)
    data_sent.............: 169 kB (5.6 kB/s)
    http_req_blocked......: avg=135.07ms max=578.12ms med=5.3µs min=1.98µs p(90)=550.32ms p(95)=570.91ms
    http_req_connecting...: avg=134.99ms max=577.96ms med=0s min=0s p(90)=549.92ms p(95)=569.94ms
    http_req_duration.....: avg=7.49s max=12.95s med=7.58s min=304.89ms p(90)=12.25s p(95)=12.48s
    http_req_receiving....: avg=24.17ms max=161ms med=40.84ms min=30.72µs p(90)=48.66ms p(95)=49.48ms
    http_req_sending......: avg=1.4ms max=45.75ms med=42.35µs min=19.69µs p(90)=2.29ms p(95)=4.68ms
    http_req_waiting......: avg=7.46s max=12.95s med=7.54s min=261.01ms p(90)=12.22s p(95)=12.44s
    http_reqs.............: 474 (15.8/s)
    vus...................: 1000
    vus_max...............: 1000

```

使用批量发送的方式发送