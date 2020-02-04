---
title : PySpark Install
sidebar_main : true
use_math : true
header:
  # teaser :
  # overlay_image :
---




### Version

 * OS 
 
```
MacOS Mojave Version 10.14.6
```

* Java

```
$ java -version
openjdk version "1.8.0_222"
OpenJDK Runtime Environment (AdoptOpenJDK)(build 1.8.0_222-b10)
OpenJDK 64-Bit Server VM (AdoptOpenJDK)(build 25.222-b10, mixed mode)

$ javac -versionw
javac 1.8.0_222
```


* Scala

```
$ scala -version
Scala code runner version 2.13.0 -- Copyright 2002-2019, LAMP/EPFL and Lightbend, Inc.
```

## Install pyspark

```
$ brew install apache-spark@2.3.2

==> Installing apache-spark@2.3.2 from eddies/spark-tap
==> Downloading https://archive.apache.org/dist/spark/spark-2.3.2/spark-2.3.2-bin-hadoop2.7.tgz
Already downloaded: /Users/has3ong/Library/Caches/Homebrew/downloads/df98174845f8d2418a685220c6bccc23ada4c07c3f11875ea1df5a44b296366a--spark-2.3.2-bin-hadoop2.7.tgz
🍺  /usr/local/Cellar/apache-spark@2.3.2/2.3.2: 1,019 files, 243.9MB, built in 6 seconds

$ pip install pyspark
```

apache-spark@2.3.2 버전으로 사용하겠습니다.


## Setting Environments

Java

```
$ export JAVA_HOME="/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home"
```

Scala

```
$ export SCALA_HOME="usr/local/Cellar/scala/2.13.0/libexec"
$ export PATH=$PATH:$SCLAL_HOME/bin
```

Spark

```
$ export SPARK_HOME="/usr/local/Cellar/apache-spark@2.3.2/2.3.2/libexec"
$ export PATH=$PATH:$SPARK_HOME
```

Python

```
$ export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH
$ export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH
```

터미널안에서 실행시켜도 되며 `sudo vi ~/.bash_profile` 안에 들어가서 수정하신뒤 `source ~/.bash_profile` 명령어를 통해 사용하셔도 무방합니다.


## Start PySpark

```
$ pyspark
Python 3.7.4 (default, Jul  9 2019, 18:13:23)
[Clang 10.0.1 (clang-1001.0.46.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
2019-09-30 00:12:33 WARN  NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.3.2
      /_/

Using Python version 3.7.4 (default, Jul  9 2019 18:13:23)
SparkSession available as 'spark'.
>>> 2019-09-30 19:54:31 WARN  HeartbeatReceiver:66 - Removing executor driver with no recent heartbeats: 457928 ms exceeds timeout 120000 ms
2019-09-30 19:54:31 ERROR TaskSchedulerImpl:70 - Lost an executor driver (already removed): Executor heartbeat timed out after 457928 ms
2019-09-30 19:54:31 WARN  SparkContext:66 - Killing executors is not supported by current scheduler.


```


`pyspark`명령어를 쳤을때 다음과 같은 화면이 나오면 정상적으로 설치가 완료가 되었습니다.
`pyspark`명령어를 통해 Spark shell을 사용하면 web UI를 사용할 수 있다. 기본값은 `127.0.0.1:4041`로 잡혀있다.

