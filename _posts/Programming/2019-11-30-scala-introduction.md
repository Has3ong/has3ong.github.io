---
title : Scala Introduction
tags :
- Scala
---

## Install Scala on Mac

### Runtime Enviroment

* macOS Catalina version 10.15.1
* java vesrsion
openjdk version "1.8.0_232"
OpenJDK Runtime Environment (AdoptOpenJDK)(build 1.8.0_232-b09)
OpenJDK 64-Bit Server VM (AdoptOpenJDK)(build 25.232-b09, mixed mode)

### Install

```
$ brew install scala                                                                                                              
Updating Homebrew...
==> Auto-updated Homebrew!
Updated 3 taps (homebrew/cask-versions, homebrew/core and homebrew/cask).
==> New Formulae
php@7.3
==> Updated Formulae
bee              coq              exploitdb        hugo             kustomize        math-comp        nifi-registry    pmd              timewarrior
borgmatic        drafter          helmfile         kubeseal         lightgbm         neomutt          php              tcsh             wiiuse

==> Downloading https://downloads.lightbend.com/scala/2.13.1/scala-2.13.1.tgz
######################################################################## 100.0%
==> Caveats
To use with IntelliJ, set the Scala home to:
  /usr/local/opt/scala/idea
==> Summary
🍺  /usr/local/Cellar/scala/2.13.1: 42 files, 20.1MB, built in 8 seconds

$ scala -version                                       
Scala code runner version 2.13.1 -- Copyright 2002-2019, LAMP/EPFL and Lightbend, Inc.

$ scala                                                                                                                             
Welcome to Scala 2.13.1 (OpenJDK 64-Bit Server VM, Java 1.8.0_232).
Type in expressions for evaluation. Or try :help.

scala>
```

> HelloWorld.scala

```
object HelloWorld{
    def main(args:Array[String]){
        println("Hello World!")
    }
}
```

JVM에 의해 실행 가능한 바이트 코드로 컴파일하기

```
$ scalac HelloWorld.scala
```
 
실행

```
$ scala HelloWorld
Hello World!
```

> Example 2

```
object HelloWorld {
  def main(args: Array[String]): Unit = {
    println("Hello World!")
    for {
      arg <- args
    } println(s"Arg=$arg")
  }
}
```
 
컴파일

```
$ scalac HelloWorld.scala
```

실행

```
$ scala HelloWorld 1 2 3
Hello World!
Arg=1
Arg=2
Arg=3
```