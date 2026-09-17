import pandas as pd


EXCEL_FILE = "Planilla g100g.xlsx"


def main():

    df = pd.read_excel(
        EXCEL_FILE,
        sheet_name=0,
        header=None,
        engine="openpyxl"
    )

    factors = []

    for row in range(len(df)):

        compound = df.iloc[row, 1]

        if pd.isna(compound):
            continue

        compound = str(compound).strip()

        if ":" not in compound:
            continue

        try:
            tcf = float(df.iloc[row, 4])
            ffax = float(df.iloc[row, 7])
        except Exception:
            continue

        factors.append(
            {
                "compound": compound,
                "tcf": tcf,
                "ffax": ffax
            }
        )

    factors_df = pd.DataFrame(factors)

    factors_df[
        ["compound", "tcf"]
    ].to_csv(
        "src/config/tcf.csv",
        index=False
    )

    factors_df[
        ["compound", "ffax"]
    ].to_csv(
        "src/config/ffax.csv",
        index=False
    )

    print()
    print("Factores exportados")
    print(factors_df.head())


if __name__ == "__main__":
    main()