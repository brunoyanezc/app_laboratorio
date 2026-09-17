from calculations.build_results import (
    build_results
)

results = build_results(
    "data/examples",
    "src/config/sample_parameters.csv",
    "src/config/method.yaml"
)

print()

print(results.columns.tolist())