import pandas as pd
import pytest

from preprocess_logs import clean_log, prepare_workbooks


def raw_frame():
    return pd.DataFrame({
        "user_name": ["실제이름A", "실제이름B", "실제이름C", "실제이름D", "실제이름E"],
        "birth_date": ["2001-01-01"] * 5,
        "contact": ["010-0000-0000"] * 5,
        "purpose": ["스터디", "상담", "출력", "프로그램", "대여"],
        "check_in": ["2026-03-01 09:00", "2026-03-01 18:00", "2026-03-01 19:00", "2026-03-01 14:00", "2026-03-01 15:00"],
        "check_out": ["2026-03-01 10:00", None, "2026-03-01 19:03", "2026-03-01 13:50", "2026-03-01 15:02"],
    })


def test_missing_checkout_stays_missing() -> None:
    out = clean_log(raw_frame())
    assert pd.isna(out.loc[1, "check_out"])
    assert pd.isna(out.loc[1, "observed_minutes"])
    assert out.loc[1, "visit_type"] == "missing_checkout"


def test_bad_time_order_is_flagged_not_clipped() -> None:
    out = clean_log(raw_frame())
    assert out.loc[3, "visit_type"] == "invalid_time_order"
    assert pd.isna(out.loc[3, "observed_minutes"])


def test_pii_is_dropped_and_visits_preserved() -> None:
    out = clean_log(raw_frame())
    assert "user_name" not in out and "birth_date" not in out and "contact" not in out
    assert len(out) == 5
    assert out.loc[2, "visit_type"] == "utility_visit"
    assert out.loc[4, "visit_type"] == "utility_visit"


def test_unstructured_purpose_is_not_exported() -> None:
    raw = raw_frame()
    raw.loc[0, "purpose"] = "홍길동 연락처 010-1234-5678"
    assert clean_log(raw).loc[0, "purpose"] == "기타"


def test_free_text_site_is_not_exported() -> None:
    raw = raw_frame()
    raw["site"] = ["본원", "홍길동의 집 010-1234-5678", "외곽", None, "구래"]
    clean = clean_log(raw)
    assert clean["site"].tolist() == ["본원", "기타", "외곽", "기타", "구래"]


def test_missing_columns_raise() -> None:
    with pytest.raises(ValueError, match="Missing required"):
        clean_log(pd.DataFrame({"check_in": ["2026-01-01"]}))


def test_private_excel_roundtrip(tmp_path) -> None:
    input_dir = tmp_path / "private"
    input_dir.mkdir()
    raw_frame().to_excel(input_dir / "secret.xlsx", index=False)
    out_file = input_dir / "processed.csv"
    summary = prepare_workbooks(input_dir, out_file)
    assert summary["total_rows"] == 5
    assert summary["missing_checkout"] == 1
    saved = pd.read_csv(out_file)
    assert not any(x in saved for x in ("user_name", "birth_date", "contact"))
    assert "secret" not in str(saved.to_dict())
