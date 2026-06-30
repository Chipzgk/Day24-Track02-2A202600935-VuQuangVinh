# src/quality/validation.py
import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite

def build_patient_expectation_suite() -> ExpectationSuite:
    """
    TODO: Tạo expectation suite cho anonymized patient data.
    """
    import great_expectations.expectations as gxe
    
    context = gx.get_context()
    suite = gx.ExpectationSuite(name="patient_data_suite")

    # 1. patient_id không được null
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="patient_id"))

    # 2. cccd phải có đúng 12 ký tự
    suite.add_expectation(gxe.ExpectColumnValueLengthsToEqual(column="cccd", value=12))

    # 3. ket_qua_xet_nghiem phải trong khoảng [0, 50]
    suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column="ket_qua_xet_nghiem", min_value=0, max_value=50))

    # 4. benh phải thuộc danh sách hợp lệ
    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    suite.add_expectation(gxe.ExpectColumnValuesToBeInSet(column="benh", value_set=valid_conditions))

    # 5. email phải match regex pattern
    suite.add_expectation(gxe.ExpectColumnValuesToMatchRegex(column="email", regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"))

    # 6. Không được có duplicate patient_id
    suite.add_expectation(gxe.ExpectColumnValuesToBeUnique(column="patient_id"))

    try:
        suite = context.suites.add(suite)
    except Exception:
        # Nếu đã tồn tại thì lấy lại
        suite = context.suites.get("patient_data_suite")
        
    return suite


def validate_anonymized_data(filepath: str) -> dict:
    """
    TODO: Validate anonymized data.
    Trả về dict: {"success": bool, "failed_checks": list, "stats": dict}
    """
    df = pd.read_csv(filepath)
    results = {
        "success": True,
        "failed_checks": [],
        "stats": {
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    }

    # Check 1: Không còn CCCD gốc dạng số thuần túy
    df_raw = pd.read_csv("data/raw/patients_raw.csv")
    if (df["cccd"] == df_raw["cccd"]).any():
        results["success"] = False
        results["failed_checks"].append("cccd_not_anonymized")

    # Check 2: Không có null values trong các cột quan trọng
    important_cols = ["patient_id", "benh", "ket_qua_xet_nghiem"]
    if df[important_cols].isnull().any().any():
        results["success"] = False
        results["failed_checks"].append("null_values_in_important_columns")

    # Check 3: Số rows phải bằng original
    if len(df) != len(df_raw):
        results["success"] = False
        results["failed_checks"].append("row_count_mismatch")

    return results
