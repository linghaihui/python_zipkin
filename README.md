一个简单的[zipkin](https://zipkin.io/)的例子。

模拟了如下图的api调用关系:

<img src="https://ws1.sinaimg.cn/large/006tKfTcgy1g0poh292l6j30vq0qmdla.jpg" width=400>

在安装好依赖的python虚拟环境 运行 `bash start.sh`, 然后在终端执行 `curl 127.0.0.1:9001/api`, 浏览器打开`http://127.0.0.1:9411` 可看到结果:

![](https://ws1.sinaimg.cn/large/006tKfTcgy1g0pp4x5zzbj31uo0em0v0.jpg)
