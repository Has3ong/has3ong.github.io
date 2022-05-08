---
title:  "Java 16 New Features"
excerpt: "Java 16 New Features"
categories:
  - Programming
tags:
  - Programming
  - Java
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

새로운 LTS 버전인 JDK 16가 2021년 3월 16일에 발표가 되었습니다.

추가된 기능들을 알아보겠습니다.

[JDK 16](https://openjdk.java.net/projects/jdk/16/)를 참고했습니다.

### JEP 338:	Vector API (Incubator)

지원되는 CPU 아키텍처에서 최적의 벡터 명령어로 런타임에 안정적으로 컴파일되는 벡터 계산을 표현하는 API를 도입하여 동등한 스칼라 계산보다 우수한 성능을 달성합니다.

#### Goals 

* Clear and concise API — API는 루프 내에서 그리고 가능하면 제어 흐름으로 구성된 일련의 벡터 연산으로 구성된 광범위한 벡터 계산을 명확하고 간결하게 표현할 수 있어야 합니다. 벡터 크기 또는 벡터당 레인 수와 관련하여 일반적인 계산을 표현할 수 있어야 하므로 이러한 계산을 다른 벡터 크기를 지원하는 하드웨어 간에 이식할 수 있어야 합니다.
* Platform agnostic — API는 CPU 아키텍처에 구애받지 않고 벡터 명령을 지원하는 여러 아키텍처에서 구현할 수 있어야 합니다. 플랫폼 최적화와 이식성이 충돌하는 Java API에서 일반적으로 그러하듯이, 일부 플랫폼별 관용구를 이식 가능한 코드로 표현할 수 없는 결과를 낳더라도 API를 이식 가능한 것으로 만드는 쪽으로 편향됩니다.
* Reliable runtime compilation and performance on x64 and AArch64 architectures — 지원되는 x64 아키텍처에서 Java 런타임, 특히 HotSpot C2 컴파일러는 SSE(Streaming SIMD Extensions) 및 Advanced에서 지원하는 것과 같은 해당하는 효율적이고 성능이 뛰어난 벡터 명령어로 벡터 작업을 컴파일해야 합니다. 벡터 확장(AVX). 개발자는 자신이 표현하는 벡터 연산이 관련 벡터 명령어에 밀접하게 안정적으로 매핑될 것이라는 확신을 가져야 합니다. 가능한 ARM AArch64 아키텍처에서 C2는 유사하게 벡터 연산을 NEON에서 지원하는 벡터 명령어로 컴파일합니다.
* Graceful degradation — 아키텍처가 일부 필수 명령어를 지원하지 않기 때문에 런타임 시 벡터 계산을 벡터 명령어 시퀀스로 완전히 표현할 수 없는 경우가 있습니다. 이러한 경우 Vector API 구현은 정상적으로 저하되고 여전히 작동해야 합니다. 벡터 계산을 벡터 명령어로 효율적으로 컴파일할 수 없는 경우 경고가 표시될 수 있습니다. 벡터가 없는 플랫폼에서 단계적 저하로 인해 수동으로 풀린 루프와 경쟁력 있는 코드가 생성됩니다. 여기서 언롤 팩터는 선택한 벡터의 레인 수입니다.

#### Description

벡터는 추상 클래스 `Vector<E>`로 표현됩니다. 유형 변수 E는 벡터에 포함된 스칼라 기본 정수 또는 부동 소수점 요소 유형의 박스형 유형으로 인스턴스화됩니다. 벡터에는 벡터의 크기를 비트 단위로 정의하는 모양도 있습니다. 벡터의 모양은 벡터 계산이 HotSpot C2 컴파일러에 의해 컴파일될 때 `Vector<E>`의 인스턴스가 하드웨어 벡터 레지스터에 매핑되는 방식을 제어합니다. 벡터의 길이, 즉 레인 또는 요소의 수는 벡터 크기를 요소 크기로 나눈 값입니다.

지원되는 요소 유형(E) 세트는 `Byte`, `Short`, `Integer`, `Long`, `Float` 및 `Double`이며 각각 스칼라 기본 유형 `byte`, `short`, `int`, `long`,`float` 및 `double`에 해당합니다.

지원되는 모양 세트는 64, 128, 256 및 512비트의 벡터 크기와 최대 비트에 해당합니다. 512비트 모양은 바이트를 64개 레인으로 묶거나 `int`를 16개 레인으로 묶을 수 있으며 이러한 모양의 벡터는 한 번에 64바이트 또는 한 번에 16개 `int`에서 작동할 수 있습니다. 최대 비트 모양은 현재 아키텍처의 최대 벡터 크기를 지원합니다. 이를 통해 플랫폼 구현이 128비트 증분으로 128~2048비트 범위의 고정 크기를 지원할 수 있는 ARM SVE 플랫폼을 지원할 수 있습니다.

우리는 이러한 단순한 모양이 모든 관련 플랫폼에서 유용할 만큼 충분히 일반적이라고 믿습니다. 그러나 이 API의 인큐베이션 동안 미래 플랫폼을 실험하면서 모양 매개변수의 디자인을 추가로 수정할 수 있습니다. 이러한 작업은 이 프로젝트의 초기 범위에 있지 않지만 이러한 가능성은 부분적으로 Vector API에서 모양의 현재 역할을 알려줍니다. (자세한 논의는 아래의 향후 작업 섹션을 참조하십시오.)

요소 유형과 모양의 조합은 `VectorSpecies<E>`로 표시되는 벡터의 종을 결정합니다.

벡터에 대한 작업은 lane-wise 또는 cross-lane.으로 분류됩니다.

* lane-wise는 덧셈과 같은 스칼라 연산자를 하나 이상의 벡터의 각 레인에 병렬로 적용합니다. 레인별 연산은 항상 그런 것은 아니지만 일반적으로 길이와 모양이 같은 벡터를 생성합니다. Lane-wise 연산은 단항, 이진, 삼항, 테스트 또는 변환 연산으로 더 분류됩니다.
* cross-lane. 작업은 전체 벡터에 작업을 적용합니다. 교차 레인 작업은 스칼라 또는 다른 모양의 벡터를 생성합니다. 교차 차선 작업은 순열 또는 축소 작업으로 더 분류됩니다.

API의 표면을 줄이기 위해 각 작업 클래스에 대한 집합적 메서드를 정의합니다. 이러한 메서드는 연산자 상수를 입력으로 사용합니다. 이러한 상수는 VectorOperator.Operator 클래스의 인스턴스이며 VectorOperators 클래스의 정적 최종 필드에 정의됩니다. 편의를 위해 덧셈 및 곱셈과 같은 일부 일반적인 전체 서비스 작업에 대해 일반 메서드 대신 사용할 수 있는 전용 메서드를 정의합니다.

변환 및 재해석과 같은 벡터에 대한 특정 작업은 본질적으로 모양이 변경됩니다. 즉, 입력의 모양과 모양이 다른 벡터를 생성합니다. 벡터 계산의 모양 변경 작업은 이식성과 성능에 부정적인 영향을 줄 수 있습니다. 이러한 이유로 API는 적용 가능한 경우 각 모양 변경 작업의 모양 불변 특성을 정의합니다. 최상의 성능을 위해 개발자는 가능한 한 형태 불변 연산을 사용하여 형태 불변 코드를 작성해야 합니다. 모양 변경 작업은 API 사양에서 이와 같이 식별됩니다.

`Vector<E>` 클래스는 모든 요소 유형에서 지원하는 공통 벡터 작업에 대한 메서드 집합을 선언합니다. 요소 유형에 특정한 작업의 경우 `Vector<E>`에는 6개의 추상 하위 클래스가 있습니다. 지원되는 각 요소 유형에 대해 하나씩 `ByteVector`, `ShortVector`, `IntVector`, `LongVector`, `FloatVector` 및 `DoubleVector`입니다. 이러한 유형별 하위 클래스는 메서드 서명이 요소 유형 또는 관련 배열 유형을 참조하기 때문에 요소 유형에 바인딩되는 추가 작업을 정의합니다. 이러한 연산의 예로는 축소(예: 모든 레인을 스칼라 값으로 합산) 및 벡터 요소를 배열로 복사하는 것이 있습니다. 이러한 하위 클래스는 또한 정수 하위 유형에 특정한 추가 풀 서비스 연산(예: 논리 또는 같은 비트 연산)과 부동 소수점 유형에 특정한 연산(예: 지수와 같은 초월 수학 함수)을 정의합니다.

구현 문제로 `Vector<E>`의 이러한 유형별 하위 클래스는 다른 벡터 모양에 대한 구체적인 하위 클래스에 의해 추가로 확장됩니다. 이러한 구체적인 하위 클래스는 유형 및 모양에 특정한 작업을 제공할 필요가 없기 때문에 공개되지 않습니다. 이것은 API 표면을 제품이 아닌 관심사의 합계로 줄입니다. 구체적인 `Vector` 클래스의 인스턴스는 기본 `Vector<E>` 클래스 및 해당 유형별 하위 클래스에 정의된 팩토리 메서드를 통해 얻습니다. 이 팩토리는 원하는 벡터 인스턴스의 종류를 입력으로 받아 다양한 종류의 인스턴스를 생성합니다. 예를 들어 요소가 기본값(즉, 0 벡터)인 벡터 인스턴스 또는 지정된 배열에서 초기화된 벡터 인스턴스가 있습니다.

제어 흐름을 지원하기 위해 일부 벡터 작업은 선택적으로 공용 추상 클래스 `VectorMask<E>`가 나타내는 마스크를 허용합니다. 마스크의 각 요소는 벡터 레인에 해당하는 부울 값입니다. 마스크는 작업이 적용되는 레인을 선택합니다. 레인에 대한 마스크 요소가 `true`이면 적용되고 마스크가 `false`이면 일부 대체 작업이 수행됩니다.

벡터와 유사하게 `VectorMask<E>`의 인스턴스는 각 요소 유형 및 길이 조합에 대해 정의된 비공개 구체적인 하위 클래스의 인스턴스입니다. 작업에 사용되는 `VectorMask<E>`의 인스턴스는 작업에 포함된 벡터 인스턴스와 동일한 유형 및 길이를 가져야 합니다. 벡터 비교 작업은 마스크를 생성한 다음 다른 작업에 대한 입력으로 사용하여 특정 레인에서 선택적으로 작동하여 흐름 제어를 에뮬레이트할 수 있습니다. `VectorMask<E>` 클래스의 정적 팩토리 메서드를 사용하여 마스크를 만들 수도 있습니다.

우리는 마스크가 모양과 관련하여 일반적인 벡터 계산 개발에서 중요한 역할을 할 것으로 예상합니다. 이러한 기대는 ARM Scalable Vector Extensions 및 Intel의 AVX-512에서 마스크와 동일한 술어 레지스터의 핵심적인 중요성을 기반으로 합니다.

##### Example

다음은 배열 요소에 대한 간단한 스칼라 계산입니다.

```java
void scalarComputation(float[] a, float[] b, float[] c) {
   for (int i = 0; i < a.length; i++) {
        c[i] = (a[i] * a[i] + b[i] * b[i]) * -1.0f;
   }
}
```

(배열 인수의 길이가 같다고 가정합니다.)

다음은 Vector API를 사용한 등가 벡터 계산입니다.

```java
static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;

void vectorComputation(float[] a, float[] b, float[] c) {
    int i = 0;
    int upperBound = SPECIES.loopBound(a.length);
    for (; i < upperBound; i += SPECIES.length()) {
        // FloatVector va, vb, vc;
        var va = FloatVector.fromArray(SPECIES, a, i);
        var vb = FloatVector.fromArray(SPECIES, b, i);
        var vc = va.mul(va)
                   .add(vb.mul(vb))
                   .neg();
        vc.intoArray(c, i);
    }
    for (; i < a.length; i++) {
        c[i] = (a[i] * a[i] + b[i] * b[i]) * -1.0f;
    }
}
```

시작하려면 FloatVector에서 현재 아키텍처에 가장 적합한 모양을 가진 선호하는 종을 얻습니다. 런타임 컴파일러가 값을 상수로 처리하여 벡터 계산을 더 잘 최적화할 수 있도록 정적 최종 필드에 저장합니다. 그런 다음 메인 루프는 벡터 길이, 즉 종의 길이만큼 입력 배열을 반복합니다. 해당 인덱스의 배열 a와 b에서 주어진 종의 float 벡터를 로드하고 산술 연산을 유창하게 수행한 다음 결과를 배열 c에 저장합니다. 마지막 반복 후에 배열 요소가 남아 있으면 해당 꼬리 요소에 대한 결과가 일반 스칼라 루프로 계산됩니다.

이 구현은 대규모 어레이에서 최적의 성능을 달성합니다. HotSpot C2 컴파일러는 AVX를 지원하는 Intel x64 프로세서에서 다음과 유사한 기계어 코드를 생성합니다.

```
0.43%  / │  0x0000000113d43890: vmovdqu 0x10(%r8,%rbx,4),%ymm0
  7.38%  │ │  0x0000000113d43897: vmovdqu 0x10(%r10,%rbx,4),%ymm1
  8.70%  │ │  0x0000000113d4389e: vmulps %ymm0,%ymm0,%ymm0
  5.60%  │ │  0x0000000113d438a2: vmulps %ymm1,%ymm1,%ymm1
 13.16%  │ │  0x0000000113d438a6: vaddps %ymm0,%ymm1,%ymm0
 21.86%  │ │  0x0000000113d438aa: vxorps -0x7ad76b2(%rip),%ymm0,%ymm0
  7.66%  │ │  0x0000000113d438b2: vmovdqu %ymm0,0x10(%r9,%rbx,4)
 26.20%  │ │  0x0000000113d438b9: add    $0x8,%ebx
  6.44%  │ │  0x0000000113d438bc: cmp    %r11d,%ebx
         \ │  0x0000000113d438bf: jl     0x0000000113d43890
```

이것은 프로젝트 파나마 개발 저장소의 vectorIntrinsics 분기에 있는 Vector API 및 구현의 프로토타입을 사용하여 위 코드에 대한 JMH 마이크로 벤치마크의 출력입니다. 생성된 기계어 코드의 이러한 핫 영역은 벡터 레지스터 및 벡터 명령어로의 명확한 변환을 보여줍니다. 번역을 더 명확하게 하기 위해 루프 언롤링을 비활성화했습니다. 그렇지 않으면 HotSpot은 기존 C2 루프 최적화를 사용하여 이 코드를 해제합니다. 모든 Java 객체 할당이 생략됩니다.

##### Intel SVML intrinsics for transcendental operations

Vector API에는 이 JEP의 목표를 달성하기 위해 두 가지 구현이 있습니다. 첫 번째는 Java로 작업을 구현하므로 기능적이지만 최적은 아닙니다. 두 번째는 HotSpot C2 컴파일러에 대해 벡터 API 유형에 대한 특수 처리가 포함된 작업을 내장으로 만듭니다. 이것은 변환을 위한 아키텍처 지원 및 구현이 존재하는 경우 하드웨어 레지스터 및 명령으로의 적절한 변환을 허용합니다.

C2에 추가된 내장 함수가 폭발적으로 증가하는 것을 방지하기 위해 이진, 단항, 비교 등과 같은 연산 종류에 해당하는 내장 함수 집합이 정의되며, 여기서 연산 세부 사항을 설명하는 상수 인수가 전달됩니다. API의 모든 부분에 대한 내장 기능을 지원하려면 약 20개의 새로운 내장 기능이 필요합니다.

벡터 인스턴스는 가치 기반, 즉 신원에 민감한 작업을 피해야 하는 도덕적 가치입니다. 또한 벡터 인스턴스는 레인의 요소로 추상적으로 구성되지만 해당 요소는 C2에 의해 스칼라화되지 않습니다. 벡터 값은 적절한 크기의 하드웨어 벡터 레지스터에 매핑되는 `int` 또는 `long`과 같은 전체 단위로 처리됩니다. 인라인 유형은 벡터 값이 전체 단위로 취급되도록 하기 위해 몇 가지 관련 개선 사항이 필요합니다.

인라인 유형을 사용할 수 있을 때까지 Vector 인스턴스는 이스케이프 분석의 한계를 극복하고 boxing을 피하기 위해 C2에서 특별히 처리됩니다. 따라서 벡터에 대한 ID에 민감한 작업은 피해야 합니다.

### JEP 347:	Enable C++14 Language Features

JDK C++ 소스 코드에서 C++14 언어 기능의 사용을 허용하고 이러한 기능 중 HotSpot 코드에서 사용할 수 있는 기능에 대한 구체적인 지침을 제공합니다.

#### Goals

JDK 15를 통해 JDK의 C++ 코드가 사용하는 언어 기능은 C++98/03 언어 표준으로 제한되었습니다. JDK 11에서는 아직 새로운 기능을 사용하지 않지만 최신 버전의 C++ 표준으로 빌드할 수 있도록 코드가 업데이트되었습니다. 여기에는 C++11/14 언어 기능을 지원하는 다양한 컴파일러의 최신 버전으로 빌드할 수 있는 기능이 포함됩니다.

이 JEP의 목적은 JDK 내에서 C++ 소스 코드 변경 사항을 공식적으로 허용하여 C++14 언어 기능을 활용하고 핫스팟 코드에서 사용할 수 있는 기능에 대한 구체적인 지침을 제공하는 것입니다.

#### Description

##### Changes to the Build System

C++14 언어 기능을 활용하려면 플랫폼 컴파일러에 따라 몇 가지 빌드 시 변경이 필요합니다. 다양한 플랫폼 컴파일러의 최소 허용 버전도 지정해야 합니다. 원하는 언어 표준을 명시적으로 지정해야 합니다. 이후 컴파일러 버전은 기본적으로 이후의(호환되지 않는) 언어 표준으로 설정될 수 있습니다.

* Windows: JDK 11에는 Visual Studio 2017이 필요합니다. (이전 버전은 구성 시간 경고를 생성하며 작동할 수도 있고 작동하지 않을 수도 있습니다.) Visual Studio 2017의 경우 기본 C++ 표준은 C++14입니다. `/std:c++14` 옵션을 추가해야 합니다. 이전 버전에 대한 지원은 완전히 중단됩니다.
* Linux: `-std=gnu++98` 컴파일러 옵션을 `-std=c++14`로 바꿉니다. 지원되는 최소 `gcc` 버전은 5.0입니다.
* macOS: `-std=gnu++98` 컴파일러 옵션을 `-std=c++14`로 바꿉니다. 지원되는 최소 `clang` 버전은 3.5입니다.
* AIX/PowerPC: `-std=gnu++98` 컴파일러 옵션을 `-std=c++14`로 바꾸고 `xlclang++`를 컴파일러로 사용해야 합니다. `xlclang++`의 최소 지원 버전은 16.1입니다.

##### Changes to C++ Usage in HotSpot code

HotSpot 코드에서 C++ 사용에 대한 기존 제한 사항 및 모범 사례 권장 사항은 C++98/03 언어 표준을 기반으로 하며 HotSpot 스타일 가이드에 설명되어 있습니다.

최신 언어 표준의 기능에 대한 유사한 제한 및 지침을 해당 문서에 추가할 것입니다. 그것들은 허용된 기능의 표와 제외된 기능의 다른 표로 설명됩니다. 허용된 기능의 사용은 무조건적이거나 일부 제한 또는 추가 지침이 있을 수 있습니다. HotSpot 코드에서 제외된 기능의 사용은 금지되어 있습니다.

HotSpot 개발자가 합의에 도달하지 않았거나 전혀 논의되지 않은 세 번째 범주인 미정 기능이 있습니다. 이러한 기능의 사용도 금지됩니다.

그러나 일부 언어 기능의 사용은 즉시 명확하지 않을 수 있으며 컴파일러가 해당 기능을 수락하므로 어쨌든 실수로 미끄러질 수 있습니다. 항상 그렇듯이 코드 검토 프로세스는 이에 대한 주요 방어 수단입니다.

기능의 분류에 대해 제안된 변경 사항은 그룹 리더가 결정한 대로 HotSpot 그룹 구성원의 대략적인 합의에 의해 승인됩니다. 이러한 변경 사항은 스타일 가이드 업데이트에 문서화되어야 합니다.

C++11 및 C++14의 새로운 기능 목록과 해당 설명에 대한 링크는 일부 컴파일러 및 라이브러리에 대한 온라인 설명서에서 찾을 수 있습니다.

* [C++ Standards Support in GCC](https://gcc.gnu.org/projects/cxx-status.html)
* [C++ Support in Clang](https://clang.llvm.org/cxx_status.html)
* [Visual C++ Language Conformance](https://docs.microsoft.com/en-us/cpp/overview/visual-cpp-language-conformance?view=msvc-170)
* [libstdc++ Status](https://gcc.gnu.org/onlinedocs/libstdc++/manual/status.html)
* [libc++ Status](https://libcxx.llvm.org/cxx1y_status.html)

일반적으로 코드 작성, 특히 코드 읽기를 단순화하는 기능을 허용하는 것이 좋습니다.

HotSpot은 C++ 표준 라이브러리 사용을 거의 피했습니다. 그 이유 중 일부는 더 이상 사용되지 않을 수 있지만(특히 초기 버전에서 발생한 버그), 다른 일부는 여전히 적용할 수 있습니다(종속성 최소화). 표준 라이브러리의 조각을 분류하는 것은 언어 기능과 동일한 프로세스를 거쳐야 합니다.

HotSpot에 대한 초기 기능 분류 세트는 다음과 같습니다.

### JEP 357:	Migrate from Mercurial to Git

OpenJDK 커뮤니티의 소스 코드 저장소를 Mercurial(hg)에서 Git으로 마이그레이션하십시오.

#### Goals

* Mercurial에서 Git으로 모든 단일 저장소 OpenJDK 프로젝트 마이그레이션
* 태그를 포함한 모든 버전 관리 기록 보존
* Git 모범 사례에 따라 커밋 메시지 다시 형식 지정
* `jcheck`, `webrev` 및 `defpath` 도구를 Git으로 이식
* Mercurial과 Git 해시 간에 변환하는 도구 만들기

#### Description

우리는 이미 Mercurial 저장소를 Git 저장소로 변환하는 프로그램을 프로토타입했습니다. `git-fast-import` 프로토콜을 사용하여 Mercurial 변경 집합을 Git으로 가져오고 Git 모범 사례에 맞게 기존 커밋 메시지를 조정합니다. Mercurial `jdk/jdk` 저장소에 대한 커밋 메시지는 다음과 같은 구조를 갖습니다.

```
JdkHgCommitMessage : BugIdLine+ SummaryLine? ReviewersLine ContributedByLine?
BugIdLine : /[0-9]{8}/ ": " Text
SummaryLine : "Summary: " Text
ReviewersLine : "Reviewed-by: " Username (", " Username)* "\n"
ContributedByLine : "Contributed-by: " Text
Username : /[a-z]+/
Text : /[^\n]+/ "\n"
```

Git `jdk/jdk` 저장소에 대한 커밋 메시지는 약간 다른 구조를 갖습니다.

```
JdkGitCommitMessage : BugIdLine+ Body? Trailers
BugIdLine : /[0-9]{8}/ ": " Text
Body : BlankLine Text*
Trailers : BlankLine Co-authors? Reviewers
Co-authors : (BlankLine Co-author )+
Co-author : "Co-authored-by: " Real-name <Email>
Reviewers : "Reviewed-by: " Username (", " Username)* "\n"
BlankLine = "\n"
Username : /[a-z]+/
Text : /[^\n]+/ "\n"
```

메시지 구조를 변경하는 이유는 다음과 같습니다.

* Git CLI 도구에서는 제목(한 줄 뒤에 빈 줄)을 사용하는 것이 좋습니다.
* 그런 다음 제목을 사용하면 자유 형식 본문이 가능합니다.
* Git 생태계는 예고편, 즉 줄바꿈으로 본문과 분리된 줄을 인식합니다. 예를 들어 GitHub와 GitLab은 모두 공동 작성자: 트레일러를 인식하고 커밋에 여러 작성자가 있음을 인식합니다.

Git은 커밋 메타데이터의 추가 필드를 사용하여 작성자와 구별되는 커밋 커미터를 나타냅니다. 후원자를 나타내기 위해 커미터 필드를 사용할 것입니다. 후원 커밋의 경우 작성자는 커밋의 작성자 필드에 이름이 지정되고 후원자는 커미터 필드에 이름이 지정됩니다. 스폰서도 공동 작성자인 경우 적절한 공동 작성자 예고편이 추가되며 이는 기존 Mercurial 메시지 구조에서 캡처할 수 없는 상황입니다.

개별 커미터 필드의 또 다른 가능한 용도는 기능 릴리스에서 업데이트 릴리스까지 백포트 커밋을 식별하는 것입니다. 일반적으로 원래 커밋의 작성자가 아닌 다른 사람이 수행합니다.

모든 커밋 작성자가 OpenJDK 작성자가 아니기 때문에 작성자 및 커미터 필드의 내용은 `Real-name <Email>` 형식이 됩니다. 작성자 또는 커미터가 OpenJDK 작성자임을 나타내기 위해 특수 이메일 주소가 사용됩니다: `<openjdk-username>@openjdk.org.`

다음은 Git 커밋 메시지의 예입니다.

```
76543210: Crash when starting the JVM

Fixed a tricky race condition when the JVM is starting up by using a Mutex.

Co-authored-by: Robin Westberg <rwestberg@openjdk.org>
Reviewed-by: darcy
```

이러한 커밋의 작성자 및 커미터 필드는 다음과 같습니다.

```
Author: Erik Duveblad <ehelin@openjdk.org>
Commit: Erik Duveblad <ehelin@openjdk.org>
```

변환 프로세스에서 작성자가 기여자: 행에 나열되지 않으면 커밋이 후원된 것으로 간주됩니다. 이 경우 기부자: 라인의 첫 번째 사람이 저자로, 후원자가 커미터로, 추가 기여자가 공동 저자로 간주됩니다.

변환된 리포지토리의 예는 https://github.com/openjdk/ 에서 사용할 수 있습니다.

### JEP 369:	Migrate to GitHub

GitHub에서 OpenJDK 커뮤니티의 Git 리포지토리를 호스팅합니다. [JEP 357(Migrate from Mercurial to Git)](https://openjdk.java.net/jeps/357)과 함께 JDK 기능 릴리스 및 버전 11 이상용 JDK 업데이트 릴리스를 포함하여 모든 단일 리포지토리 OpenJDK 프로젝트를 GitHub로 마이그레이션합니다.

#### Goals

* https://github.com/openjdk/에서 모든 OpenJDK Git 리포지토리를 호스팅합니다.
* 모든 푸시 전에 사전 커밋 검사(`jcheck`)를 실행합니다.
* 기존 OpenJDK 서비스를 통합합니다.
* GitHub와 상호 작용하는 다양한 방법을 활성화합니다.
* 기존 이메일 및 `webrev` 기반 워크플로와 구조적으로 유사한 워크플로가 지원되는지 확인합니다.
* 모든 메타데이터를 보존하고 보관합니다.
* OpenJDK 커뮤니티가 항상 다른 소스 코드 호스팅 제공자로 이동할 수 있는지 확인하십시오.
* 개발자가 기여하기 위해 OpenJDK 특정 도구를 설치하도록 요구하지 마십시오.
* OpenJDK [Bylaws](https://openjdk.java.net/bylaws) 변경하지 마십시오.
* OpenJDK [Census](https://openjdk.java.net/census) 변경하지 마십시오.

### JEP 376:	ZGC: Concurrent Thread-Stack Processing

ZGC 스레드 스택 처리를 `safepoint`에서 동시 단계로 이동합니다.

#### Goals 

* ZGC safepoints에서 스레드 스택 처리를 제거합니다.
* 스택 처리를 lazy, cooperative, concurrent, incremental으로 만듭니다.
* ZGC safepoints에서 다른 모든 스레드별 루트 처리를 제거합니다.
* 다른 HotSpot 하위 시스템이 스택을 느리게 처리할 수 있는 메커니즘을 제공합니다.

#### Description

스택 워터마크 장벽으로 스택 스캐닝 문제를 해결할 것을 제안합니다. GC safepoint는 전역 변수를 뒤집어 Java 스레드 스택을 논리적으로 무효화합니다. 무효화된 각 스택은 동시에 처리되어 처리해야 할 항목을 추적합니다. 각 스레드가 safepoint에서 깨어나면 일부 epoch 카운터를 비교하여 스택이 유효하지 않음을 알게 되므로 스택 스캔 상태를 추적하기 위해 스택 워터마크를 설치합니다. 스택 워터마크를 사용하면 주어진 프레임이 워터마크 위에 있는지(스택이 아래쪽으로 증가한다고 가정) 구분할 수 있으므로 오래된 개체 참조가 포함될 수 있으므로 Java 스레드에서 사용해서는 안 됩니다.

프레임을 팝하거나 스택의 마지막 프레임 아래로 이동하는 모든 작업(예: 스택 워커, 반환 및 예외)에서 후크는 일부 스택 로컬 주소를 워터마크와 비교합니다. (이 스택 로컬 주소는 사용 가능한 경우 프레임 포인터이거나 프레임 포인터가 최적화되어 있지만 프레임이 상당히 일정한 크기를 갖는 컴파일된 프레임에 대한 스택 포인터일 수 있습니다.) 워터마크 위에 있을 때 느린 경로는 다음으로 이동합니다. 프레임 내의 개체 참조를 업데이트하고 워터마크를 위쪽으로 이동하여 한 프레임을 수정합니다. 오늘날처럼 빠르게 반환하기 위해 스택 워터마크 장벽은 약간 수정된 safepoint 폴링을 사용합니다. 새로운 폴은 safepoint(또는 실제로 스레드 로컬 핸드셰이크)가 보류 중일 때뿐만 아니라 아직 수정되지 않은 프레임으로 돌아갈 때도 느린 경로를 사용합니다. 단일 조건 분기를 사용하여 컴파일된 메서드에 대해 인코딩할 수 있습니다.

스택 워터마크의 불변은 스택의 마지막 프레임인 호출 수신자가 주어지면 호출 수신자와 호출자가 모두 처리된다는 것입니다. 이를 보장하기 위해 safepoint에서 깨어날 때 스택 워터마크 상태가 설치되면 호출자와 호출 수신자가 모두 처리됩니다. 호출 수신자가 준비되어 있으므로 해당 호출 수신자가 반환하면 호출자에 대한 추가 처리가 트리거되고 무장 프레임이 호출자에게 이동하는 식입니다. 따라서 프레임 풀기 또는 걷기에 의해 트리거된 처리는 풀기 또는 걷기 중인 프레임 위의 두 프레임에서 항상 발생합니다. 이것은 호출자가 소유해야 하지만 호출 수신자가 사용하는 인수의 전달을 단순화합니다. 호출자와 호출 수신자 프레임(따라서 추가 스택 인수) 모두 자유롭게 액세스할 수 있습니다.

Java 스레드는 실행을 계속하는 데 필요한 최소 프레임 수를 처리합니다. 동시 GC 스레드는 나머지 프레임을 처리하여 모든 스레드 스택과 기타 스레드 루트가 결국 처리되도록 합니다. 스택 워터마크 장벽을 사용하는 동기화는 GC가 처리하는 동안 Java 스레드가 프레임으로 반환되지 않도록 합니다.

### JEP 380:	Unix-Domain Socket Channels

`java.nio.channels` 패키지의 소켓 채널 및 서버 소켓 채널 API에 Unix 도메인(AF_UNIX) 소켓 지원을 추가합니다. 상속된 채널 메커니즘을 확장하여 Unix 도메인 소켓 채널 및 서버 소켓 채널을 지원합니다.

#### Goals

Unix 도메인 소켓은 동일한 호스트에서 IPC(프로세스 간 통신)에 사용됩니다. 인터넷 프로토콜(IP) 주소와 포트 번호가 아닌 파일 시스템 경로 이름으로 주소가 지정된다는 점을 제외하면 대부분의 면에서 TCP/IP 소켓과 유사합니다. 이 JEP의 목표는 주요 Unix 플랫폼 및 Windows에서 공통적인 Unix 도메인 소켓의 모든 기능을 지원하는 것입니다. Unix 도메인 소켓 채널은 읽기/쓰기 동작, 연결 설정, 서버에서 들어오는 연결 수락, 선택기에서 선택 가능한 다른 비차단 채널과의 다중화 및 관련 소켓 지원 측면에서 기존 TCP/IP 채널과 동일하게 작동합니다. 옵션.

#### Description

Unix 도메인 소켓 채널을 지원하기 위해 다음 API 요소를 추가합니다.

* 새로운 소켓 주소 클래스, `java.net.UnixDomainSocketAddress;`
* 기존 `java.net.StandardProtocolFamily` 열거형의 UNIX 상수 값입니다.
* 프로토콜 패밀리를 지정하는 `SocketChannel` 및 `ServerSocketChannel`의 새로운 개방형 팩토리 메서드
* Unix 도메인 소켓에 대한 채널이 작동하는 방식을 지정하기 위해 SocketChannel 및 ServerSocketChannel 사양이 업데이트되었습니다.

### JEP 386:	Alpine Linux Port

JDK를 Alpine Linux 및 x64 및 AArch64 아키텍처 모두에서 musl을 기본 C 라이브러리로 사용하는 다른 Linux 배포판으로 이식합니다.

### JEP 387:	Elastic Metaspace

사용하지 않은 HotSpot 클래스 메타데이터(즉, 메타스페이스) 메모리를 운영 체제에 보다 신속하게 반환하고, 메타스페이스 공간을 줄이고, 메타스페이스 코드를 단순화하여 유지 관리 비용을 줄입니다.

#### Description

기존 메타 공간 메모리 할당자를 버디 기반 할당 방식으로 교체할 것을 제안합니다. 이것은 예를 들어 Linux 커널에서 성공적으로 사용된 오래되고 입증된 알고리즘입니다. 이 방식을 사용하면 메타스페이스 메모리를 더 작은 청크로 할당하는 것이 실용적이므로 클래스 로더 오버헤드가 줄어듭니다. 또한 단편화를 줄여 사용하지 않은 메타 공간 메모리를 운영 체제로 반환하여 탄력성을 향상시킬 수 있습니다.

또한 요청 시 운영 체제에서 경기장으로 메모리를 느리게 커밋합니다. 이렇게 하면 대규모 경기장으로 시작하지만 즉시 사용하지 않거나 최대 범위로 사용하지 않을 수 있는 로더(예: 부트 클래스 로더)의 공간이 줄어듭니다.

마지막으로, 버디 할당이 제공하는 탄력성을 최대한 활용하기 위해 메타스페이스 메모리를 서로 독립적으로 커밋 및 커밋되지 않을 수 있는 균일한 크기의 알갱이로 정렬합니다. 이러한 그래뉼의 크기는 가상 메모리 단편화를 제어하는 ​​간단한 방법을 제공하는 새로운 명령줄 옵션으로 제어할 수 있습니다.

새로운 알고리즘을 자세히 설명하는 문서는 여기에서 찾을 수 있습니다. 작동하는 프로토타입은 JDK 샌드박스 저장소에 분기로 존재합니다.

### JEP 388:	Windows/AArch64 Port

JDK를 Windows/AArch64로 이식합니다.

#### Description

이전에 Linux/AArch64 포트(JEP 237)에 대해 수행한 작업을 확장하여 JDK를 Windows/AArch64로 이식했습니다. 이 포트에는 템플릿 인터프리터, C1 및 C2 JIT 컴파일러, 가비지 수집기(직렬, 병렬, G1, Z 및 Shenandoah)가 포함됩니다. Windows 10 및 Windows Server 2016 운영 체제를 모두 지원합니다.

이 JEP의 초점은 이식 노력 자체(대부분 완료)가 아니라 JDK 메인 라인 저장소로의 포트 통합입니다.

현재 12개가 조금 넘는 변경 집합이 있습니다. 공유 코드의 변경 사항을 최소한으로 유지했습니다. 변경 사항은 AArch64 메모리 모델 지원을 Windows로 확장하고, 일부 MSVC 문제를 해결하고, AArch64 포트에 LLP64 지원을 추가하고, Windows에서 CPU 기능 감지를 수행합니다. 또한 크로스 컴파일 및 Windows 도구 모음을 더 잘 지원하도록 빌드 스크립트를 수정했습니다.

새로운 플랫폼 코드 자체는 15개(+4) 파일과 1222줄(+322)로 제한됩니다.

조기 액세스 바이너리는 여기에서 사용할 수 있습니다.

### JEP 389:	Foreign Linker API (Incubator)

네이티브 코드에 대한 정적 유형의 순수 Java 액세스를 제공하는 API를 소개합니다. 이 API는 외부 메모리 API([JEP 393](https://openjdk.java.net/jeps/389))와 함께 오류가 발생하기 쉬운 기본 라이브러리에 바인딩하는 프로세스를 상당히 단순화합니다.

#### History

이 JEP의 기반을 제공하는 외부 메모리 액세스 API는 [JEP 370](https://openjdk.java.net/jeps/370)에서 처음 제안되었으며 2019년 말에 인큐베이팅 API로 Java 14를 대상으로 했으며 이후 Java를 대상으로 하는 [JEP 383](https://openjdk.java.net/jeps/383) 및 [JEP 393](https://openjdk.java.net/jeps/393)에 의해 새로 고쳐졌습니다. 각각 15와 16. 외부 메모리 액세스 API와 외부 링커 API는 함께 프로젝트 파나마의 주요 결과물을 구성합니다.

#### Goals

* ***Ease of use***: JNI를 우수한 순수 Java 개발 모델로 교체하십시오.
* ***C support***: 이 노력의 초기 범위는 x64 및 AArch64 플랫폼에서 C 라이브러리와 고품질의 완전히 최적화된 상호 운용성을 제공하는 것을 목표로 합니다.
* ***Generality***: 외부 링커 API 및 구현은 시간이 지남에 따라 다른 플랫폼(예: 32비트 x86) 및 C 이외의 언어(예: C++, Fortran)로 작성된 외부 기능에 대한 지원을 수용할 수 있을 만큼 충분히 유연해야 합니다.
* ***Performance***: 외부 링커 API는 JNI와 비슷하거나 더 나은 성능을 제공해야 합니다.

#### Description 

이 섹션에서는 외부 링커 API를 사용하여 기본 상호 운용성을 달성하는 방법에 대해 자세히 설명합니다. 이 섹션에서 설명하는 다양한 추상화는 `jdk.incubator.foreign`이라는 인큐베이터 모듈로 동일한 이름의 패키지로 기존 외부 메모리 액세스 API와 나란히 제공됩니다

##### Symbol lookups

외부 함수 지원의 첫 번째 요소는 기본 라이브러리에서 기호를 조회하는 메커니즘입니다. 기존 Java/JNI 시나리오에서 이는 내부적으로 `dlopen` 호출에 매핑되는 `System::loadLibrary` 및 `System::load` 메서드를 통해 수행됩니다. 외부 링커 API는 `LibraryLookup` 클래스(메서드 핸들 조회와 유사)를 통해 간단한 라이브러리 조회 추상화를 제공하며, 이는 주어진 기본 라이브러리에서 명명된 기호를 조회하는 기능을 제공합니다. 세 가지 다른 방법으로 라이브러리 조회를 얻을 수 있습니다.

* `LibraryLookup::ofDefault` — VM과 함께 로드된 모든 기호를 볼 수 있는 라이브러리 조회를 반환합니다.
* `LibraryLookup::ofPath` — 주어진 절대 경로에서 찾은 라이브러리와 관련된 라이브러리 조회를 생성합니다.
* `LibraryLookup::ofLibrary` — 주어진 이름을 가진 라이브러리와 연관된 라이브러리 조회를 생성합니다(이를 위해서는 `java.library.path` 변수를 적절하게 설정해야 할 수도 있습니다).

조회가 확보되면 클라이언트는 조회를 사용하여 `lookup(String)` 메서드를 사용하여 전역 변수 또는 함수와 같은 라이브러리 기호에 대한 핸들을 검색할 수 있습니다. 이 메서드는 메모리 주소와 이름에 대한 프록시일 뿐인 새로운 `LibraryLookup.Symbol`을 반환합니다.

예를 들어 다음 코드는 `clang` 라이브러리에서 제공하는 `clang_getClangVersion` 함수를 조회합니다.

```java
LibraryLookup libclang = LibraryLookup.ofLibrary("clang");
LibraryLookup.Symbol clangVersion = libclang.lookup("clang_getClangVersion");
```

외부 링커 API의 라이브러리 로딩 메커니즘과 JNI의 메커니즘 간의 중요한 차이점 중 하나는 로드된 JNI 라이브러리가 클래스 로더와 연관된다는 것입니다. 또한 클래스 로더 무결성을 유지하기 위해 동일한 JNI 라이브러리를 둘 이상의 클래스 로더에 로드할 수 없습니다. 여기에 설명된 외부 기능 메커니즘은 더 원시적입니다. 외부 링커 API를 사용하면 클라이언트가 개입하는 JNI 코드 없이 기본 라이브러리를 직접 대상으로 지정할 수 있습니다. 결정적으로 Java 객체는 외부 링커 API에 의해 네이티브 코드로 전달되거나 전달되지 않습니다. 이 때문에 `LibraryLookup`을 통해 로드된 라이브러리는 클래스 로더에 연결되지 않고 필요한 만큼 (재)로드될 수 있습니다.

##### The C linker

CLinker 인터페이스는 API의 외부 기능 지원의 기초입니다.

```java
interface CLinker {
    MethodHandle downcallHandle(LibraryLookup.Symbol func,
                                MethodType type,
                                FunctionDescriptor function);
    MemorySegment upcallStub(MethodHandle target,
                             FunctionDescriptor function);
}
```

이 추상화는 이중 역할을 합니다. 첫째, 하향 호출(예: Java에서 원시 코드로의 호출)의 경우 `downcallHandle` 메소드를 사용하여 원시 함수를 일반 `MethodHandle` 객체로 모델링할 수 있습니다. 둘째, 상향 호출(예: 네이티브에서 Java 코드로의 호출)의 경우 `upcallStub` 메소드를 사용하여 기존 `MethodHandle`(일부 Java 메소드를 가리킬 수 있음)을 `MemorySegment`로 변환할 수 있습니다. 함수 포인터. CLinker 추상화는 주로 C 언어에 대한 상호 운용 지원을 제공하는 데 중점을 두고 있지만 이 추상화의 개념은 미래에 다른 외국어에도 적용할 수 있을 만큼 충분히 일반적입니다.

`downcallHandle` 및 `upcallStub`은 모두 외부 함수의 서명을 전체적으로 설명하는 데 사용되는 메모리 레이아웃의 집합체인 `FunctionDescriptor` 인스턴스를 사용합니다. CLinker 인터페이스는 각 기본 C 기본 유형에 대해 하나씩 많은 레이아웃 상수를 정의합니다. 이러한 레이아웃은 `FunctionDescriptor`를 사용하여 결합하여 C 함수의 서명을 설명할 수 있습니다. 예를 들어 다음 설명자를 사용하여 `char*`를 취하고 `long`을 반환하는 C 함수를 모델링할 수 있습니다.

```java
FunctionDescriptor func
    = FunctionDescriptor.of(CLinker.C_LONG, CLinker.C_POINTER);
```

`downcallHandle` 및 `upcallStub` 모두 `MethodType` 인스턴스를 (직접적으로 또는 간접적으로) 수락합니다. 메소드 유형은 생성된 하향 호출 핸들 또는 상향 호출 스텁과 상호 작용할 때 클라이언트가 사용할 Java 서명을 설명합니다. `MethodType` 인스턴스의 인수 및 반환 형식은 해당 레이아웃에 대해 유효성이 검사됩니다. 예를 들어, 링커 런타임은 주어진 인수/반환 값과 연관된 Java 캐리어의 크기가 해당 레이아웃의 크기와 동일한지 확인합니다. 기본 레이아웃을 Java 캐리어에 매핑하는 것은 플랫폼마다 다를 수 있지만(예: `C_LONG`은 Linux/x64에서는 `long`으로 매핑되지만 Windows에서는 `int`로 매핑됨) 포인터 레이아웃(`C_POINTER`)은 항상 `MemoryAddress` 캐리어 및 구조체( 레이아웃이 `GroupLayout`에 의해 정의됨)은 항상 `MemorySegment` 캐리어와 연결됩니다.

##### Downcalls

표준 C 라이브러리에 정의된 다음 함수를 호출한다고 가정합니다.

```c++
size_t strlen(const char *s);
```

그렇게 하려면 다음을 수행해야 합니다.

* `strlen` 기호 조회,
* CLinker 클래스의 레이아웃을 사용하여 C 함수의 서명을 설명하고,
* 기본 기능에 오버레이할 Java 서명을 선택합니다(기본 메서드 핸들의 클라이언트가 상호 작용할 서명이 됨).
* `CLinker::downcallHandle`을 사용하여 위의 정보로 다운콜 네이티브 메서드 핸들을 만듭니다.

다음은 이를 수행하는 방법의 예입니다.

```java
MethodHandle strlen = CLinker.getInstance().downcallHandle(
        LibraryLookup.ofDefault().lookup("strlen"),
        MethodType.methodType(long.class, MemoryAddress.class),
        FunctionDescriptor.of(C_LONG, C_POINTER)
    );
```

`strlen` 함수는 VM과 함께 로드되는 표준 C 라이브러리의 일부이므로 기본 조회를 사용하여 조회할 수 있습니다. 나머지는 매우 간단합니다. 유일한 까다로운 세부 사항은 `size_t`를 모델링하는 방법입니다. 일반적으로 이 유형은 포인터 크기이므로 Linux에서는 `C_LONG`을 사용할 수 있지만 Windows에서는 `C_LONG_LONG`을 사용해야 합니다. Java 측에서는 `long`을 사용하여 `size_t`를 모델링하고 `MemoryAddress` 매개변수를 사용하여 포인터를 모델링합니다.

다운콜 네이티브 메서드 핸들을 얻으면 다른 메서드 핸들로 사용할 수 있습니다.

```java
try (MemorySegment str = CLinker.toCString("Hello")) {
   long len = strlen.invokeExact(str.address()); // 5
}
```

여기에서 CLinker의 도우미 메서드 중 하나를 사용하여 Java 문자열을 NULL로 끝나는 C 문자열을 포함하는 오프 힙 메모리 세그먼트로 변환합니다. 그런 다음 해당 세그먼트를 메서드 핸들에 전달하고 결과를 Java long에 저장합니다.

이 모든 것이 개입하는 네이티브 코드 없이 가능했다는 점에 유의하십시오. 모든 상호 운용 코드는 (낮은 수준) Java로 표현될 수 있습니다.

##### Upcalls

때로는 Java 코드를 일부 기본 함수에 대한 함수 포인터로 전달하는 것이 유용합니다. 업콜에 대한 외부 링커 지원을 사용하여 이를 달성할 수 있습니다. 이를 증명하기 위해 표준 C 라이브러리에 정의된 다음 함수를 고려하십시오.

```c++
void qsort(void *base, size_t nmemb, size_t size,
           int (*compar)(const void *, const void *));
```

이것은 함수 포인터로 전달되는 사용자 지정 비교기 함수인 `compar`를 사용하여 배열의 내용을 정렬하는 데 사용할 수 있는 함수입니다. Java에서 `qsort` 함수를 호출할 수 있으려면 먼저 이에 대한 다운콜 네이티브 메소드 핸들을 생성해야 합니다.

```java
MethodHandle qsort = CLinker.getInstance().downcallHandle(
        LibraryLookup.ofDefault().lookup("qsort"),
        MethodType.methodType(void.class, MemoryAddress.class, long.class,
                              long.class, MemoryAddress.class),
        FunctionDescriptor.ofVoid(C_POINTER, C_LONG, C_LONG, C_POINTER)
    );
```

이전과 같이 `C_LONG` 및 `long.class`를 사용하여 C `size_t` 유형을 매핑하고 첫 번째 포인터 매개변수(배열 포인터)와 마지막 매개변수(함수 포인터) 모두에 `MemoryAddess.class`를 사용합니다.

이번에는 `qsort` 다운콜 핸들을 호출하기 위해 마지막 매개변수로 전달할 함수 포인터가 필요합니다. 이것은 기존 메소드 핸들에서 함수 포인터를 생성할 수 있게 해주기 때문에 외부 링커 추상화의 상향 호출 지원이 편리한 곳입니다. 먼저 포인터로 전달된 두 개의 `int` 요소를 비교할 수 있는 정적 메서드를 작성합니다.

```java
class Qsort {
    static int qsortCompare(MemoryAddress addr1, MemoryAddress addr2) {
            return MemoryAccess.getIntAtOffset(MemorySegment.ofNativeRestricted(), 
                                               addr1.toRawLongValue()) - 
                   MemoryAccess.getIntAtOffset(MemorySegment.ofNativeRestricted(),
                                               addr2.toRawLongValue());
    }
}
```

그런 다음 위의 비교기 함수를 가리키는 메서드 핸들을 만듭니다.

```java
MethodHandle comparHandle
    = MethodHandles.lookup()
                   .findStatic(Qsort.class, "qsortCompare",
                               MethodType.methodType(int.class,
                                                     MemoryAddress.class,
                                                     MemoryAddress.class));
```

이제 Java 비교기에 대한 메서드 핸들이 있으므로 함수 포인터를 만들 수 있습니다. 다운콜과 마찬가지로 CLinker 클래스의 레이아웃을 사용하여 외부 함수 포인터의 서명을 설명합니다.

```java
MemorySegment comparFunc
    = CLinker.getInstance().upcallStub(comparHandle,
                                            FunctionDescriptor.of(C_INT,
                                                                  C_POINTER,
                                                                  C_POINTER));
);
```

마지막으로 메모리 세그먼트 `comparFunc`가 있습니다. 이 세그먼트의 기본 주소는 Java 비교기 기능을 호출하는 데 사용할 수 있는 스텁을 가리키므로 이제 `qsort` 다운콜 핸들을 호출하는 데 필요한 모든 것이 있습니다.

```java
try (MemorySegment array = MemorySegment.allocateNative(4 * 10)) {
    array.copyFrom(MemorySegment.ofArray(new int[] { 0, 9, 3, 4, 6, 5, 1, 8, 2, 7 }));
    qsort.invokeExact(array.address(), 10L, 4L, comparFunc.address());
    int[] sorted = array.toIntArray(); // [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
}
```

이 코드는 오프 힙 배열을 만들고 Java 배열의 내용을 복사한 다음 외부 링커에서 얻은 비교기 함수와 함께 배열을 qsort 핸들에 전달합니다. 부작용으로 호출 후 오프 힙 배열의 내용은 Java로 작성된 비교기 기능에 따라 정렬됩니다. 그런 다음 정렬된 요소가 포함된 세그먼트에서 새 Java 배열을 추출합니다.

이 고급 예제는 Java/네이티브 경계를 넘어 코드와 데이터의 완전한 양방향 상호 운용을 통해 외부 링커 추상화의 모든 기능을 보여줍니다.

### JEP 390:	Warnings for Value-Based Classes

기본 래퍼 클래스를 값 기반으로 지정하고 제거를 위해 해당 생성자를 더 이상 사용하지 않으며, 새로운 사용 중단 경고가 표시됩니다. Java 플랫폼에서 값 기반 클래스의 인스턴스에서 동기화하려는 부적절한 시도에 대한 경고를 제공합니다.

#### Description

`java.lang`의 기본 래퍼 클래스(`Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Boolean` 및 `Character`)는 값 기반으로 지정되었습니다. 값 기반 클래스에 대한 설명은 더 이상 사용되지 않는 생성자 및 내부 팩토리를 허용하고 기본 클래스 마이그레이션 요구 사항과 더 잘 일치하도록 업데이트되었습니다(예: 값 기반 클래스는 인스턴스 필드를 상속해서는 안 됨).

값 기반 클래스 인스턴스의 오용을 방지하려면:

Java 9에서 원래 사용되지 않는 기본 래퍼 클래스 생성자는 제거를 위해 사용되지 않습니다. 생성자가 소스에서 호출될 때마다 `javac`는 기본적으로 제거 경고를 생성합니다. `jdeprscan` 도구는 바이너리에서 더 이상 사용되지 않는 API의 사용을 식별하는 데 사용할 수 있습니다.

`javac`는 값 기반 클래스 유형 또는 하위 유형이 모두 값 기반으로 지정된 유형의 피연산자로 동기화된 문의 사용법을 식별하는 새로운 경고 범주인 동기화를 구현합니다. 경고 범주는 기본적으로 켜져 있으며 `-Xlint:synchronization을` 사용하여 수동으로 선택할 수 있습니다.

HotSpot은 값 기반 클래스 인스턴스에서 발생하는 `monitorenter`의 런타임 감지를 구현합니다. 명령줄 옵션 `-XX:DiagnoseSyncOnValueBasedClasses=1`은 작업을 치명적인 오류로 처리합니다. 명령줄 옵션 `-XX:DiagnoseSyncOnValueBasedClasses=2`는 콘솔과 JDK Flight Recorder 이벤트를 통해 로깅을 켭니다.

컴파일 시간 동기화 경고는 정적 유형에 따라 달라지지만 런타임 경고는 개체와 같은 값 기반이 아닌 클래스 및 인터페이스 유형에 대한 동기화에 응답할 수 있습니다.

예를 들어:

```java
Double d = 20.0;
synchronized (d) { ... } // javac warning & HotSpot warning
Object o = d;
synchronized (o) { ... } // HotSpot warning
```

`Monitorexit` 바이트코드 및 `Object` 메소드 `wait`, `notify` 및 `notifyAll`은 동기화된 명령문 또는 메소드 외부에서 호출되는 경우 항상 `IllegalMonitorStateException`을 발생시켰습니다. 따라서 이러한 작업에 대한 경고가 필요하지 않습니다.

##### Identifying value-based classes

JDK 내에서 `@jdk.internal.ValueBased` 주석은 클래스가 값 기반이거나 추상 클래스 또는 인터페이스에 값 기반 하위 클래스가 필요하다는 신호를 `javac` 및 HotSpot에 보내는 데 사용됩니다.

`@ValueBased`는 Java Platform API 및 JDK의 다음 선언에 적용됩니다.

* `java.lang`의 원시 래퍼 클래스.
* 클래스 `java.lang.Runtime.Version;`
* `java.util`의 `Optional` 클래스: `Optional`, `OptionalInt`, `OptionalLong` 및 `OptionalDouble`;
* `java.time` API의 많은 클래스: `Instant`, `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, `ZoneId`, `OffsetTime`, `OffsetDateTime`, `ZoneOffset`, `Duration`, `Period`, `Year`, `YearMonth` 및 `MonthDay` 및 `java.time.chrono`에서: `MinguoDate`, `HijrahDate` , `JapaneseDate` 및 `ThaiBuddhistDate`;
* 인터페이스 `java.lang.ProcessHandle` 및 해당 구현 클래스.
`java.util`에 있는 컬렉션 팩토리의 구현 클래스: `List.of`, `List.copyOf`, `Set.of`, `Set.copyOf`, `Map.of`, `Map.copyOf`, `Map.ofEntries` 및 `Map.entry`.

주석이 추상 클래스나 인터페이스에 적용될 때마다 JDK의 모든 하위 클래스에도 적용됩니다.

`java.lang.constant` 및 `jdk.incubator.foreign`의 일부 클래스 및 인터페이스는 값 기반이라고 주장했지만 수정된 요구 사항을 충족하지 않습니다(예: 인스턴스 필드 상속). 따라서 기본 클래스로 마이그레이션할 수 없습니다. 이 경우 더 이상 가치 기반 클래스로 설명하는 것이 적절하지 않으며 사양이 수정되었습니다.

##### Scope of changes

Java SE: 이 JEP는 기본 래퍼 클래스, 기존 값 기반 클래스, 관련 인터페이스 및 팩토리 메서드의 사양을 개선하여 Java SE를 수정합니다. 또한 기본 래퍼 클래스 생성자 제거에 대해 더 이상 사용되지 않습니다. Java 언어 또는 Java 가상 머신 사양을 변경하지 않습니다.

JDK: JDK에서 이 JEP는 또한 `javac` 및 HotSpot에 새로운 경고 및 로깅 기능을 추가합니다. 그리고 `@jdk.internal.ValueBased` 주석을 정의하고 여러 JDK 클래스에 적용합니다.

### JEP 392:	Packaging Tool

자체 포함된 Java 애플리케이션을 패키징하기 위한 `jpackage` 도구를 제공합니다.

#### Goals

레거시 JavaFX javapackager 도구를 기반으로 다음과 같은 패키징 도구를 만듭니다.

* 최종 사용자에게 자연스러운 설치 환경을 제공하기 위해 기본 패키징 형식을 지원합니다. 이러한 형식에는 Windows의 msi 및 exe, macOS의 pkg 및 dmg, Linux의 deb 및 rpm이 포함됩니다.
* 패키징 시 시작 시간 매개변수를 지정할 수 있습니다.
* 명령줄에서 직접 호출하거나 ToolProvider API를 통해 프로그래밍 방식으로 호출할 수 있습니다.

#### Description

`jpackage` 도구는 필요한 모든 종속성을 포함하는 플랫폼별 패키지로 Java 애플리케이션을 패키징합니다. 응용 프로그램은 일반 JAR 파일 모음 또는 모듈 모음으로 제공될 수 있습니다. 지원되는 플랫폼별 패키지 형식은 다음과 같습니다.

* Linux: deb 및 rpm
* macOS: pkg 및 dmg
* Windows: msi 및 exe

기본적으로 `jpackage`는 실행되는 시스템에 가장 적합한 형식으로 패키지를 생성합니다.

##### Basic usage: Non-modular applications

JAR 파일로 구성된 애플리케이션이 모두 `lib`라는 디렉토리에 있고 `lib/main.jar`에 기본 클래스가 포함되어 있다고 가정합니다. 그런 다음 아래 커맨드를 사용합니다.

```
$ jpackage --name myapp --input lib --main-jar main.jar
```

로컬 시스템의 기본 형식으로 애플리케이션을 패키징하고 결과 패키지 파일은 현재 디렉토리에 남겨둡니다. `main.jar`의 `MANIFEST.MF` 파일에 `Main-Class` 속성이 없으면 기본 클래스를 명시적으로 지정해야 합니다.

```
$ jpackage --name myapp --input lib --main-jar main.jar \
  --main-class myapp.Main
```

패키지 이름은 myapp이지만 패키지 파일 자체의 이름은 더 길어지고 패키지 유형(예: myapp.exe)으로 끝납니다. 패키지에는 myapp이라고도 하는 응용 프로그램의 실행 프로그램이 포함됩니다. 애플리케이션을 시작하기 위해 런처는 입력 디렉토리에서 복사된 모든 JAR 파일을 JVM의 클래스 경로에 배치합니다.

기본 형식이 아닌 다른 형식으로 패키지를 생성하려면 `--type` 옵션을 사용하십시오. 예를 들어 macOS에서 dmg 파일이 아닌 pkg 파일을 생성:

```
$ jpackage --name myapp --input lib --main-jar main.jar --type pkg
```

##### Basic usage: Modular applications

`lib` 디렉토리의 모듈식 JAR 파일 및/또는 JMOD 파일로 구성된 모듈식 애플리케이션이 있고 모듈 myapp의 기본 클래스가 있는 경우 커맨드

```
$ jpackage --name myapp --module-path lib -m myapp
```
포장해 드립니다. myapp 모듈이 기본 클래스를 식별하지 않으면 다시 명시적으로 지정해야 합니다.

```
$ jpackage --name myapp --module-path lib -m myapp/myapp.Main
```

(모듈식 JAR 또는 JMOD 파일을 생성할 때 `jar` 및 `jmod` 도구에 `--main-class` 옵션을 사용하여 기본 클래스를 지정할 수 있습니다.)

##### Package metadata

두 번 이상 사용할 수 있는 `--file-associations` 옵션을 통해 애플리케이션에 대한 하나 이상의 파일 유형 연결을 정의할 수 있습니다. 이 옵션에 대한 인수는 다음 키 중 하나 이상에 대한 값이 있는 속성 파일입니다.

모든 `jpackage` 옵션에 대한 설명은 `jpackage` 매뉴얼 페이지에서 찾을 수 있습니다.

###### File associations

* `extensions`는 응용 프로그램과 연결할 파일의 확장자를 지정하고,
* `mime-type`은 애플리케이션과 연관될 파일의 ​​MIME 유형을 지정합니다.
* `icon`은 이 연관과 함께 사용하기 위해 애플리케이션 이미지 내에서 아이콘을 지정합니다.
* `description`은 연결에 대한 간단한 설명을 지정합니다.

###### Launchers

기본적으로 `jpackage` 도구는 응용 프로그램에 대한 간단한 기본 실행 프로그램을 만듭니다. 다음 옵션을 통해 기본 런처를 사용자 정의할 수 있습니다.

* `--arguments <string>` — 실행기에 명령줄 인수가 지정되지 않은 경우 기본 클래스에 전달할 명령줄 인수(이 옵션은 여러 번 사용할 수 있음)
* `--java-options <string>` — JVM에 전달할 옵션(이 옵션은 여러 번 사용할 수 있음)

애플리케이션에 추가 런처가 필요한 경우 `--add-launcher` 옵션을 통해 추가할 수 있습니다.

* `--add-launcher <런처 이름>=<파일>`

명명된 `<file>`은 하나 이상의 키 `app-version` 아이콘 인수 `java-options` `main-class` `main-jar` 모듈 또는 `win-console`에 대한 값이 있는 속성 파일이어야 합니다. 이 키의 값은 같은 이름의 옵션에 대한 인수로 해석되지만 기본 실행 프로그램이 아닌 생성되는 실행 프로그램과 관련됩니다. `--add-launcher` 옵션은 여러 번 사용할 수 있습니다.

##### Application images

`jpackage` 도구는 최종 단계에서 호출하는 플랫폼별 패키징 도구에 대한 입력으로 애플리케이션 이미지를 구성합니다. 일반적으로 이 이미지는 임시 아티팩트이지만 패키징하기 전에 사용자 지정해야 하는 경우가 있습니다. 따라서 두 단계로 `jpackage` 도구를 실행할 수 있습니다. 먼저 특수 패키지 유형 `app-image`를 사용하여 초기 애플리케이션 이미지를 생성합니다.

```
$ jpackage --name myapp --module-path lib -m myapp --type 앱 이미지
```

그러면 myapp 디렉토리에 애플리케이션 이미지가 생성됩니다. 필요에 따라 해당 이미지를 사용자 정의한 다음 `--app-image` 옵션을 통해 최종 패키지를 생성합니다.

```
$ jpackage --name myapp --app-image myapp
```

##### Runtime images

애플리케이션 이미지에는 애플리케이션을 구성하는 파일과 애플리케이션을 실행할 JDK 런타임 이미지가 모두 포함됩니다. 기본적으로 `jpackage` 도구는 `jlink` 도구를 호출하여 런타임 이미지를 생성합니다. 이미지의 내용은 애플리케이션 유형에 따라 다릅니다.

JAR 파일로 구성된 비모듈식 애플리케이션의 경우 런타임 이미지에는 일반 Java 실행 프로그램에서 명명되지 않은 모듈의 클래스 경로 애플리케이션에 제공되는 동일한 JDK 모듈 세트가 포함됩니다.

모듈식 JAR 파일 및/또는 JMOD 파일로 구성된 모듈식 애플리케이션의 경우 런타임 이미지에는 애플리케이션의 기본 모듈과 모든 종속성의 전이적 폐쇄가 포함됩니다.

`jpackage`에서 사용하는 기본 `jlink` 옵션 세트는 다음과 같습니다.

`--strip-native-commands` `--strip-debug` `--no-man-pages` `--no-header-files`
그러나 이것은 `--jlink-options` 옵션을 통해 변경할 수 있습니다. 결과 이미지에는 사용 가능한 모든 서비스 제공자가 포함되지 않습니다. 그것들을 바인딩하려면 `--jlink-options`를 사용하고 `jlink` 옵션 목록에 `--bind-services`를 포함하십시오.

두 경우 모두 런타임 이미지에 추가 모듈을 포함하려면 `jpackage` 도구의 `--add-modules` 옵션을 사용할 수 있습니다. 런타임 이미지의 모듈 목록은 이미지의 릴리스 파일에서 사용할 수 있습니다.

`jpackage` 도구로 생성된 런타임 이미지에는 `src.zip` 파일이 포함되어 있지 않습니다.

런타임 이미지를 추가로 사용자 정의하려면 `jlink`를 직접 호출하고 `--runtime-image` 옵션을 통해 결과 이미지를 `jpackage` 도구에 전달할 수 있습니다. 예를 들어, jdeps 도구를 사용하여 비모듈식 애플리케이션에 `java.base` 및 `java.sql` 모듈만 필요한지 확인했다면 패키지 크기를 크게 줄일 수 있습니다.

```
$ jlink --add-modules java.base,java.sql --출력 myjre
$ jpackage --name myapp --input lib --main-jar main.jar --runtime-image myjre
```

##### Application-image layout and content

애플리케이션 이미지의 레이아웃과 콘텐츠는 플랫폼에 따라 다릅니다. 실제 이미지에는 아래 레이아웃에 표시되지 않은 일부 파일이 포함되어 있습니다. 이러한 파일은 언제든지 변경될 수 있는 구현 세부 정보입니다.

###### Linux

```
myapp/
  bin/              // Application launcher(s)
    myapp
  lib/
    app/
      myapp.cfg     // Configuration info, created by jpackage
      myapp.jar     // JAR files, copied from the --input directory
      mylib.jar
      ...
    runtime/        // JDK runtime image
```

Linux의 기본 설치 디렉토리는 `/opt`입니다. `--install-dir` 옵션을 통해 재정의할 수 있습니다.

###### macOS

```
MyApp.app/
  Contents/
    Info.plist
    MacOS/          // Application launcher(s)
      MyApp
    Resources/      // Icons, etc.
    app/
      MyApp.cfg     // Configuration info, created by jpackage
      myapp.jar     // JAR files, copied from the --input directory
      mylib.jar
      ...
    runtime/        // JDK runtime image
```

macOS의 기본 설치 디렉토리는 `/Applications`입니다. `--install-dir` 옵션을 통해 재정의할 수 있습니다.

###### Windows

```
MyApp/
  MyApp.exe         // Application launcher(s)
  app/
    MyApp.cfg       // Configuration info, created by jpackage
    myapp.jar       // JAR files, copied from the --input directory
    mylib.jar
    ...
  runtime/          // JDK runtime image
```

Windows의 기본 설치 디렉토리는 `C:\Program Files\`입니다. `--install-dir` 옵션을 통해 재정의할 수 있습니다.

##### Delivering jpackage

`jpackage` 도구는 `jdk.jpackage`라는 모듈의 JDK에서 제공됩니다.

커맨드라인 인터페이스는 [JEP 293](https://openjdk.java.net/jeps/293)을 따릅니다.

커맨드라인 인터페이스 외에도 `jpackage`는 "`jpackage`"라는 이름으로 `ToolProvider API(java.util.spi.ToolProvider)`를 통해 액세스할 수 있습니다.

### JEP 393:	Foreign-Memory Access API (Third Incubator)

Java 프로그램이 Java 힙 외부의 외부 메모리에 안전하고 효율적으로 액세스할 수 있도록 하는 API를 도입하십시오.

#### History

Foreign-Memory Access API는 [JEP 370](https://openjdk.java.net/jeps/370)에 의해 처음 제안되었으며 2019년 후반에 인큐베이팅 API로 Java 14를 대상으로 했으며 나중에 2020년 중반에 Java 15를 대상으로 하는 [JEP 383](https://openjdk.java.net/jeps/383)에 의해 다시 인큐베이션되었습니다. 이 JEP는 기반 개선을 통합할 것을 제안합니다. 피드백을 받고 Java 16에서 API를 다시 배양합니다. 이 API 새로 고침에는 다음 변경 사항이 포함됩니다.

* `MemorySegment`와 `MemoryAddress` 인터페이스 간의 역할 구분이 명확해졌습니다.
* 간단한 경우에 VarHandle API의 필요성을 최소화하기 위해 공통 정적 메모리 접근자를 제공하는 새로운 인터페이스인 `MemoryAccess`;
* 공유 세그먼트 지원 
* `Cleaner`로 세그먼트를 등록하는 기능.

#### Goals

* ***Generality***: 단일 API는 다양한 외부 메모리(예: 기본 메모리, 영구 메모리, 관리 힙 메모리 등)에서 작동할 수 있어야 합니다.
* ***Safety***: 작동 중인 메모리의 종류에 관계없이 API가 JVM의 안전을 훼손하는 것은 불가능해야 합니다.
* ***Control***: 클라이언트는 메모리 세그먼트를 할당 해제하는 방법에 대해 명시적으로(메소드 호출을 통해) 또는 암시적으로(세그먼트가 더 이상 사용되지 않을 때) 옵션이 있어야 합니다.
* ***Usability***: 외부 메모리에 액세스해야 하는 프로그램의 경우 API는 `sun.misc.Unsafe`와 같은 레거시 Java API에 대한 강력한 대안이어야 합니다.

#### Description

Foreign-Memory Access API는 동일한 이름의 패키지에 `jdk.incubator.foreign`이라는 인큐베이터 모듈로 제공됩니다. `MemorySegment`, `MemoryAddress` 및 `MemoryLayout`의 세 가지 주요 추상화를 소개합니다.

* `MemorySegment`는 주어진 공간적 및 시간적 경계를 가진 연속적인 메모리 영역을 모델링합니다.
* `MemoryAddress`는 온 또는 오프 힙에 상주할 수 있는 주소를 모델링하고,
* `MemoryLayout`은 메모리 세그먼트의 내용에 대한 프로그래밍 방식의 설명입니다.

메모리 세그먼트는 기본 메모리 버퍼, 메모리 매핑된 파일, Java 배열 및 바이트 버퍼(직접 또는 힙 기반)와 같은 다양한 소스에서 만들 수 있습니다. 예를 들어 기본 메모리 세그먼트는 다음과 같이 생성할 수 있습니다.

```java
try (MemorySegment segment = MemorySegment.allocateNative(100)) {
   ...
}
```

이렇게 하면 크기가 100바이트인 기본 메모리 버퍼와 연결된 메모리 세그먼트가 생성됩니다.

메모리 세그먼트는 공간적으로 경계가 지정되어 있으므로 하한과 상한이 있습니다. 세그먼트를 사용하여 이러한 경계 외부의 메모리에 액세스하려고 하면 예외가 발생합니다.

위의 try-with-resource 구성을 사용하여 증명된 것처럼 메모리 세그먼트도 시간적으로 제한되어 있습니다. 즉, 더 이상 사용하지 않을 때는 생성하고 사용한 다음 닫아야 합니다. 세그먼트를 닫으면 해당 세그먼트와 관련된 메모리 할당 해제와 같은 추가 부작용이 발생할 수 있습니다. 이미 닫힌 메모리 세그먼트에 액세스하려고 하면 예외가 발생합니다. 공간적 및 시간적 경계는 외부 메모리 액세스 API의 안전성을 보장하므로 이 API를 사용하면 JVM이 충돌할 수 없습니다.

##### Memory dereference

세그먼트와 관련된 메모리의 역참조는 Java 9에 도입된 데이터 액세스에 대한 추상화인 `var` 핸들을 얻어서 달성됩니다. 특히, 세그먼트는 메모리 액세스 `var` 핸들로 역참조됩니다. 이러한 종류의 `var` 핸들에는 한 쌍의 액세스 좌표가 있습니다.

* `MemorySegment` 유형의 좌표 — 메모리가 역참조되는 세그먼트
* `long` 유형의 좌표 — 역참조가 발생하는 세그먼트의 기본 주소로부터의 오프셋

메모리 액세스 `var` 핸들은 `MemoryHandles` 클래스의 팩토리 메서드를 사용하여 가져옵니다. 예를 들어, 기본 메모리 세그먼트의 요소를 설정하려면 다음과 같이 메모리 액세스 `var` 핸들을 사용할 수 있습니다.

```java
VarHandle intHandle = MemoryHandles.varHandle(int.class,
        ByteOrder.nativeOrder());

try (MemorySegment segment = MemorySegment.allocateNative(100)) {
    for (int i = 0; i < 25; i++) {
        intHandle.set(segment, i * 4, i);
    }
}
```

`MemoryHandles` 클래스에서 제공하는 하나 이상의 결합기 메서드를 사용하여 일반 메모리 액세스 `var` 핸들을 결합하여 고급 액세스 관용구를 표현할 수 있습니다. 이를 통해 클라이언트는 예를 들어 프로젝션/임베딩 메서드-핸들 쌍을 사용하여 메모리 액세스 `var` 핸들 유형을 매핑할 수 있습니다. 클라이언트는 또한 주어진 메모리 액세스 `var` 핸들의 좌표를 재정렬하고, 하나 이상의 좌표를 삭제하고, 새 좌표를 삽입할 수 있습니다.

API에 더 쉽게 액세스할 수 있도록 `MemoryAccess` 클래스는 메모리 액세스 `var` 핸들을 구성할 필요 없이 메모리 세그먼트를 역참조하는 데 사용할 수 있는 여러 정적 접근자를 제공합니다. 예를 들어 주어진 오프셋에서 세그먼트의 `int` 값을 설정하는 접근자가 있으므로 위의 예를 다음과 같이 단순화할 수 있습니다.

```java
try (MemorySegment segment = MemorySegment.allocateNative(100)) {
    for (int i = 0; i < 25; i++) {
        MemoryAccess.setIntAtOffset(segment, i * 4, i);
    }
}
```

##### Memory Layouts

API의 표현력을 향상시키고 위의 예와 같은 명시적 숫자 계산의 필요성을 줄이기 위해 `MemoryLayout`을 사용하여 `MemorySegment`의 내용을 프로그래밍 방식으로 설명할 수 있습니다. 예를 들어, 위의 예에서 사용된 기본 메모리 세그먼트의 레이아웃은 다음과 같이 설명할 수 있습니다.

```java
SequenceLayout intArrayLayout
    = MemoryLayout.ofSequence(25,
        MemoryLayout.ofValueBits(32,
            ByteOrder.nativeOrder()));
```

이것은 주어진 요소 레이아웃(32비트 값)이 25번 반복되는 시퀀스 메모리 레이아웃을 생성합니다. 메모리 레이아웃이 있으면 다음 예제와 같이 코드에서 모든 수동 숫자 계산을 제거하고 필요한 메모리 액세스 `var` 핸들 생성을 단순화할 수 있습니다.

```java
SequenceLayout intArrayLayout
    = MemoryLayout.ofSequence(25,
        MemoryLayout.ofValueBits(32,
            ByteOrder.nativeOrder()));

VarHandle indexedElementHandle
    = intArrayLayout.varHandle(int.class,
        PathElement.sequenceElement());

try (MemorySegment segment = MemorySegment.allocateNative(intArrayLayout)) {
    for (int i = 0; i < intArrayLayout.elementCount().getAsLong(); i++) {
        indexedElementHandle.set(segment, (long) i, i);
    }
}
```

이 예에서 레이아웃 객체는 복잡한 레이아웃 표현식에서 중첩 레이아웃을 선택하는 데 사용되는 레이아웃 경로 생성을 통해 메모리 액세스 `var` 핸들 생성을 유도합니다. 레이아웃 개체는 또한 레이아웃에서 파생된 크기 및 정렬 정보를 기반으로 하는 기본 메모리 세그먼트의 할당을 유도합니다. 이전 예제(25)의 루프 상수는 시퀀스 레이아웃의 요소 수로 대체되었습니다.

##### Unchecked segments

역참조 연산은 메모리 세그먼트에서만 가능합니다. 메모리 세그먼트에는 공간적 및 시간적 경계가 있으므로 런타임은 항상 주어진 세그먼트와 연결된 메모리가 안전하게 역참조되도록 할 수 있습니다. 그러나 클라이언트가 메모리 주소만 가질 수 있는 상황이 있습니다. 예를 들어 네이티브 코드와 상호 작용할 때 종종 발생합니다. 또한 메모리 주소는 긴 값으로 구성할 수 있습니다(`MemoryAddress::ofLong` 팩토리를 통해). 이러한 경우 런타임은 메모리 주소와 관련된 공간 및 시간 경계를 알 수 있는 방법이 없으므로 API에서 메모리 주소 역참조를 금지합니다.

메모리 주소를 역참조하기 위해 클라이언트에는 두 가지 옵션이 있습니다. 주소가 메모리 세그먼트 내에 있는 것으로 알려진 경우 클라이언트는 리베이스 작업(`MemoryAddress::segmentOffset`)을 수행할 수 있습니다. 리베이스 작업은 세그먼트의 기본 주소에 상대적인 주소 오프셋을 재해석하여 기존 세그먼트에 적용할 수 있는 새 오프셋을 생성합니다. 그러면 안전하게 역참조될 수 있습니다.

또는 그러한 세그먼트가 존재하지 않는 경우 클라이언트는 특별한 `MemoryAddress::asSegmentRestricted` 팩토리를 사용하여 안전하지 않게 세그먼트를 생성할 수 있습니다. 이 팩토리는 역참조 작업을 허용하기 위해 확인되지 않은 주소에 공간 및 시간 경계를 효과적으로 연결합니다. 이름에서 알 수 있듯이 이 작업은 본질적으로 안전하지 않으므로 주의해서 사용해야 합니다. 이러한 이유로 외부 메모리 액세스 API는 JDK 시스템 속성 `foreign.restricted`가 거부 이외의 값으로 설정된 경우에만 이 팩토리에 대한 호출을 허용합니다. 이 속성에 가능한 값은 다음과 같습니다.

* `deny` — 각 제한된 호출에 대해 런타임 예외를 발행합니다(기본값).
* `permit` — 제한된 호출을 허용합니다.
* `warn` — 허가와 비슷하지만 제한된 각 호출에 대해 한 줄 경고도 출력합니다. 그리고
* `debug` — 허가와 유사하지만 주어진 제한된 호출에 해당하는 스택도 덤프합니다.

앞으로 제한된 작업에 대한 액세스를 모듈 시스템과 통합할 계획입니다. 특정 모듈은 제한된 기본 액세스가 필요하다고 어떻게든 선언할 수 있습니다. 이러한 모듈에 의존하는 응용 프로그램이 실행될 때 사용자는 제한된 기본 작업을 수행하기 위해 해당 모듈에 권한을 제공해야 할 수 있습니다. 그렇지 않으면 런타임에서 응용 프로그램 실행을 거부합니다.

###### Confinement

공간 및 시간 경계 외에도 세그먼트에는 스레드 제한 기능도 있습니다. 즉, 세그먼트는 세그먼트를 만든 스레드가 소유하고 다른 스레드는 세그먼트의 내용에 액세스하거나 특정 작업(예: 닫기)을 수행할 수 없습니다. 스레드 제한은 제한적이지만 다중 스레드 환경에서도 최적의 메모리 액세스 성능을 보장하는 데 중요합니다.

외부 메모리 액세스 API는 스레드 제한 장벽을 완화하는 여러 방법을 제공합니다. 첫째, 스레드는 명시적 핸드오프 작업을 수행하여 협력적으로 세그먼트를 공유할 수 있습니다. 여기서 스레드는 주어진 세그먼트에 대한 소유권을 해제하고 이를 다른 스레드로 전송합니다. 다음 코드를 고려하십시오.

```java
MemorySegment segmentA = MemorySegment.allocateNative(10); // confined to thread A
...
var segmentB = segmentA.withOwnerThread(threadB); // now confined to thread B
```

이 액세스 패턴은 직렬 제한이라고도 하며 한 번에 하나의 스레드만 세그먼트에 액세스해야 하는 생산자/소비자 사용 사례에서 유용할 수 있습니다. 핸드오프 작업을 안전하게 만들기 위해 API는 원래 세그먼트를 종료하고(닫기가 호출되었지만 기본 메모리를 해제하지 않은 것처럼) 올바른 소유자가 있는 새 세그먼트를 반환합니다. 구현은 또한 두 번째 스레드가 세그먼트에 액세스할 때 첫 번째 스레드의 모든 쓰기가 메모리로 플러시되도록 합니다.

직렬 제한이 충분하지 않으면 클라이언트는 선택적으로 스레드 소유권을 제거할 수 있습니다. 즉, 제한된 세그먼트를 여러 스레드가 동시에 액세스하고 닫을 수 있는 공유 세그먼트로 전환할 수 있습니다. 이전과 마찬가지로 세그먼트를 공유하면 원래 세그먼트가 종료되고 소유자 스레드가 없는 새 세그먼트가 반환됩니다.

```java
MemorySegment segmentA = MemorySegment.allocateNative(10); // confined by thread A
...
var sharedSegment = segmentA.withOwnerThread(null); // now a shared segment
```

공유 세그먼트는 메모리 세그먼트에서 `Spliterator` 인스턴스를 얻을 수 있기 때문에 여러 스레드가 세그먼트의 내용에 대해 병렬로 작업해야 할 때(예: Fork/Join과 같은 프레임워크 사용) 특히 유용합니다. 예를 들어, 메모리 세그먼트의 모든 32비트 값을 병렬로 합산하려면 다음 코드를 사용할 수 있습니다.

```java
SequenceLayout seq = MemoryLayout.ofSequence(1_000_000, MemoryLayouts.JAVA_INT);
SequenceLayout seq_bulk = seq.reshape(-1, 100);
VarHandle intHandle = seq.varHandle(int.class, sequenceElement());    

int sum = StreamSupport.stream(MemorySegment.spliterator(segment.withOwnerThread(null),
                                                         seq_bulk),
                               true)
                .mapToInt(slice -> {
                    int res = 0;
                    for (int i = 0; i < 100 ; i++) {
                        res += MemoryAccess.getIntAtIndex(slice, i);
                    }
                    return res;
                }).sum();
```

`MemorySegment::spliterator` 메소드는 세그먼트와 시퀀스 레이아웃을 취하고 세그먼트를 제공된 시퀀스 레이아웃의 요소에 해당하는 청크로 분할하는 분할기 인스턴스를 반환합니다. 여기에서 백만 개의 요소를 포함하는 배열의 요소를 합산하려고 합니다. 각 계산이 정확히 하나의 요소를 처리하는 병렬 합계를 수행하는 것은 비효율적이므로 대신 레이아웃 API를 사용하여 대량 시퀀스 레이아웃을 파생합니다. 벌크 레이아웃은 원본 레이아웃과 크기가 같지만 요소가 100개 요소의 그룹으로 배열되는 시퀀스 레이아웃으로 병렬 처리에 더 적합합니다.

분할자가 있으면 이를 사용하여 병렬 스트림을 구성하고 세그먼트의 내용을 병렬로 합산할 수 있습니다. 분할자에 의해 운영되는 세그먼트는 공유되므로 여러 스레드에서 동시에 세그먼트에 액세스할 수 있습니다. 스플리터 API는 액세스가 규칙적인 방식으로 발생하도록 합니다. 원래 세그먼트에서 슬라이스를 만들고 각 슬라이스를 스레드에 제공하여 원하는 계산을 수행하므로 동일한 메모리 영역에서 두 스레드가 동시에 작동할 수 없도록 합니다.

공유 세그먼트는 세그먼트를 넘겨주는 스레드가 세그먼트에서 작업을 계속할 다른 스레드를 알지 못하는 경우에 직렬 제한을 수행하는 데에도 유용할 수 있습니다. 예를 들면 다음과 같습니다.

```java
// thread A
MemorySegment segment = MemorySegment.allocateNative(10); // confined by thread A
// do some work
segment = segment.withOwnerThread(null);

// thread B
segment.withOwnerThread(Thread.currentThread()); // now confined by thread B
// do some more work
```

여러 스레드가 주어진 공유 세그먼트를 획득하기 위해 경쟁할 수 있지만 API는 그 중 하나만 공유 세그먼트의 소유권 획득에 성공하도록 합니다.

##### Implcit Deallocation

메모리 세그먼트는 결정적 할당 해제 기능을 제공하지만 가비지 수집기가 세그먼트에 더 이상 연결할 수 없다고 결정할 때 세그먼트와 연결된 메모리 리소스가 해제되도록 `Cleaner`에 등록할 수도 있습니다.

```java
MemorySegment segment = MemorySegment.allocateNative(100);
Cleaner cleaner = Cleaner.create();
segment.registerCleaner(cleaner);
// do some work
segment = null; // Cleaner might reclaim the segment memory now
```

클리너를 사용하여 세그먼트를 등록해도 클라이언트가 `MemorySegment::close`를 명시적으로 호출하는 것을 방지할 수 없습니다. API는 세그먼트의 정리 작업이 명시적으로(클라이언트 코드에 의해) 또는 암시적으로(청소기에 의해) 최대 한 번만 호출되도록 보장합니다. 도달할 수 없는 세그먼트는 (정의상) 어떤 스레드에서도 액세스할 수 없기 때문에 클리너는 제한된 세그먼트인지 공유 세그먼트인지에 관계없이 도달할 수 없는 세그먼트와 관련된 모든 메모리 리소스를 항상 해제할 수 있습니다.

### JEP 394:	Pattern Matching for instanceof

`instanceof` 연산자에 대한 패턴 일치로 Java 프로그래밍 언어를 향상시키십시오. 패턴 일치를 사용하면 프로그램의 공통 논리, 즉 개체에서 구성 요소의 조건부 추출을 보다 간결하고 안전하게 표현할 수 있습니다.

#### History

`instanceof`에 대한 패턴 일치는 [JEP 305](https://openjdk.java.net/jeps/305)에서 제안되었으며 JDK 14에서 미리보기 기능으로 제공되었습니다. [JEP 375](https://openjdk.java.net/jeps/375)에서 다시 제안했으며 두 번째 미리 보기를 위해 JDK 15로 제공되었습니다.

이 JEP는 다음과 같은 개선을 통해 JDK 16의 기능을 완성할 것을 제안합니다.

패턴 변수가 암시적으로 최종적이라는 제한을 해제하여 로컬 변수와 패턴 변수 간의 비대칭을 줄입니다.

패턴 `instanceof` 표현식이 `S` 유형의 표현식을 `T` 유형의 패턴과 비교하는 것을 컴파일 타임 오류로 만듭니다. 여기서 S는 T의 하위 유형입니다. (이 `instanceof` 표현식은 항상 성공하고 무의미합니다. 반대의 경우, 패턴 일치가 항상 실패하는 곳은 이미 컴파일 타임 오류입니다.)

추가 피드백을 기반으로 다른 개선 사항이 포함될 수 있습니다.

#### Description

`pattern`은 (1) 대상에 적용할 수 있는 술어 또는 테스트와 (2) 술어가 성공적으로 적용된 경우에만 대상에서 추출되는 패턴 변수로 알려진 지역 변수 세트의 조합입니다.

유형 패턴은 단일 패턴 변수와 함께 유형을 지정하는 술어로 구성됩니다.

`instanceof` 연산자(JLS 15.20.2)는 유형 대신 유형 패턴을 사용하도록 확장되었습니다.

이를 통해 위의 지루한 코드를 다음과 같이 리팩토링할 수 있습니다.

```java
if (obj instanceof String s) {
    // Let pattern matching do the work!
    ...
}
```

(이 코드에서 `String s` 구문은 유형 패턴입니다.) 의미는 직관적입니다. `instanceof` 연산자는 대상 `obj`를 다음과 같이 유형 패턴과 일치시킵니다. `obj`가 `String`의 인스턴스이면 `String`으로 캐스트되고 값이 변수 s에 할당됩니다.

패턴 일치의 조건성(값이 패턴과 일치하지 않으면 패턴 변수에 값이 할당되지 않음)은 패턴 변수의 범위를 신중하게 고려해야 함을 의미합니다. 우리는 간단한 작업을 수행하고 패턴 변수의 범위가 포함하는 문과 둘러싸는 블록의 모든 후속 문이라고 말할 수 있습니다. 그러나 이것은 불행한 중독 결과를 가져옵니다. 예를 들면 다음과 같습니다.

```java
if (a instanceof Point p) {
   ...
}
if (b instanceof Point p) {         // ERROR - p is in scope
   ...
}
```

다시 말해서, 두 번째 명령문에 의해 패턴 변수 `p`는 중독된 상태에 있을 것입니다. 범위 안에 있지만 값이 할당되지 않을 수 있으므로 액세스할 수 없어야 합니다. 그러나 액세스해서는 안 되지만 범위 내에 있으므로 다시 선언할 수 없습니다. 이것은 패턴 변수가 선언된 후 중독될 수 있다는 것을 의미하므로 프로그래머는 패턴 변수에 대해 많은 고유한 이름을 생각해야 합니다.

패턴 변수의 범위에 대해 대략적인 근사값을 사용하는 대신 패턴 변수는 흐름 범위 개념을 대신 사용합니다. 패턴 변수는 컴파일러가 패턴이 확실히 일치하고 변수에 값이 할당될 것이라고 추론할 수 있는 범위에만 있습니다. 이 분석은 흐름에 민감하며 확정 할당과 같은 기존 흐름 분석과 유사한 방식으로 작동합니다. 우리의 예로 돌아가서:

```java
if (a instanceof Point p) {
    // p is in scope
    ...
}
// p not in scope here
if (b instanceof Point p) {     // Sure!
        ...
}
```

좌우명은 "패턴 변수는 확실히 일치하는 범위에 있습니다"입니다. 이를 통해 패턴 변수를 안전하게 재사용할 수 있으며 Java 개발자가 이미 민감한 분석을 진행하는 데 익숙하기 때문에 직관적이고 친숙합니다.

`if` 문의 조건식이 단일 `instanceof`보다 복잡해지면 그에 따라 패턴 변수의 범위도 커집니다. 예를 들어 이 코드에서:

```java
if (obj instanceof String s && s.length() > 5) {
    flag = s.contains("jdk");
}
```

패턴 변수 `s`는 `&&` 연산자의 오른쪽 범위와 실제 블록에 있습니다. (`&&` 연산자의 오른쪽은 패턴 일치가 성공하고 `s`에 값이 할당된 경우에만 평가됩니다.) 반면에 다음 코드는 컴파일되지 않습니다.

```java
if (obj instanceof String s || s.length() > 5) {    // Error!
    ...
}
```

`||`의 의미 때문에 연산자의 경우 패턴 변수 `s`가 할당되지 않았을 수 있으므로 흐름 분석에서는 변수 `s`가 `||` 운영자.

`instanceof`에서 패턴 일치를 사용하면 Java 프로그램에서 전체 명시적 캐스트 수를 크게 줄여야 합니다. 유형 테스트 패턴은 등식 메서드를 작성할 때 특히 유용합니다. Effective Java의 항목 10에서 가져온 다음 동등 방법을 고려한다.

```java
public boolean equals(Object o) {
    return (o instanceof CaseInsensitiveString) &&
        ((CaseInsensitiveString) o).s.equalsIgnoreCase(s);
}
Using a type pattern means it can be rewritten to the clearer:

public boolean equals(Object o) {
    return (o instanceof CaseInsensitiveString cis) &&
        cis.s.equalsIgnoreCase(s);
}
```

다른 `equals` 메소드는 훨씬 더 극적으로 개선되었습니다. 다음과 같이 `equals` 메소드를 작성할 수 있는 위에서 `Point` 클래스를 고려하십시오.

```java
public boolean equals(Object o) {
    if (!(o instanceof Point))
        return false;
    Point other = (Point) o;
    return x == other.x
        && y == other.y;
}
```

대신 패턴 일치를 사용하여 이러한 여러 명령문을 단일 표현식으로 결합하여 반복을 제거하고 제어 흐름을 단순화할 수 있습니다.

```java
public boolean equals(Object o) {
    return (o instanceof Point other)
        && x == other.x
        && y == other.y;
}
```

패턴 변수에 대한 흐름 범위 분석은 명령문이 정상적으로 완료될 수 있는지 여부에 대한 개념에 민감합니다. 예를 들어 다음 방법을 고려하십시오.

```java
public void onlyForStrings(Object o) throws MyException {
    if (!(o instanceof String s))
        throw new MyException();
    // s is in scope
    System.out.println(s);
    ...
}
```

이 메소드는 매개변수 `o`가 문자열인지 테스트하고 그렇지 않은 경우 예외를 던집니다. 조건문이 정상적으로 완료된 경우에만 `println` 문에 도달할 수 있습니다. 조건문의 포함된 명령문은 정상적으로 완료될 수 없기 때문에 이는 조건식이 `false` 값으로 평가된 경우에만 발생할 수 있으며, 이는 결과적으로 패턴 일치가 성공했음을 의미합니다. 따라서 패턴 변수 `s`의 범위는 메서드 블록에서 조건문 뒤에 오는 명령문을 안전하게 포함합니다.

패턴 변수는 지역 변수의 특별한 경우일 뿐이며 범위 정의를 제외하고 다른 모든 측면에서 패턴 변수는 지역 변수로 취급됩니다. 특히, 이것은 (1) 할당될 수 있고 (2) 필드 선언을 섀도잉할 수 있음을 의미합니다. 예를 들어:

```java
class Example1 {
    String s;

    void test1(Object o) {
        if (o instanceof String s) {
            System.out.println(s);      // Field s is shadowed
            s = s + "\n";               // Assignment to pattern variable
            ...
        }
        System.out.println(s);          // Refers to field s
        ...
    }
}
```

그러나 패턴 변수의 흐름 범위 지정 특성은 이름이 필드 선언을 섀도잉하는 패턴 변수 선언을 참조하는지 또는 필드 선언 자체를 참조하는지 여부를 결정하기 위해 약간의 주의를 기울여야 함을 의미합니다.

```java
class Example2 {
    Point p;

    void test2(Object o) {
        if (o instanceof Point p) {
            // p refers to the pattern variable
            ...
        } else {
            // p refers to the field
            ...
        }
    }
}
```

이에 따라 `instanceof` 문법이 확장됩니다.

```
RelationalExpression:
     ...
     RelationalExpression instanceof ReferenceType
     RelationalExpression instanceof Pattern

Pattern:
     ReferenceType Identifier
```

### JEP 395:	Records

변경할 수 없는 데이터의 투명한 전달자 역할을 하는 클래스인 레코드를 사용하여 Java 프로그래밍 언어를 향상시키십시오. 레코드는 명목 튜플로 생각할 수 있습니다.

#### History

레코드는 [JEP 359](https://openjdk.java.net/jeps/359)에서 제안되었으며 JDK 14에서 미리 보기 기능으로 제공되었습니다.

피드백에 대한 응답으로 [JEP 384](https://openjdk.java.net/jeps/359)에 의해 디자인이 개선되었고 JDK 15에서 두 번째로 미리보기 기능으로 제공되었습니다. 두 번째 미리 보기의 개선 사항은 다음과 같습니다.

* 첫 번째 미리 보기에서는 정식 생성자가 공개되어야 했습니다. 두 번째 미리 보기에서 표준 생성자가 암시적으로 선언된 경우 해당 액세스 한정자는 레코드 클래스와 동일합니다. 정식 생성자가 명시적으로 선언된 경우 액세스 수정자는 최소한 레코드 클래스만큼의 액세스를 제공해야 합니다.
* `@Override` 어노테이션의 의미는 어노테이션이 있는 메소드가 레코드 컴포넌트에 대해 명시적으로 선언된 접근자 메소드인 경우를 포함하도록 확장되었습니다.
* 압축 생성자의 의도된 사용을 강제하기 위해 생성자 본문의 인스턴스 필드에 할당하는 것은 컴파일 타임 오류가 되었습니다.
* 로컬 레코드 클래스, 로컬 열거형 클래스 및 로컬 인터페이스를 선언하는 기능이 도입되었습니다.

이 JEP는 다음과 같이 개선하여 JDK 16의 기능을 완성할 것을 제안합니다.

* 내부 클래스가 명시적 또는 암시적으로 정적 멤버를 선언할 수 없도록 하는 오랜 제한을 완화합니다. 이것은 합법화되고 특히 내부 클래스가 레코드 클래스인 멤버를 선언할 수 있게 합니다.

추가 피드백을 기반으로 추가 개선 사항이 포함될 수 있습니다.

#### Goals

* 값의 단순한 집계를 표현하는 객체 지향 구조를 고안하십시오.
* 개발자가 확장 가능한 동작보다 변경할 수 없는 데이터 모델링에 집중할 수 있도록 지원합니다.
* `equals` 및 `accessors`와 같은 데이터 기반 메서드를 자동으로 구현합니다.
* 명목 유형 및 마이그레이션 호환성과 같은 오랜 Java 원칙을 유지합니다.

#### Description

레코드 클래스는 Java 언어의 새로운 종류의 클래스입니다. 레코드 클래스는 일반 클래스보다 덜 의식적으로 일반 데이터 집계를 모델링하는 데 도움이 됩니다.

레코드 클래스의 선언은 주로 상태 선언으로 구성됩니다. 그런 다음 레코드 클래스는 해당 상태와 일치하는 API에 커밋합니다. 즉, 레코드 클래스는 클래스가 일반적으로 누리는 자유(클래스의 API를 내부 표현에서 분리하는 기능)를 포기하지만 그 대가로 레코드 클래스 선언이 훨씬 더 간결해집니다.

보다 정확하게는 레코드 클래스 선언은 이름, 선택적 유형 매개변수, 헤더 및 본문으로 구성됩니다. 헤더는 상태를 구성하는 변수인 레코드 클래스의 구성 요소를 나열합니다. (이 구성 요소 목록을 상태 설명이라고도 합니다.) 예를 들면 다음과 같습니다.

```java
record Point(int x, int y) { }
```

레코드 클래스는 데이터에 대한 투명한 캐리어라는 의미론적 주장을 하기 때문에 레코드 클래스는 많은 표준 멤버를 자동으로 획득합니다.

헤더의 각 구성 요소에 대해 두 개의 멤버: 구성 요소와 이름 및 반환 유형이 동일한 공개 접근자 메서드와 구성 요소와 유형이 동일한 비공개 최종 필드.

서명이 헤더와 동일하고 레코드를 인스턴스화하는 새 표현식의 해당 인수에 각 개인 필드를 할당하는 정식 생성자.

두 레코드 값이 동일한 유형이고 동일한 구성 요소 값을 포함하는 경우 동일한지 확인하는 `equals` 및 `hashCode` 메소드 그리고

이름과 함께 모든 레코드 구성 요소의 문자열 표현을 반환하는 `toString` 메서드입니다.

즉, 레코드 클래스의 헤더는 해당 상태, 즉 해당 구성 요소의 유형 및 이름을 설명하고 API는 해당 상태 설명에서 기계적으로 완전하게 파생됩니다. API에는 구성, 구성원 액세스, 동등성 및 표시를 위한 프로토콜이 포함됩니다. (향후 버전에서는 강력한 패턴 매칭이 가능하도록 해체 패턴을 지원할 예정입니다.)

##### Constructors for record classes

레코드 클래스의 생성자 규칙은 일반 클래스와 다릅니다. 생성자 선언이 없는 일반 클래스에는 자동으로 기본 생성자가 제공됩니다. 대조적으로, 생성자 선언이 없는 레코드 클래스에는 레코드를 인스턴스화한 새 표현식의 해당 인수에 모든 개인 필드를 할당하는 정식 생성자가 자동으로 제공됩니다. 예를 들어, 이전에 선언된 레코드인 `record Point(int x, int y) { }`는 다음과 같이 컴파일됩니다.

```java
record Point(int x, int y) {
    // Implicitly declared fields
    private final int x;
    private final int y;

    // Other implicit declarations elided ...

    // Implicitly declared canonical constructor
    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
```

표준 생성자는 위에 표시된 것처럼 레코드 헤더와 일치하는 형식 매개변수 목록을 사용하여 명시적으로 선언될 수 있습니다. 형식 매개변수 목록을 생략하여 보다 간결하게 선언할 수도 있습니다. 이러한 컴팩트 정규 생성자에서 매개변수는 묵시적으로 선언되며 레코드 구성요소에 해당하는 개인 필드는 본문에서 할당할 수 없지만 생성자의 끝에서 해당 형식 매개변수`(this.x = x;)`에 자동으로 할당됩니다. 간결한 형식은 개발자가 필드에 매개변수를 할당하는 지루한 작업 없이 매개변수의 유효성을 검사하고 정규화하는 데 집중할 수 있도록 도와줍니다.

예를 들어, 다음은 암시적 형식 매개변수의 유효성을 검사하는 컴팩트 표준 생성자입니다.

```java
record Range(int lo, int hi) {
    Range {
        if (lo > hi)  // referring here to the implicit constructor parameters
            throw new IllegalArgumentException(String.format("(%d,%d)", lo, hi));
    }
}
```

다음은 형식 매개변수를 정규화하는 컴팩트한 정식 생성자입니다.

```java
record Rational(int num, int denom) {
    Rational {
        int gcd = gcd(num, denom);
        num /= gcd;
        denom /= gcd;
    }
}
```

이 선언은 기존 생성자 형식과 동일합니다.

```java
record Rational(int num, int denom) {
    Rational(int num, int demon) {
        // Normalization
        int gcd = gcd(num, denom);
        num /= gcd;
        denom /= gcd;
        // Initialization
        this.num = num;
        this.denom = denom;
    }
}
```

암시적으로 선언된 생성자와 메서드가 있는 레코드 클래스는 중요하고 직관적인 의미론적 속성을 충족합니다. 예를 들어, 다음과 같이 선언된 레코드 클래스 `R`을 고려하십시오.

```java
record R(T1 c1, ..., Tn cn){ }
```
R의 인스턴스 r1이 다음과 같은 방식으로 복사되는 경우:

```java
R r2 = new R(r1.c1(), r1.c2(), ..., r1.cn());
```

그런 다음 `r1`이 널 참조가 아니라고 가정하면 항상 `r1.equals(r2)` 표현식이 `true`로 평가됩니다. 명시적으로 선언된 접근자와 `equals` 메서드는 이 불변성을 존중해야 합니다. 그러나 컴파일러가 명시적으로 선언된 메서드가 이 불변성을 존중하는지 확인하는 것은 일반적으로 불가능합니다.

예를 들어, 레코드 클래스의 다음 선언은 해당 접근자 메서드가 레코드 인스턴스의 상태를 "silently" 조정하고 위의 불변량이 충족되지 않기 때문에 잘못된 스타일로 간주되어야 합니다.

```java
record SmallPoint(int x, int y) {
  public int x() { return this.x < 100 ? this.x : 100; }
  public int y() { return this.y < 100 ? this.y : 100; }
}
```

또한 모든 레코드 클래스에 대해 암시적으로 선언된 `equals` 메서드가 구현되어 반사적이며 부동 소수점 구성 요소가 있는 레코드 클래스에 대해 `hashCode`와 일관되게 동작합니다. 다시 말하지만 명시적으로 선언된 `equals` 및 `hashCode` 메소드는 유사하게 작동해야 합니다.

##### Rules for record classes

일반 클래스와 비교하여 레코드 클래스의 선언에는 많은 제한 사항이 있습니다.

* 레코드 클래스 선언에는 extends 절이 없습니다. 레코드 클래스의 수퍼클래스는 항상 `java.lang.Record`이며, 열거형 클래스의 수퍼클래스가 항상 `java.lang.Enum`인 것과 유사합니다. 일반 클래스가 암시적 슈퍼클래스 Object를 명시적으로 확장할 수 있지만 레코드는 암시적 슈퍼클래스 `Record`를 포함하여 어떤 클래스도 명시적으로 확장할 수 없습니다.
* 레코드 클래스는 암시적으로 최종적이며 추상화될 수 없습니다. 이러한 제한 사항은 레코드 클래스의 API가 해당 상태 설명에 의해서만 정의되며 나중에 다른 클래스에 의해 향상될 수 없다는 점을 강조합니다.
* 레코드 구성 요소에서 파생된 필드는 최종적입니다. 이 제한은 데이터 캐리어 클래스에 널리 적용할 수 있는 기본적으로 변경할 수 없는 정책을 구현합니다.
* 레코드 클래스는 인스턴스 필드를 명시적으로 선언할 수 없으며 인스턴스 이니셜라이저를 포함할 수 없습니다. 이러한 제한은 레코드 헤더만 레코드 값의 상태를 정의하도록 합니다.
* 그렇지 않으면 자동으로 파생될 멤버의 명시적 선언은 명시적 선언의 주석을 무시하고 자동으로 파생된 멤버의 형식과 정확히 일치해야 합니다. 접근자 또는 `equals` 또는 `hashCode` 메서드의 명시적 구현은 레코드 클래스의 의미론적 불변성을 유지하도록 주의해야 합니다.
* 코드 클래스는 네이티브 메서드를 선언할 수 없습니다. 레코드 클래스가 기본 메서드를 선언할 수 있는 경우 레코드 클래스의 동작은 정의에 따라 레코드 클래스의 명시적 상태가 아닌 외부 상태에 따라 달라집니다. 네이티브 메서드가 있는 클래스는 레코드로 마이그레이션하기에 적합하지 않습니다.

위의 제한 사항을 넘어서서 레코드 클래스는 일반 클래스처럼 작동합니다.

* 레코드 클래스의 인스턴스는 새 표현식을 사용하여 생성됩니다.
* 레코드 클래스는 최상위 레벨 또는 중첩으로 선언될 수 있으며 제네릭일 수 있습니다.
* 레코드 클래스는 정적 메서드, 필드 및 이니셜라이저를 선언할 수 있습니다.
* 레코드 클래스는 인스턴스 메서드를 선언할 수 있습니다.
* 레코드 클래스는 인터페이스를 구현할 수 있습니다. 레코드 클래스는 헤더에 설명된 상태를 넘어 상속된 상태를 의미하기 때문에 수퍼클래스를 지정할 수 없습니다. 그러나 레코드 클래스는 수퍼인터페이스를 자유롭게 지정하고 이를 구현하기 위한 인스턴스 메소드를 선언할 수 있습니다. 클래스와 마찬가지로 인터페이스는 많은 레코드의 동작을 유용하게 특성화할 수 있습니다. 동작은 도메인 독립적(예: 비교 가능)이거나 도메인 특정일 수 있으며, 이 경우 레코드는 도메인을 캡처하는 봉인된 계층의 일부일 수 있습니다(아래 참조).
* 레코드 클래스는 중첩 레코드 클래스를 포함하여 중첩 유형을 선언할 수 있습니다. 레코드 클래스 자체가 중첩된 경우 암시적으로 정적입니다. 이렇게 하면 레코드 클래스에 상태를 자동으로 추가하는 인스턴스를 즉시 둘러싸는 것을 방지할 수 있습니다.
* 레코드 클래스와 헤더의 구성 요소는 주석으로 장식될 수 있습니다. 레코드 구성 요소의 모든 주석은 주석에 적용 가능한 대상 집합에 따라 자동으로 파생된 필드, 메서드 및 생성자 매개변수로 전파됩니다. 레코드 구성 요소의 유형에 대한 유형 주석은 자동으로 파생된 멤버의 해당 유형 사용에도 전파됩니다.
* 레코드 클래스의 인스턴스는 직렬화 및 역직렬화될 수 있습니다. 그러나 `writeObject`, `readObject`, `readObjectNoData`, `writeExternal` 또는 `readExternal` 메서드를 제공하여 프로세스를 사용자 지정할 수 없습니다. 레코드 클래스의 구성 요소는 직렬화를 제어하는 ​​반면 레코드 클래스의 정식 생성자는 역직렬화를 제어합니다.

##### Local record classes

레코드 클래스의 인스턴스를 생성하고 소비하는 프로그램은 그 자체가 단순한 변수 그룹인 많은 중간 값을 처리할 가능성이 높습니다. 이러한 중간 값을 모델링하기 위해 레코드 클래스를 선언하는 것이 편리한 경우가 많습니다. 한 가지 옵션은 오늘날 많은 프로그램이 도우미 클래스를 선언하는 것처럼 정적 및 중첩된 "도우미" 레코드 클래스를 선언하는 것입니다. 더 편리한 옵션은 변수를 조작하는 코드에 가까운 메소드 내부에 레코드를 선언하는 것입니다. 따라서 우리는 로컬 클래스의 기존 구성과 유사한 로컬 레코드 클래스를 정의합니다.

다음 예에서 판매자 및 월별 판매 수치의 집계는 로컬 레코드 클래스인 `MerchantSales`로 모델링됩니다. 이 레코드 클래스를 사용하면 다음과 같은 스트림 작업의 가독성이 향상됩니다.

```java
List<Merchant> findTopMerchants(List<Merchant> merchants, int month) {
    // Local record
    record MerchantSales(Merchant merchant, double sales) {}

    return merchants.stream()
        .map(merchant -> new MerchantSales(merchant, computeSales(merchant, month)))
        .sorted((m1, m2) -> Double.compare(m2.sales(), m1.sales()))
        .map(MerchantSales::merchant)
        .collect(toList());
}
```

로컬 레코드 클래스는 중첩 레코드 클래스의 특별한 경우입니다. 중첩 레코드 클래스와 마찬가지로 로컬 레코드 클래스는 암시적으로 정적입니다. 이것은 자신의 메서드가 바깥쪽 메서드의 변수에 액세스할 수 없음을 의미합니다. 차례로 이것은 레코드 클래스에 상태를 자동으로 추가하는 즉시 둘러싸는 인스턴스를 캡처하는 것을 방지합니다. 로컬 레코드 클래스가 암시적으로 정적이라는 사실은 암시적으로 정적이 아닌 로컬 클래스와 대조됩니다. 사실, 지역 클래스는 암시적이든 명시적이든 정적이 아니며 항상 둘러싸는 메서드의 변수에 액세스할 수 있습니다.

##### Local enum classes and local interfaces

로컬 레코드 클래스를 추가하면 다른 종류의 암시적 정적 로컬 선언을 추가할 수 있습니다.

중첩된 열거형 클래스와 중첩된 인터페이스는 이미 암시적으로 정적이므로 일관성을 위해 암시적으로 정적인 로컬 열거형 클래스와 로컬 인터페이스를 정의합니다.

##### Static members of inner classes

멤버가 상수 변수가 아닌 한 내부 클래스가 명시적으로 또는 암시적으로 정적 멤버를 선언하면 현재 컴파일 타임 오류로 지정됩니다. 이것은 예를 들어 내부 클래스가 레코드 클래스 멤버를 선언할 수 없음을 의미합니다. 중첩된 레코드 클래스는 암시적으로 정적이기 때문입니다.

내부 클래스가 명시적으로 또는 암시적으로 정적 멤버를 선언할 수 있도록 이 제한을 완화합니다. 특히 이를 통해 내부 클래스가 레코드 클래스인 정적 멤버를 선언할 수 있습니다.

##### Annotations on record components

레코드 구성 요소에는 레코드 선언에서 여러 역할이 있습니다. 레코드 구성 요소는 일급 개념이지만 각 구성 요소는 동일한 이름 및 유형의 필드, 동일한 이름 및 반환 유형의 접근자 메서드, 동일한 이름 및 유형의 정식 생성자의 형식 매개변수에도 해당합니다. .

이것은 다음과 같은 질문을 제기합니다. 구성 요소에 주석을 달 때 실제로 주석이 달린 것은 무엇입니까? 대답은 "이 특정 주석을 적용할 수 있는 모든 요소"입니다. 이를 통해 필드, 생성자 매개변수 또는 접근자 메서드에 주석을 사용하는 클래스를 이러한 멤버를 중복 선언하지 않고도 레코드로 마이그레이션할 수 있습니다. 예를 들어 다음과 같은 클래스

```java
public final class Card {
    private final @MyAnno Rank rank;
    private final @MyAnno Suit suit;
    @MyAnno Rank rank() { return this.rank; }
    @MyAnno Suit suit() { return this.suit; }
    ...
}
```

동등하고 훨씬 더 읽기 쉬운 레코드 선언으로 마이그레이션할 수 있습니다.

```java
public record Card(@MyAnno Rank rank, @MyAnno Suit suit) { ... }
```

주석의 적용 가능성은 `@Target` 메타 주석을 사용하여 선언됩니다. 다음을 고려하세요:

```java
@Target(ElementType.FIELD)
    public @interface I1 {...}
```

이것은 필드 선언에 적용할 수 있는 주석 `@I1`을 선언합니다. 주석이 둘 이상의 선언에 적용 가능하다고 선언할 수 있습니다. 예를 들어:

```java
@Target({ElementType.FIELD, ElementType.METHOD})
    public @interface I2 {...}
```

이것은 필드 선언과 메소드 선언 모두에 적용할 수 있는 주석 `@I2`를 선언합니다.

레코드 구성 요소의 주석으로 돌아가면 이러한 주석이 해당하는 프로그램 지점에 표시됩니다. 즉, @Target 메타 주석을 사용하여 전파가 개발자의 제어 하에 있습니다. 전파 규칙은 체계적이고 직관적이며 다음과 같이 적용됩니다.

* 레코드 구성 요소의 주석이 필드 선언에 적용 가능한 경우 주석은 해당 개인 필드에 나타납니다.
* 레코드 구성 요소의 주석이 메서드 선언에 적용 가능한 경우 주석은 해당 접근자 메서드에 나타납니다.
* 레코드 구성 요소의 주석이 형식 매개 변수에 적용 가능한 경우 명시적으로 선언되지 않은 경우 표준 생성자의 해당 형식 매개 변수에 주석이 표시되고 명시적으로 선언된 경우 압축 생성자의 해당 형식 매개 변수에 주석이 나타납니다. 
* 레코드 구성 요소의 주석이 유형에 적용 가능한 경우 주석은 다음 모두에 전파됩니다.
  * 해당 필드의 유형
  * 해당 접근자 메서드의 반환 유형
  * 정규 생성자의 해당 형식 매개변수 유형
  * 레코드 구성 요소의 유형(리플렉션을 통해 런타임에 액세스할 수 있음)

공개 접근자 메서드 또는 (non-compact) 정식 생성자가 명시적으로 선언된 경우 직접 표시되는 주석만 있습니다. 해당 레코드 구성 요소에서 이러한 구성원으로 전파되는 것은 없습니다.

레코드 구성 요소의 선언 주석은 주석이 `@Target(RECORD_COMPONENT)`으로 메타 주석 처리되지 않는 한 리플렉션 API를 통해 런타임에 레코드 구성 요소와 연결된 주석에 포함되지 않습니다.

##### Compatibility and migration

추상 클래스 `java.lang.Record`는 모든 레코드 클래스의 공통 수퍼 클래스입니다. 모든 Java 소스 파일은 미리 보기 기능을 활성화하거나 비활성화하는지 여부에 관계없이 `java.lang.Record` 클래스와 `java.lang` 패키지의 다른 모든 유형을 암시적으로 가져옵니다. 그러나 응용 프로그램이 다른 패키지에서 `Record`라는 다른 클래스를 가져오는 경우 컴파일러 오류가 발생할 수 있습니다.

`com.myapp.Record`의 다음 클래스 선언을 고려하십시오.

```java
package com.myapp;

public class Record {
    public String greeting;
    public Record(String greeting) {
        this.greeting = greeting;
    }
}
```

다음 예인 `org.example.MyappPackageExample`은 와일드카드를 사용하여 `com.myapp.Record`를 가져오지만 컴파일하지 않습니다.

```java
package org.example;
import com.myapp.*;

public class MyappPackageExample {
    public static void main(String[] args) {
       Record r = new Record("Hello world!");
    }
}
```

컴파일러는 다음과 유사한 오류 메시지를 생성합니다.

```java
./org/example/MyappPackageExample.java:6: error: reference to Record is ambiguous
       Record r = new Record("Hello world!");
       ^
  both class com.myapp.Record in com.myapp and class java.lang.Record in java.lang match

./org/example/MyappPackageExample.java:6: error: reference to Record is ambiguous
       Record r = new Record("Hello world!");
                      ^
  both class com.myapp.Record in com.myapp and class java.lang.Record in java.lang match
```

`com.myapp` 패키지의 `Record`와 `java.lang` 패키지의 `Record` 모두 와일드카드를 사용하여 가져옵니다. 결과적으로 어떤 클래스도 우선하지 않으며 컴파일러는 단순 이름 `Record`를 사용하는 경우 오류 메시지를 생성합니다.

이 예제를 컴파일하려면 `import` 문을 변경하여 `Record`의 정규화된 이름을 가져오도록 할 수 있습니다.

```java
import com.myapp.Record;
```

`java.lang` 패키지에 클래스를 도입하는 것은 드물지만 때로는 필요합니다. 이전 예제는 Java 5의 `Enum`, Java 9의 `Module` 및 Java 14의 `Record`입니다.

##### Java grammar

```java
RecordDeclaration:
  {ClassModifier} `record` TypeIdentifier [TypeParameters]
    RecordHeader [SuperInterfaces] RecordBody

RecordHeader:
 `(` [RecordComponentList] `)`

RecordComponentList:
 RecordComponent { `,` RecordComponent}

RecordComponent:
 {Annotation} UnannType Identifier
 VariableArityRecordComponent

VariableArityRecordComponent:
 {Annotation} UnannType {Annotation} `...` Identifier

RecordBody:
  `{` {RecordBodyDeclaration} `}`

RecordBodyDeclaration:
  ClassBodyDeclaration
  CompactConstructorDeclaration

CompactConstructorDeclaration:
  {ConstructorModifier} SimpleTypeName ConstructorBody
```

##### Class-file representation

레코드의 클래스 파일은 레코드 속성을 사용하여 레코드의 구성 요소에 대한 정보를 저장합니다.

```java
Record_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 components_count;
    record_component_info components[components_count];
}

record_component_info {
    u2 name_index;
    u2 descriptor_index;
    u2 attributes_count;
    attribute_info attributes[attributes_count];
}
```

레코드 구성 요소에 삭제된 설명자와 다른 일반 서명이 있는 경우 `record_component_info` 구조에 서명 속성이 있어야 합니다.

##### Reflection API

`java.lang.Class`에 두 개의 공개 메소드를 추가합니다.

`RecordComponent[] getRecordComponents()` — `java.lang.reflect.RecordComponent` 객체의 배열을 반환합니다. 이 배열의 요소는 레코드 선언에 나타나는 것과 동일한 순서로 레코드의 구성 요소에 해당합니다. 이름, 주석 및 접근자 메서드를 포함하여 배열의 각 요소에서 추가 정보를 추출할 수 있습니다.

`boolean isRecord()` — 주어진 클래스가 레코드로 선언된 경우 `true`를 반환합니다. (`isEnum`과 비교)

### JEP 396:	Strongly Encapsulate JDK Internals by Default

`sun.misc.Unsafe`와 같은 중요한 내부 API를 제외하고 기본적으로 JDK의 모든 내부 요소를 강력하게 캡슐화합니다. 최종 사용자가 JDK 9 이후 기본값인 완화된 강력한 캡슐화를 선택할 수 있도록 합니다.

#### Goals

* Project Jigsaw의 주요 목표 중 하나인 JDK의 보안 및 유지 관리성을 지속적으로 개선합니다.
* 개발자가 내부 요소를 사용하는 것에서 표준 API를 사용하는 것으로 마이그레이션하도록 장려하여 개발자와 해당 사용자 모두 향후 Java 릴리스로 번거롭지 않게 업그레이드할 수 있습니다.

#### Description

완화된 강력한 캡슐화는 실행기 옵션 `--illegal-access`에 의해 제어됩니다. [JEP 261](https://openjdk.java.net/jeps/261)에 의해 도입된 이 옵션은 사용을 방지하기 위해 도발적으로 명명되었습니다. 현재 다음과 같이 작동합니다.

* `--illegal-access=permit`은 JDK 8에 있던 모든 패키지가 이름 없는 모듈의 코드에 열려 있도록 정렬합니다. 따라서 클래스 경로의 코드는 JDK 8에 있던 패키지에 대해 `java.*` 패키지의 비공개 요소, `sun.*` 및 기타 내부 패키지의 모든 요소에 액세스하기 위해 계속 리플렉션을 사용할 수 있습니다. 첫 번째 반사 액세스 작업 그러한 요소에 대해 경고가 발행되지만 그 시점 이후에는 경고가 발행되지 않습니다.

이 모드는 JDK 9부터 기본값이었습니다.

* `--illegal-access=warn`은 모든 불법 반사 액세스 작업에 대해 경고 메시지가 발행된다는 점을 제외하고는 허용과 동일합니다.
* `--illegal-access=debug`는 모든 불법 반사 액세스 작업에 대해 경고 메시지와 스택 추적이 모두 발행된다는 점을 제외하고는 `warn`과 동일합니다.
* `--illegal-access=deny`는 다른 명령줄 옵션(예: `--add-opens`)으로 활성화된 작업을 제외한 모든 불법 액세스 작업을 비활성화합니다.

JDK의 모든 내부 요소를 강력하게 캡슐화하는 다음 단계로 `--illegal-access` 옵션의 기본 모드를 허용에서 거부로 변경할 것을 제안합니다. 이 변경으로 JDK 8에 존재하고 중요한 내부 API를 포함하지 않는 패키지는 더 이상 기본적으로 열리지 않습니다. 전체 목록은 여기에서 볼 수 있습니다. `sun.misc` 패키지는 여전히 `jdk.unsupported` 모듈에 의해 내보내지며 리플렉션을 통해 계속 액세스할 수 있습니다.

또한 Java 플랫폼 사양의 관련 텍스트를 수정하여 포함하는 모듈의 선언에서 해당 패키지가 열려 있는 것으로 명시적으로 선언되지 않는 한 모든 Java 플랫폼 구현에서 기본적으로 패키지를 열 수 없도록 합니다.

`--illegal-access` 옵션의 허용, 경고 및 디버그 모드는 계속 작동합니다. 이러한 모드를 통해 최종 사용자는 원하는 경우 완화된 강력한 캡슐화를 선택할 수 있습니다.

### JEP 397:	Sealed Classes (Second Preview)

봉인된 클래스와 인터페이스로 Java 프로그래밍 언어를 향상시키십시오. 봉인된 클래스 및 인터페이스는 다른 클래스 또는 인터페이스가 확장하거나 구현할 수 있는 것을 제한합니다.

#### History

봉인된 클래스는 [JEP 360](https://openjdk.java.net/jeps/360)에서 제안되었으며 JDK 15에서 미리 보기 기능으로 제공되었습니다.

이 JEP는 다음과 같이 개선된 JDK 16의 기능을 다시 검토할 것을 제안합니다.

* JLS의 제한된 식별자 및 제한된 키워드의 이전 개념을 대체하여 컨텍스트 키워드의 개념을 지정하십시오. 봉인, 봉인되지 않은 문자 시퀀스, 문맥 키워드로 허가를 소개합니다.
* 익명 클래스 및 람다 식과 마찬가지로 로컬 클래스는 봉인된 클래스 또는 봉인된 인터페이스의 암시적으로 선언된 허용된 하위 클래스를 결정할 때 봉인된 클래스의 하위 클래스가 아닐 수 있습니다.
* 봉인된 유형 계층과 관련하여 캐스트 변환을 보다 엄격하게 검사하기 위해 참조 변환을 좁히십시오.

#### Goals

* 클래스 또는 인터페이스 작성자가 구현을 담당하는 코드를 제어할 수 있도록 합니다.
* 수퍼클래스의 사용을 제한하기 위해 액세스 수정자보다 더 선언적인 방법을 제공합니다.
* 패턴의 철저한 분석을 위한 기반을 제공하여 패턴 매칭의 미래 방향을 지원합니다.

#### Description

`sealed class` 또는 인터페이스는 허용된 클래스 및 인터페이스에 의해서만 확장되거나 구현될 수 있습니다.

클래스는 선언에 봉인된 수정자를 적용하여 봉인됩니다. 그런 다음, `extends` 및 `Implements` 절 뒤에, `permits` 절은 봉인된 클래스를 확장할 수 있는 클래스를 지정합니다. 예를 들어 다음 `Shape` 선언은 세 개의 허용되는 하위 클래스를 지정합니다.

```java
package com.example.geometry;

public abstract sealed class Shape
    permits Circle, Rectangle, Square { ... }
```

`Permits`에 의해 지정된 클래스는 동일한 모듈(수퍼클래스가 명명된 모듈에 있는 경우) 또는 동일한 패키지(수퍼클래스가 명명되지 않은 모듈에 있는 경우)와 같이 슈퍼클래스 근처에 있어야 합니다. 예를 들어 다음 `Shape` 선언에서 허용되는 하위 클래스는 모두 동일한 이름의 모듈의 서로 다른 패키지에 있습니다.

```java
package com.example.geometry;

public abstract sealed class Shape 
    permits com.example.polar.Circle,
            com.example.quad.Rectangle,
            com.example.quad.simple.Square { ... }
```

허용된 하위 클래스의 크기와 수가 작은 경우 봉인된 클래스와 동일한 소스 파일에서 선언하는 것이 편리할 수 있습니다. 이러한 방식으로 선언되면 봉인된 클래스는 `permits` 절을 생략할 수 있으며 Java 컴파일러는 소스 파일의 선언에서 허용된 하위 클래스를 유추합니다. (하위 클래스는 보조 또는 중첩 클래스일 수 있습니다.) 예를 들어 다음 코드가 `Shape.java`에서 발견되면 봉인된 클래스 `Shape`에는 세 개의 허용되는 하위 클래스가 있는 것으로 유추됩니다.

```java
package com.example.geometry;

abstract sealed class Shape { ... }
... class Circle    extends Shape { ... }
... class Rectangle extends Shape { ... }
... class Square    extends Shape { ... }
```

클래스를 봉인하면 하위 클래스가 제한됩니다. 사용자 코드는 `instanceof` 테스트의 `if-else` 체인을 사용하여 봉인된 클래스의 인스턴스를 검사할 수 있습니다(서브클래스당 하나의 테스트). 다른 모든 것을 포괄하는 절은 필요하지 않습니다. 예를 들어 다음 코드는 `Shape`의 허용되는 세 가지 하위 클래스를 찾습니다.

```java
Shape rotate(Shape shape, double angle) {
    if (shape instanceof Circle) return shape;
    else if (shape instanceof Rectangle) return shape.rotate(angle);
    else if (shape instanceof Square) return shape.rotate(angle);
    // no else needed!
}
```

봉인된 클래스는 허용되는 하위 클래스에 세 가지 제약 조건을 부과합니다.

1. 봉인된 클래스와 허용된 하위 클래스는 동일한 모듈에 속해야 하며, 이름이 없는 모듈에서 선언된 경우 동일한 패키지에 속해야 합니다.
2. 모든 허용된 하위 클래스는 봉인된 클래스를 직접 확장해야 합니다.
3. 모든 허용된 하위 클래스는 수정자를 사용하여 상위 클래스에 의해 시작된 봉인을 전파하는 방법을 설명해야 합니다.
   * 허용된 하위 클래스는 클래스 계층 구조의 해당 부분이 더 확장되는 것을 방지하기 위해 `final`로 선언될 수 있습니다. (레코드 클래스([JEP 395](https://openjdk.java.net/jeps/395))는 암시적으로 `final`로 선언됩니다.)
   * 허용된 하위 클래스는 해당 계층의 일부가 봉인된 슈퍼클래스에서 예상한 것보다 더 확장될 수 있도록 봉인된 것으로 선언될 수 있지만 제한된 방식으로만 가능합니다.
   * 허용된 하위 클래스는 봉인되지 않은 것으로 선언되어 계층의 해당 부분이 알려지지 않은 하위 클래스에 의해 확장을 위해 열린 상태로 되돌아갑니다. (봉인된 클래스는 허용된 하위 클래스가 이 작업을 수행하는 것을 방지할 수 없습니다.)

세 번째 제약 조건의 예로서 `Circle`은 최종일 수 있지만 `Rectangle`은 봉인되고 `Square`는 봉인되지 않습니다.

```java
package com.example.geometry;

public abstract sealed class Shape
    permits Circle, Rectangle, Square { ... }

public final class Circle extends Shape { ... }

public sealed class Rectangle extends Shape 
    permits TransparentRectangle, FilledRectangle { ... }
public final class TransparentRectangle extends Rectangle { ... }
public final class FilledRectangle extends Rectangle { ... }

public non-sealed class Square extends Shape { ... }
```

`final`, `sealing` 및 `non-sealed` 수정자 중 정확히 하나는 허용된 각 하위 클래스에서 사용해야 합니다. 클래스가 `sealed`(서브클래스를 암시)과 `final`(서브클래스가 없음을 암시), 또는 `non-sealed`(서브클래스를 암시)와 `final`(서브클래스가 없음을 암시), 또는 `sealed`(제한된 서브클래스를 암시)과 `non-sealed` 둘 다일 수는 없습니다. `-sealed`(무제한 하위 클래스를 의미).

(최종 수식어는 확장/구현이 완전히 금지된 강력한 형태의 밀봉으로 간주될 수 있습니다. 즉, `final`은 개념적으로 `sealing` + 아무것도 지정하지 않는 `permit` 절과 동일하지만 그러한 허가 조항을 작성할 수는 없습니다.)

`sealed`되거나 `non-sealed` 클래스는 `abstract`일 수 있으며 `abstract` 멤버를 가질 수 있습니다. `sealed`된 클래스는 `abstract` 하위 클래스를 허용할 수 있습니다. 단, `final`이 아니라 `sealed`되거나 `non-sealed` 경우입니다.

##### Class accessibility

확장 및 허용 절은 클래스 이름을 사용하기 때문에 `permits` 하위 클래스와 봉인된 상위 클래스는 서로 액세스할 수 있어야 합니다. 그러나 허용된 하위 클래스는 서로 또는 봉인된 클래스와 동일한 액세스 가능성을 가질 필요가 없습니다. 특히, 하위 클래스는 봉인된 클래스보다 액세스 가능성이 낮을 수 있습니다. 이는 패턴 일치가 `switch`에서 지원되는 향후 릴리스에서 기본 절(또는 기타 전체 패턴)이 사용되지 않는 한 일부 코드는 하위 클래스를 완전히 전환할 수 없음을 의미합니다. Java 컴파일러는 `switch`가 원래 작성자가 상상한 것만큼 완전하지 않을 때 감지하고 `default` 절을 권장하도록 오류 메시지를 사용자 정의하도록 권장됩니다.

##### Sealed interfaces

클래스의 경우 인터페이스에 sealing 수식어를 적용하여 인터페이스를 봉인할 수 있습니다. 슈퍼인터페이스를 지정하기 위한 `extends` 절 뒤에는 구현 클래스와 서브인터페이스가 허가 절로 지정됩니다. 예를 들어, 서론의 행성 예는 다음과 같이 다시 작성할 수 있습니다.

```java
sealed interface Celestial 
    permits Planet, Star, Comet { ... }

final class Planet implements Celestial { ... }
final class Star   implements Celestial { ... }
final class Comet  implements Celestial { ... }
```

다음은 알려진 하위 클래스 집합이 있는 클래스 계층 구조의 또 다른 고전적인 예입니다. 모델링 수학적 표현입니다.

```java
package com.example.expression;

public sealed interface Expr
    permits ConstantExpr, PlusExpr, TimesExpr, NegExpr { ... }

public final class ConstantExpr implements Expr { ... }
public final class PlusExpr     implements Expr { ... }
public final class TimesExpr    implements Expr { ... }
public final class NegExpr      implements Expr { ... }
```

##### Sealing and record classes

봉인된 클래스는 레코드 클래스와 잘 작동합니다([JEP 395](https://openjdk.java.net/jeps/395)). 레코드 클래스는 암시적으로 최종이므로 레코드 클래스의 봉인된 계층 구조는 위의 예보다 약간 더 간결합니다.

```java
package com.example.expression;

public sealed interface Expr
    permits ConstantExpr, PlusExpr, TimesExpr, NegExpr { ... }

public record ConstantExpr(int i)       implements Expr { ... }
public record PlusExpr(Expr a, Expr b)  implements Expr { ... }
public record TimesExpr(Expr a, Expr b) implements Expr { ... }
public record NegExpr(Expr e)           implements Expr { ... }
```

봉인된 클래스와 레코드 클래스의 조합을 대수 데이터 형식이라고도 합니다. 레코드 클래스를 사용하면 제품 형식을 표현할 수 있고 봉인된 클래스를 사용하여 합계 형식을 표현할 수 있습니다.

##### Sealed classes and conversions

캐스트 표현식은 값을 유형으로 변환합니다. 유형 `instanceof` 표현식은 유형에 대해 값을 테스트합니다. Java는 이러한 종류의 표현식에 허용되는 유형에 대해 매우 관대합니다. 예를 들어:

```java
interface I {}
   class C {} // does not implement I

   void test (C c) {
       if (c instanceof I) 
           System.out.println("It's an I");
   }
```

이 프로그램은 현재 `C` 개체가 인터페이스 `I`을 구현하는 것이 불가능하더라도 합법적입니다. 물론 프로그램이 발전함에 따라 다음과 같이 될 수 있습니다.

```java
...
   class B extends C implements I {}

   test(new B()); 
   // Prints "It's an I"
```

유형 변환 규칙은 개방형 확장성의 개념을 포착합니다. Java 유형 시스템은 닫힌 세계를 가정하지 않습니다. 클래스와 인터페이스는 미래에 확장될 수 있으며 변환 변환은 런타임 테스트로 컴파일되므로 안전하게 유연하게 사용할 수 있습니다.

그러나 스펙트럼의 다른 쪽 끝에서 변환 규칙은 클래스가 확실히 확장될 수 없는 경우, 즉 최종 클래스인 경우를 다룹니다.

```java
interface I {}
   final class C {}

   void test (C c) {
       if (c instanceof I) 
           System.out.println("It's an I");
   }
```

컴파일러가 `C`의 하위 클래스가 있을 수 없다는 것을 알고 있기 때문에 메서드 테스트는 컴파일에 실패합니다. 따라서 `C`는 `I`를 구현하지 않으므로 `C` 값이 `I`를 구현하는 것은 절대 불가능합니다. 이것은 컴파일 타임 오류입니다.

`C`가 최종적이지 않고 봉인된 경우 어떻게 됩니까? 그것의 직접적인 서브클래스는 명시적으로 열거되고 - 봉인의 정의에 의해 - 동일한 모듈에 있으므로 컴파일러가 유사한 컴파일 시간 오류를 발견할 수 있는지 확인하기를 기대합니다. 다음 코드를 고려하십시오.

```java
interface I {}
   sealed class C permits D {}
   final class D extends C {}
   
   void test (C c) {
       if (c instanceof I) 
           System.out.println("It's an I");
   }
```

클래스 `C`는 `I`을 구현하지 않으며 최종적이지 않으므로 기존 규칙에 따라 변환이 가능하다고 결론을 내릴 수 있습니다. 그러나 `C`는 봉인되어 있으며 `C`의 허용된 직접 하위 클래스, 즉 `D`가 있습니다. 봉인 유형의 정의에 따르면 `D`는 최종, 봉인 또는 봉인되지 않아야 합니다. 이 예에서 `C`의 모든 직접 하위 클래스는 최종적이며 `I`를 구현하지 않습니다. 따라서 이 프로그램은 `I`를 구현하는 `C`의 하위 유형이 있을 수 없으므로 거부되어야 합니다.

대조적으로, 봉인된 클래스의 직접 하위 클래스 중 하나가 봉인되지 않은 유사한 프로그램을 고려하십시오.

```java
interface I {}
   sealed class C permits D, E {}
   non-sealed class D extends C {}
   final class E extends C {}

   void test (C c) {
       if (c instanceof I) 
           System.out.println("It's an I");
   }
```

밀봉되지 않은 유형 `D`의 하위 유형이 `I`를 구현할 수 있기 때문에 이는 유형이 정확합니다.

이 JEP는 압축 참조 변환의 정의를 확장하여 봉인된 계층 구조를 탐색하여 컴파일 시간에 어떤 변환이 불가능한지 결정합니다.

##### Sealed classes in the JDK

JDK에서 봉인된 클래스를 사용하는 방법의 예는 JVM 엔터티에 대한 설명자를 모델링하는 `java.lang.constant` 패키지에 있습니다.

```java
package java.lang.constant;

public sealed interface ConstantDesc
    permits String, Integer, Float, Long, Double,
            ClassDesc, MethodTypeDesc, DynamicConstantDesc { ... }

// ClassDesc is designed for subclassing by JDK classes only
public sealed interface ClassDesc extends ConstantDesc
    permits PrimitiveClassDescImpl, ReferenceClassDescImpl { ... }
final class PrimitiveClassDescImpl implements ClassDesc { ... }
final class ReferenceClassDescImpl implements ClassDesc { ... } 

// MethodTypeDesc is designed for subclassing by JDK classes only
public sealed interface MethodTypeDesc extends ConstantDesc
    permits MethodTypeDescImpl { ... }
final class MethodTypeDescImpl implements MethodTypeDesc { ... }

// DynamicConstantDesc is designed for subclassing by user code
public non-sealed abstract class DynamicConstantDesc implements ConstantDesc { ... }
```

##### Sealed classes and pattern matching

봉인된 클래스의 상당한 이점은 패턴 일치와 함께 향후 릴리스에서 실현될 것입니다. `if-else` 체인으로 봉인된 클래스의 인스턴스를 검사하는 대신 사용자 코드는 유형 테스트 패턴으로 향상된 스위치를 사용할 수 있습니다. 이렇게 하면 Java 컴파일러가 패턴이 완전한지 확인할 수 있습니다.

예를 들어, 이전의 다음 코드를 고려하십시오.

```java
Shape rotate(Shape shape, double angle) {
    if (shape instanceof Circle) return shape;
    else if (shape instanceof Rectangle) return shape.rotate(angle);
    else if (shape instanceof Square) return shape.rotate(angle);
    // no else needed!
}
```

Java 컴파일러는 `instanceof` 테스트가 `Shape`의 허용된 모든 하위 클래스를 포함하는지 확인할 수 없습니다. 예를 들어 `instanceof Rectangle` 테스트가 생략된 경우 컴파일 시간 오류 메시지가 발행되지 않습니다.

대조적으로, 패턴 일치 `switch` 표현식을 사용하는 다음 코드에서 컴파일러는 `Shape`의 허용된 모든 하위 클래스가 포함되어 있는지 확인할 수 있으므로 `default` 절(또는 기타 전체 패턴)이 필요하지 않습니다. 또한 컴파일러는 세 가지 경우 중 하나라도 누락된 경우 오류 메시지를 발행합니다.

```java
Shape rotate(Shape shape, double angle) {
    return switch (shape) {   // pattern matching switch
        case Circle c    -> c; 
        case Rectangle r -> r.rotate(angle);
        case Square s    -> s.rotate(angle);
        // no default needed!
    }
}
```

##### Java Grammar

클래스 선언의 문법은 다음과 같이 수정됩니다.

```
NormalClassDeclaration:
  {ClassModifier} class TypeIdentifier [TypeParameters]
    [Superclass] [Superinterfaces] [PermittedSubclasses] ClassBody

ClassModifier:
  (one of)
  Annotation public protected private
  abstract static sealed final non-sealed strictfp

PermittedSubclasses:
  permits ClassTypeList

ClassTypeList:
  ClassType {, ClassType}
```

##### JVM support for sealed classes

JVM(Java Virtual Machine)은 런타임 시 봉인된 클래스와 인터페이스를 인식하고 승인되지 않은 서브클래스 및 서브인터페이스에 의한 확장을 방지합니다.

`Sealed`는 클래스 수정자이지만 `ClassFile` 구조에는 `ACC_SEALED` 플래그가 없습니다. 대신, 봉인된 클래스의 클래스 파일에는 봉인된 수정자를 암시적으로 나타내고 허용된 하위 클래스를 명시적으로 지정하는 `PermittedSubclasses` 속성이 있습니다.

```java
PermittedSubclasses_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 number_of_classes;
    u2 classes[number_of_classes];
}
```

허용된 하위 클래스 목록은 필수입니다. 허용된 하위 클래스가 컴파일러에서 유추된 경우에도 해당 유추된 하위 클래스는 `PermittedSubclasses` 특성에 명시적으로 포함됩니다.

허용된 하위 클래스의 클래스 파일에는 새 속성이 없습니다.

JVM이 수퍼클래스 또는 수퍼인터페이스에 `PermittedSubclasses` 속성이 있는 클래스를 정의하려고 할 때 정의되는 클래스는 속성으로 이름을 지정해야 합니다. 그렇지 않으면 `IncompatibleClassChangeError`가 발생합니다.

##### Reflection API

`java.lang.Class`에 다음 공개 메소드를 추가합니다.

* `java.lang.Class[] getPermittedSubclasses()`
* `boolean isSealed()`
`getPermittedSubclasses()` 메서드는 클래스가 봉인된 경우 클래스의 허용된 하위 클래스를 나타내는 `java.lang.Class` 객체를 포함하는 배열을 반환합니다. 클래스가 봉인되지 않은 경우 빈 배열을 반환합니다.

`isSealed` 메소드는 주어진 클래스 또는 인터페이스가 봉인된 경우 `true`를 반환합니다. (`isEnum`과 비교)