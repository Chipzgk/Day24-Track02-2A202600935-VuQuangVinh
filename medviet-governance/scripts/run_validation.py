import os
import sys

# Thêm đường dẫn project vào sys.path để import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.pii.anonymizer import MedVietAnonymizer
from src.quality.validation import build_patient_expectation_suite, validate_anonymized_data
import great_expectations as gx

def main():
    print("=== Running Great Expectations on Raw Data ===")
    df_raw = pd.read_csv("data/raw/patients_raw.csv")
    
    # Tạo/Lấy Expectation Suite
    print("[1] Building/Loading Expectation Suite...")
    suite = build_patient_expectation_suite()
    
    # Chạy validation trên raw data (sẽ có nhiều lỗi như duplicate nếu có, nhưng raw data ở đây có thể pass GE cơ bản)
    print("\n=== Anonymizing Data ===")
    anonymizer = MedVietAnonymizer()
    print("[2] Anonymizing data...")
    df_anon = anonymizer.anonymize_dataframe(df_raw)
    
    # Lưu ra file tạm để chạy hàm validate_anonymized_data
    os.makedirs("data/processed", exist_ok=True)
    anon_path = "data/processed/patients_anonymized.csv"
    df_anon.to_csv(anon_path, index=False)
    print(f"[3] Saved anonymized data to {anon_path}")
    
    print("\n=== Validation of Anonymized Data ===")
    results = validate_anonymized_data(anon_path)
    print(f"Validation Results: {results}")

if __name__ == "__main__":
    main()
