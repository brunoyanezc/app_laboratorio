from parser.discover import discover_reports


def main():

    samples = discover_reports("data/examples")

    print()
    print("MUESTRAS ENCONTRADAS")
    print("-" * 40)

    for sample in samples:

        print(
            sample["sample_id"],
            "->",
            sample["report_file"]
        )


if __name__ == "__main__":
    main()
