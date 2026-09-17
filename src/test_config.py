from config.config_loader import (
    load_method_config,
    load_sample_parameters
)


def main():

    method = load_method_config(
        "src/config/method.yaml"
    )

    samples = load_sample_parameters(
        "src/config/sample_parameters.csv"
    )

    print()
    print("CONFIGURACION METODO")
    print("-" * 40)

    print(method)

    print()
    print("PARAMETROS MUESTRAS")
    print("-" * 40)

    print(samples)


if __name__ == "__main__":
    main()