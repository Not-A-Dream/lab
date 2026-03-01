# 엄마 수학자(Mother Math) & 아기 수학자(Baby Math)

`mama_baby_math.py`는 **초미니(연구용) 수학 딥러닝 모델**입니다.  
Transformer(문자 단위 LM)를 **무한 생성 데이터**로 학습시키고, **커리큘럼 학습**과 **자리수(OOD) 일반화 평가**를 포함합니다.

- **엄마 수학자 (mother)**: 사칙연산(+, -, *, /) 중심 학습
- **아기 수학자 (baby)**: `수량 감각(비교)` → `점→숫자 매핑` → `사칙연산` 순서로 발달 커리큘럼

---

## 1) 준비물(Requirements)

- Python 3.9+ 권장 (3.13도 동작 가능)
- PyTorch (CPU 버전이면 CPU로 학습, CUDA 버전이면 GPU 사용 가능)

설치(예):
```bash
pip install torch
```

> ⚠️ CUDA 에러가 뜨면?  
> `Torch not compiled with CUDA enabled`는 **CUDA 지원 PyTorch가 아닌 CPU 빌드**를 설치한 상태입니다.  
> 이 경우 `--device cpu`로 실행하면 정상 동작합니다.

---

## 2) 실행(Quick Start)

### 2.1 아기 수학자 학습 (추천)
```bash
python mama_baby_math.py --mode baby --op add --train_steps 40000 --device cpu
```

### 2.2 엄마 수학자 학습
```bash
python mama_baby_math.py --mode mother --op add --train_steps 30000 --device cpu
```

### 2.3 (가능할 때) CUDA/GPU 사용
GPU가 있고 CUDA PyTorch를 설치했다면:
```bash
python mama_baby_math.py --mode baby --op add --train_steps 40000 --device cuda
```

---

## 3) 핵심 옵션 설명

| 옵션 | 설명 | 예시 |
|---|---|---|
| `--mode` | `baby` 또는 `mother` | `--mode baby` |
| `--op` | `add/sub/mul/div/mix` | `--op mix` |
| `--train_steps` | 총 학습 스텝 | `--train_steps 40000` |
| `--batch_size` | 배치 크기(크면 빠르지만 메모리↑) | `--batch_size 64` |
| `--device` | `cpu` 또는 `cuda` | `--device cpu` |
| `--eval_every` | 몇 스텝마다 평가할지 | `--eval_every 2000` |
| `--save_path` | 학습 결과 저장 경로 | `--save_path mama_baby_math.pt` |

---

## 4) 출력 로그 읽는 법

학습 중 이런 로그가 나옵니다:

```text
step   200 | task=compare | max_n=3 | loss 0.0008
```

- `task=compare`: 점(•)의 개수 비교(왼쪽이 많으면 L, 오른쪽이 많으면 R, 같으면 =)
- `max_n=3`: 점 개수 범위(0~3)
- `loss`: 작을수록 잘 맞추는 중(0에 가까우면 거의 완벽)

평가 로그(예):
```text
[eval@2000] current_stage: task=compare max_n=3
  [compare]  max_n=3  acc=1.000
  [dots2num] max_n=6  acc=0.950
  [arith] train_digits=1 test_digits=3 acc=0.120
```

- `acc`: 정확도 (1.0 = 100%)
- `compare`, `dots2num`: 아기 단계 과제 성능
- `arith`: 사칙연산 성능  
  - `train_digits`: 현재 학습 단계(예: 2자리까지 학습 중)  
  - `test_digits`: 더 긴 자리수로 OOD 테스트 (일반화 확인)

> ⭐ 자리수 일반화 핵심  
> `train_digits=2`인데 `test_digits=4`가 잘 나오면 “절차”를 배운 가능성이 높습니다.  
> 반대로 급락하면 “패턴 암기” 가능성이 큽니다.

---

## 5) 커리큘럼(아기 수학자)

`--mode baby`일 때 단계는 대략 아래 순서로 진행됩니다.

1. `compare`: `•••?••=` → `L/R/=`  
2. `dots2num`: `••••->` → `4`  
3. `arith`: `2+7=` → `9` (자리수를 1→2→3→4로 확장)

---

## 6) 결과 파일 저장

학습이 끝나면 기본으로 체크포인트가 저장됩니다:

- 기본값: `mama_baby_math.pt`
- 변경: `--save_path something.pt`

저장 내용:
- 모델 가중치(state_dict)
- 실행 args
- 토큰 사전(tokens)

> 불러와서 추론/추가 학습을 하려면 로딩 코드가 필요합니다.  
> 원하시면 “로드 + 대화형(입력하면 답 출력)” 스크립트도 만들어 드릴게요.

---


---

## 6.5) 대화형 추론(infer.py)

학습이 끝나면 체크포인트(`.pt`)를 불러와서 **직접 프롬프트를 넣고 답을 받는** 대화형 추론을 할 수 있습니다.

### 실행
```bash
python infer.py --ckpt mama_baby_math.pt --device cpu
```

CUDA PyTorch + NVIDIA GPU가 있는 경우:
```bash
python infer.py --ckpt mama_baby_math.pt --device cuda
```

### 입력 예시
- 점 비교:
```text
•••?••=
```
출력: `L` (왼쪽이 더 많음) / `R` / `=`

- 점→숫자:
```text
••••••->
```
출력: `6`

- 사칙연산:
```text
12+34=
99+7=
```
출력: `46`, `106`

종료: `:quit` 또는 `:q`


## 7) 자주 겪는 문제(FAQ)

### Q1. `Torch not compiled with CUDA enabled`가 떠요
- 해결: **CPU로 실행**
```bash
python mama_baby_math.py --mode baby --op add --train_steps 10000 --device cpu
```
- GPU를 쓰고 싶다면: CUDA 지원 PyTorch로 재설치 필요(PC에 NVIDIA GPU가 있어야 함)

### Q2. CPU가 너무 느려요
- 빠른 테스트용 설정:
```bash
python mama_baby_math.py --mode baby --op add --train_steps 5000 --batch_size 64 --eval_every 1000 --device cpu
```
- 가능하면 `--batch_size`를 상황에 맞게 줄이거나, 학습 스텝을 줄여서 실험을 빠르게 반복하세요.

---

## 8) 다음 실험 아이디어(추천)

1) **엄마 vs 아기 비교 실험**  
- `--mode mother`로 바로 사칙연산 학습 vs `--mode baby`로 발달 후 사칙연산  
- OOD 자리수 정확도 비교

2) **mix 연산 실험**  
```bash
python mama_baby_math.py --mode mother --op mix --train_steps 80000 --device cpu
```

3) **일반화 개선(다음 단계)**  
- 정답만 내게 하지 말고 **세로셈 스크래치패드(중간 과정)**를 강제하면 자리수 일반화가 좋아지는 경향이 있습니다.  
원하시면 “스크래치패드 버전”도 만들어 드릴게요.
