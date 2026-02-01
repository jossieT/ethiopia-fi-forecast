import pandas as pd
import os

def read_excel_files():
    base_path = r"c:/Users/Jose/Desktop/KAIM8/WEEK10/codes/ethiopia-fi-forecast"
    xlsx_files = [
        "reference_codes.xlsx",
        "Additional Data Points Guide.xlsx"
    ]
    
    for file_name in xlsx_files:
        file_path = os.path.join(base_path, file_name)
        print(f"\n--- Checking {file_name} ---")
        if os.path.exists(file_path):
            try:
                xls = pd.ExcelFile(file_path)
                print(f"Sheet names: {xls.sheet_names}")
                
                for sheet in xls.sheet_names:
                    print(f"\nSheet: {sheet} (First 5 rows)")
                    df = pd.read_excel(file_path, sheet_name=sheet)
                    print(df.head().to_markdown(index=False))
                    
                    if file_name == "reference_codes.xlsx":
                        csv_path = os.path.join(base_path, "data/raw/reference_codes.csv")
                        df.to_csv(csv_path, index=False)
                        print(f"Saved {sheet} to {csv_path}")

            except Exception as e:
                print(f"Error reading {file_name}: {e}")
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    read_excel_files()
