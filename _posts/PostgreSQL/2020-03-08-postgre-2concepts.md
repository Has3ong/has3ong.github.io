---
title : PostgreSQL Chapter 2. The SQL Language
tags :
- PostgreSQL
---

## 2.2. Concepts

PostgreSQL은 RDBMS(Relational Database Management System) 입니다. 이 말은 저장된 데이터를 관계(Relation) 를 이용하여 관리하는 시스템입니다. 관계는 본질적으로 표(Table) 의 수학적 용어입니다. 현재 데이터를 표에 저장하는 개념은 너무 흔해보일지 모르지만, 데이터베이스를 구성하는 방법은 많이있습니다. Unix 와 같은 운영체제의 파일과 디렉토리의 형태는 데이터베이스 계층의 대표적인 예 입니다. 더 현대적인 발전은 객체 지향 데이터베이스입니다.

각 테이블은 이름이 있는 행(col) 들의 모음(Collection) 입니다. 각각의 행은 테이블의 동일한 명명된 열(row) 집합을 가지고 있으며, 각 열은 특정 데이터 유형입니다. 각 열에는 순서가 있는 반면에 SQL 은 표 내의 행의 순서를 보장하지 않습니다.(표시용으로는 명시적으로 정렬할 수 있습니다.)

테이블은 데이터베이스에 그룹화되며, 단일 PostgreSQL 서버 인스턴스에 의해 관리되는 데이터베이스 컬렉션이 데이터베이스 클러스터를 구성합니다.