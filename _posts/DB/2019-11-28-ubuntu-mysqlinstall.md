---
title : Install MySQL on Ubuntu 18.04
tags :
- Ubuntu18.04
- MySQL
- DataBase
- Install
---

## 1. Install MySQL

```shell
$ sudo apt update && sudo apt install mysql-server
```

설치가 되었는지 확인

```shell
$ mysql --version
mysql  Ver 14.14 Distrib 5.7.28, for Linux (x86_64) using  EditLine wrapper
```

```shell
$ sudo systemctl status mysql
● mysql.service - MySQL Community Server
   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2019-11-28 05:39:18 UTC; 1h 10min ago
 Main PID: 12846 (mysqld)
    Tasks: 30 (limit: 2361)
   CGroup: /system.slice/mysql.service
           └─12846 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid

Nov 28 05:39:18 ip-172-26-8-131 systemd[1]: Starting MySQL Community Server...
Nov 28 05:39:18 ip-172-26-8-131 systemd[1]: Started MySQL Community Server.
```

## 2. Configure Security

새로운 MySQL 복사본을 설치할 때마다 MySQL 설치의 보안을 강화하기 위해 변경하는 기본 설정이 있습니다.

```shell
$ sudo mysql_secure_installation
```

가장 먼저 비밀번호 확인 플러그인을 설정해야합니다.

```shell
Securing the MySQL server deployment.

Connecting to MySQL using a blank password.

VALIDATE PASSWORD PLUGIN can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD plugin?

Press y|Y for Yes, any other key for No:
```

사용자가 원하는 비밀번호의 강도에 따라 루트의 보안 비밀번호를 설정할 수 있습니다.

```shell
There are three levels of password validation policy:

LOW    Length >= 8
MEDIUM Length >= 8, numeric, mixed case, and special characters
STRONG Length >= 8, numeric, mixed case, special characters and dictionary                  file

Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG:
```

비밀번호 보안을 위해 선택한 번호를 입력하고 Enter를 누르십시오. 그러면 시스템은 새로운 root 암호를 묻습니다.

```shell
Please set the password for root here.

New password:

Re-enter new password:
```

그러면 시스템이 제공 한 암호의 강도를 표시하고 암호를 계속 사용할 것인지 묻습니다.

```shell
Do you wish to continue with the password provided?(Press y|Y for Yes, any other key for No) :
```

이제 시스템에 질문이 하나씩 표시되며 질문에 대한 답변에 따라 시스템 보안을 설정할 수 있습니다.

첫 번째 질문은 익명의 테스트 사용자를 제거 할 것인지 묻습니다.

```shell
By default, a MySQL installation has an anonymous user,
allowing anyone to log into MySQL without having to have
a user account created for them. This is intended only for
testing, and to make the installation go a bit smoother.
You should remove them before moving into a production
environment.

Remove anonymous users? (Press y|Y for Yes, any other key for No) :
```

두 번째 질문은 원격 시스템에서 루트 로그인을 허용하지 않을 것인지 묻습니다. 보안 시스템의 경우 루트는 로컬 호스트에서만 연결될 수 있어야하므로 일반적으로 선택해야합니다.

```shell
Normally, root should only be allowed to connect from
'localhost'. This ensures that someone cannot guess at
the root password from the network.

Disallow root login remotely? (Press y|Y for Yes, any other key for No) :
```

세 번째 질문은 시스템에서“test”라는 기본 MySQL 데이터베이스를 제거하고 해당 데이터베이스에 대한 액세스를 제거 할 것인지 묻습니다.

나중에 test 데이터베이스를 만들어도되니 삭제할게요.

```shell
By default, MySQL comes with a database named 'test' that
anyone can access. This is also intended only for testing,
and should be removed before moving into a production
environment.


Remove test database and access to it? (Press y|Y for Yes, any other key for No) :
```

마지막으로 위에서 구성된 모든 변경 사항을 적용하려면 시스템에서 권한 테이블을 다시로드해야합니다. y를 입력하면 모든 보안 변경 사항이 적용됩니다.

```shell
Reloading the privilege tables will ensure that all changes
made so far will take effect immediately.

Reload privilege tables now? (Press y|Y for Yes, any other key for No) :
```

## 3. Configuring Root to use MySQL shell

보안 스크립트를 실행하는 동안 root의 비밀번호를 제공했습니다. 그러나이 사용자는 동일한 비밀번호를 사용하여 MySQL 쉘에 연결할 수 없습니다.인증 방법을 기본“auth_socket”에서“mysql_native_password”로 변경하여 MySQL 셸을 사용하도록 configure root를 변경할 수 있습니다.

```shell
$ sudo mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 5.7.28-0ubuntu0.18.04.4 (Ubuntu)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SELECT user,authentication_string,plugin,host FROM mysql.user;
+------------------+-------------------------------------------+-----------------------+-----------+
| user             | authentication_string                     | plugin                | host      |
+------------------+-------------------------------------------+-----------------------+-----------+
| root             |                                           | auth_socket           | localhost |
| mysql.session    | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
| mysql.sys        | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
| debian-sys-maint | *1621A389402B4174C866ED1EF7850646AD205BC9 | mysql_native_password | localhost |
+------------------+-------------------------------------------+-----------------------+-----------+
4 rows in set (0.00 sec)

mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
Query OK, 0 rows affected (0.00 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT user,authentication_string,plugin,host FROM mysql.user;
+------------------+-------------------------------------------+-----------------------+-----------+
| user             | authentication_string                     | plugin                | host      |
+------------------+-------------------------------------------+-----------------------+-----------+
| root             | *2470C0C06DEE42FD1618BB99005ADCA2EC9D1E19 | mysql_native_password | localhost |
| mysql.session    | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
| mysql.sys        | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
| debian-sys-maint | *1621A389402B4174C866ED1EF7850646AD205BC9 | mysql_native_password | localhost |
+------------------+-------------------------------------------+-----------------------+-----------+
4 rows in set (0.00 sec)

mysql> exit
Bye
```

## Start MySQL

```shell
$ mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 5.7.28-0ubuntu0.18.04.4 (Ubuntu)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```