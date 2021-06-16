# 작동 방식
1. Line, Parallel, Bridge 클래스를 이용해 직-병렬 변환과 Y-Δ 변환을 수행한다.
   -회로를 그래프로 보고 인접 행렬을 구하면 구조를 파악하기 쉬워진다.
2. 전압 소스 1개와 저항 1개만 있는 회로로 변환해 회로에 흐르는 전류를 구한다.
3. 각각의 클래스에 따라 그 안의 요소들에 적절하게 전압, 전류를 분배한다.
------
# 실험 결과
![Pspice](https://github.com/wlsdyd7511/circuitSimulator/blob/master/img/pspice.png)
![our](https://github.com/wlsdyd7511/circuitSimulator/blob/master/img/our.png)
이미 검증된 프로그램인 Pspice의 결과와 비교했을 때 브릿지 구조의 밖은 전류가 거의 비슷한 것을 알 수 있다.
따라서 브릿지 구조의 전체 저항을 구하는 식에는 문제가 없지만, 전압과 전류를 분배하는 과정에 문제가 있을 것이다.
브릿지 밖에도 약간의 오차가 있는 것은 부동 소수점 형식을 이용해 계산했기 때문에 어쩔 수 없이 발생하는 오차다.
