import os
import glob
import hashlib
import pandas as pd
import numpy as np


def mask_pii(df):
    # 성명 SHA-256 해시 변환 및 생년월일 연도만 추출
    if "user_name" in df.columns:
        df["user_id"] = df["user_name"].astype(str).apply(
            lambda x: hashlib.sha256(x.strip().encode("utf-8")).hexdigest()[:12]
        )
        df = df.drop(columns=["user_name"])

    if "birth_date" in df.columns:
        df["birth_year"] = df["birth_date"].astype(str).str[:4]
        df = df.drop(columns=["birth_date"])

    return df


def impute_checkout_time(df):
    # 퇴실 미체크(NaN) 보정: 19시 이전 입실 -> 19:00 점검 기준 / 19시 이후 입실 -> 21:00 마감 기준
    df["check_in"] = pd.to_datetime(df["check_in"])
    df["check_out"] = pd.to_datetime(df["check_out"], errors="coerce")

    na_mask = df["check_out"].isna()
    date_str = df.loc[na_mask, "check_in"].dt.strftime("%Y-%m-%d")
    is_night = df.loc[na_mask, "check_in"].dt.hour >= 19

    fallback_ts = np.where(is_night, date_str + " 21:00:00", date_str + " 19:00:00")
    df.loc[na_mask, "check_out"] = pd.to_datetime(fallback_ts)
    df["is_imputed"] = na_mask
    return df


def tag_short_visits(df, threshold_min=5):
    # 단순 출력·물품 대여 등 5분 미만 단기 방문 노이즈 분리
    duration = (df["check_out"] - df["check_in"]).dt.total_seconds() / 60.0
    df["stay_min"] = duration.clip(lower=0)

    noise_cond = (df["stay_min"] < threshold_min) | (df["purpose"].isin(["출력", "대여"]))
    df["visit_type"] = np.where(noise_cond, "utility_noise", "regular_stay")
    return df


def run_preprocessing(raw_dir="data/raw", out_path="data/processed/merged_logs.csv"):
    excel_files = glob.glob(os.path.join(raw_dir, "*.xlsx"))
    if not excel_files:
        print(f"[Skip] '{raw_dir}' 경로에 원본 엑셀 파일이 없습니다. (개인정보 보안상 원본 데이터는 Git에서 제외됨)")
        return None

    frames = []
    for fp in excel_files:
        temp = pd.read_excel(fp)
        temp["source_file"] = os.path.basename(fp)
        frames.append(temp)

    merged = pd.concat(frames, ignore_index=True)
    merged = mask_pii(merged)
    merged = impute_checkout_time(merged)
    merged = tag_short_visits(merged)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    merged.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"[Done] 전처리 완료: 총 {len(merged):,}건 -> {out_path}")
    return merged


if __name__ == "__main__":
    run_preprocessing()