![스크린샷 2019-09-30 오전 12 12 41](https://user-images.githubusercontent.com/44635266/65944174-1b789900-e46c-11e9-8ef7-c06b3c7dd203.png)


## Error

* 2019-09-30 00:07:30 WARN  Utils:66 - Service 'sparkDriver' could not bind on a random free port. You may check whether configuring an appropriate binding address.

```
2019-09-30 00:07:30 WARN  Utils:66 - Service 'sparkDriver' could not bind on a random free port. You may check whether configuring an appropriate binding address.
2019-09-30 00:07:30 ERROR SparkContext:91 - Error initializing SparkContext.
java.net.BindException: Can't assign requested address: Service 'sparkDriver' failed after 16 retries (on a random free port)! Consider explicitly setting the appropriate binding address for the service 'sparkDriver' (for example spark.driver.bindAddress for SparkDriver) to the correct binding address.
	at sun.nio.ch.Net.bind0(Native Method)
	at sun.nio.ch.Net.bind(Net.java:433)
	at sun.nio.ch.Net.bind(Net.java:425)
	at sun.nio.ch.ServerSocketChannelImpl.bind(ServerSocketChannelImpl.java:223)
	at io.netty.channel.socket.nio.NioServerSocketChannel.doBind(NioServerSocketChannel.java:128)
	at io.netty.channel.AbstractChannel$AbstractUnsafe.bind(AbstractChannel.java:558)
	at io.netty.channel.DefaultChannelPipeline$HeadContext.bind(DefaultChannelPipeline.java:1283)
	at io.netty.channel.AbstractChannelHandlerContext.invokeBind(AbstractChannelHandlerContext.java:501)
	at io.netty.channel.AbstractChannelHandlerContext.bind(AbstractChannelHandlerContext.java:486)
	at io.netty.channel.DefaultChannelPipeline.bind(DefaultChannelPipeline.java:989)
	at io.netty.channel.AbstractChannel.bind(AbstractChannel.java:254)
	at io.netty.bootstrap.AbstractBootstrap$2.run(AbstractBootstrap.java:364)
	at io.netty.util.concurrent.AbstractEventExecutor.safeExecute(AbstractEventExecutor.java:163)
	at io.netty.util.concurrent.SingleThreadEventExecutor.runAllTasks(SingleThreadEventExecutor.java:403)
	at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:463)
	at io.netty.util.concurrent.SingleThreadEventExecutor$5.run(SingleThreadEventExecutor.java:858)
	at io.netty.util.concurrent.DefaultThreadFactory$DefaultRunnableDecorator.run(DefaultThreadFactory.java:138)
	at java.lang.Thread.run(Thread.java:748)
Traceback (most recent call last):
  File "/usr/local/Cellar/apache-spark@2.3.2/2.3.2/libexec/python/pyspark/shell.py", line 45, in <module>
    spark = SparkSession.builder\
  File "/usr/local/Cellar/apache-spark@2.3.2/2.3.2/libexec/python/pyspark/sql/session.py", line 173, in getOrCreate
    sc = SparkContext.getOrCreate(sparkConf)
  File "/usr/local/Cellar/apache-spark@2.3.2/2.3.2/libexec/python/pyspark/context.py", line 351, in getOrCreate
    SparkContext(conf=conf or SparkConf())
  File "/usr/local/Cellar/apache-spark@2.3.2/2.3.2/libexec/python/pyspark/context.py", line 118, in __init__
    conf, jsc, profiler_cls)
  File "/usr/local/Cellar/apache-spark@2.3.2/2.3.2/libexec/python/pyspark/context.py", line 180, in _do_init
    self._jsc = jsc or self._initialize_context(self._conf._jconf)
  File "/usr/local/Cellar/apache-spark@2.3.2/2.3.2/libexec/python/pyspark/context.py", line 290, in _initialize_context
    return self._jvm.JavaSparkContext(jconf)
  File "/usr/local/Cellar/apache-spark@2.3.2/2.3.2/libexec/python/lib/py4j-0.10.7-src.zip/py4j/java_gateway.py", line 1525, in __call__
  File "/usr/local/Cellar/apache-spark@2.3.2/2.3.2/libexec/python/lib/py4j-0.10.7-src.zip/py4j/protocol.py", line 328, in get_return_value
py4j.protocol.Py4JJavaError: An error occurred while calling None.org.apache.spark.api.java.JavaSparkContext.
: java.net.BindException: Can't assign requested address: Service 'sparkDriver' failed after 16 retries (on a random free port)! Consider explicitly setting the appropriate binding address for the service 'sparkDriver' (for example spark.driver.bindAddress for SparkDriver) to the correct binding address.
	at sun.nio.ch.Net.bind0(Native Method)
	at sun.nio.ch.Net.bind(Net.java:433)
	at sun.nio.ch.Net.bind(Net.java:425)
	at sun.nio.ch.ServerSocketChannelImpl.bind(ServerSocketChannelImpl.java:223)
	at io.netty.channel.socket.nio.NioServerSocketChannel.doBind(NioServerSocketChannel.java:128)
	at io.netty.channel.AbstractChannel$AbstractUnsafe.bind(AbstractChannel.java:558)
	at io.netty.channel.DefaultChannelPipeline$HeadContext.bind(DefaultChannelPipeline.java:1283)
	at io.netty.channel.AbstractChannelHandlerContext.invokeBind(AbstractChannelHandlerContext.java:501)
	at io.netty.channel.AbstractChannelHandlerContext.bind(AbstractChannelHandlerContext.java:486)
	at io.netty.channel.DefaultChannelPipeline.bind(DefaultChannelPipeline.java:989)
	at io.netty.channel.AbstractChannel.bind(AbstractChannel.java:254)
	at io.netty.bootstrap.AbstractBootstrap$2.run(AbstractBootstrap.java:364)
	at io.netty.util.concurrent.AbstractEventExecutor.safeExecute(AbstractEventExecutor.java:163)
	at io.netty.util.concurrent.SingleThreadEventExecutor.runAllTasks(SingleThreadEventExecutor.java:403)
	at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:463)
	at io.netty.util.concurrent.SingleThreadEventExecutor$5.run(SingleThreadEventExecutor.java:858)
	at io.netty.util.concurrent.DefaultThreadFactory$DefaultRunnableDecorator.run(DefaultThreadFactory.java:138)
	at java.lang.Thread.run(Thread.java:748)
```


로컬 주소를 못찾는 에러입니다. `export SPARK_LOCAL_IP="127.0.0.1"` 명령어를 치면됩니다.
