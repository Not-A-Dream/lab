# Lab

머신러닝, 생성모델, 시계열, 그리고 인지/뇌 기반 연구를 위한 개인 연구 저장소입니다.

이 저장소는 다음을 목적으로 사용합니다.

* 논문 재현
* 모델 실험
* 알고리즘 연구
* 심리학 / 뇌 기반 머신러닝 아이디어 정리
* 향후 on-device / NPU / neuromorphic 연구

---

## 구조

```
lab/
  diffusion/        # diffusion, flow matching, 생성모델 연구
  llm/              # LLM, transformer, 언어모델
  time-series/      # 시계열 예측, sequence 모델, TS foundation model
  psychology/       # 인지, 신경과학, brain-inspired 아이디어

  data/             # 데이터셋 (git 추적 안함)
  outputs/          # 실험 결과 / 로그 (git 추적 안함)
  checkpoints/      # 모델 weight / ckpt (git 추적 안함)
```

---

## 저장 정책

큰 파일은 GitHub에 커밋하지 않습니다.

다음 항목은 업로드 금지

* 데이터셋
* 모델 체크포인트
* 로그 파일
* tensorboard 결과
* 대용량 numpy / torch 파일

아래 디렉토리는 gitignore로 제외합니다.

```
data/
outputs/
checkpoints/
```

데이터와 weight는 로컬 또는 외부 저장소를 사용합니다.

---

## 목적

이 저장소는 다음 연구를 위한 장기 저장소입니다.

* Diffusion 모델
* Large Language Model
* Time-series foundation model
* Multimodal learning
* Neuroscience / Psychology 기반 AI
* Neuromorphic / NPU / On-device AI

---

## 참고

이 저장소는 실험용이며 구조는 연구 진행에 따라 변경될 수 있습니다.
