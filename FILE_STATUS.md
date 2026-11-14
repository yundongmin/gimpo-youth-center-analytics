# GitHub 최종본 — 파일별 변경 내역

검토 대상: 직전 `gimpo-youth-center-analytics-reviewed.zip` (30개 파일)

- **수정 6개 / 유지 24개 / 삭제 0개**, 최종 파일 30개 + 이 목록 1개
- **검증:** `pytest` 13개 통과, 2025 EDA와 2026 KPI 재생성, 합성 Excel 생성·전처리 실행, Python compileall 정상
- **유지:** 기존 발표 이미지 `slides/1.png`~`slides/9.png`는 일절 수정하지 않음

## 수정된 파일

| 파일 | 반영 내용 |
|---|---|
| `.github/workflows/python-checks.yml` | GitHub Actions에서 한글 차트 글꼴 설치 |
| `README.md` | 2025년 직영 전환·2026년 5월 평가 준비 맥락, 평가/국비 성과 분리, 근무 종료일 미확정 표시 |
| `docs/CODE_REVIEW.md` | 최신 사실관계와 외부 검증 범위 기록 |
| `docs/metric_definitions.md` | 직영 전환 배경·방문 기록 해석·비공개 평가 정보·재식별 위험 구분 |
| `src/preprocess_logs.py` | `site` 자유기술을 허용 목록으로 제한, 개인정보가 섞인 현장명 배제 |
| `tests/test_preprocess.py` | `site` 자유기술 제거 회귀 테스트 추가 |

## 유지된 파일

아래 파일은 기존 개선본과 **파일 내용이 동일**합니다.

| 파일 | 상태 |
|---|---|
| `.gitignore` | 유지 |
| `data/aggregates.json` | 유지 |
| `outputs/2025_baseline_eda.png` | 유지 |
| `outputs/2026_kpi_comparison.json` | 유지 |
| `outputs/2026_kpi_comparison.png` | 유지 |
| `requirements-dev.txt` | 유지 |
| `requirements.txt` | 유지 |
| `scripts/make_demo_workbook.py` | 유지 |
| `slides/1.png` | 유지 |
| `slides/2.png` | 유지 |
| `slides/3.png` | 유지 |
| `slides/4.png` | 유지 |
| `slides/5.png` | 유지 |
| `slides/6.png` | 유지 |
| `slides/7.png` | 유지 |
| `slides/8.png` | 유지 |
| `slides/9.png` | 유지 |
| `src/charting.py` | 유지 |
| `src/eda_2025_baseline.py` | 유지 |
| `src/evaluate_2026_kpi.py` | 유지 |
| `src/metrics.py` | 유지 |
| `tests/conftest.py` | 유지 |
| `tests/test_metrics.py` | 유지 |
| `tests/test_reports.py` | 유지 |

## 확인이 남은 사실

1. **평가 결과:** D→B는 제공된 발표 자료의 표기입니다. 공식 점수와 통보 자료는 외부에 없으므로 코드로 검증하거나 공개 결과처럼 단정하지 않았습니다.
2. **국비 기사:** 2026년 청년성장프로젝트 공모 선정·국비 4,200만 원과 운영 평가 등급을 하나의 인과 관계로 연결하지 않았습니다.
3. **개인 근무 종료일:** 기존 README는 `2026.06`으로 기재했으나 이전 경력 기록과 차이가 있어 종료일은 경력증명서 대조 후 추가하도록 본문에서 생략했습니다.
4. **발표 이미지:** 원본 9장은 수정하지 않았으므로 해당 이미지의 D→B 서술·성과 인과 표현·대외 공개 가능 여부를 제출 전 점검해야 합니다.
5. **데이터 안전:** 개인별 기록은 ZIP에서 제외했고, 비공개 행정 데이터 사용 권한·스크린샷의 비식별 여부는 별도 확인해야 합니다.

## 실행

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
python src/eda_2025_baseline.py
python src/evaluate_2026_kpi.py
python scripts/make_demo_workbook.py
python src/preprocess_logs.py --input-dir data/private
```
