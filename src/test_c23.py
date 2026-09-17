from config.config_loader import (
    load_method_config,
)

from calculations.c23 import (
    calculate_c23_concentration,
    calculate_added_c23_mass,
)


def main():

    method = load_method_config(
        "src/config/method.yaml"
    )

    c23 = method["c23"]

    result = calculate_c23_concentration(
        stock_mass_g=c23["stock_mass_g"],
        flask_volume_ml=c23["flask_volume_ml"],
        density_g_ml=c23["density"],
        purity=c23["purity"],
    )

    print()
    print("Masa solvente:")
    print(result["solvent_mass_g"])

    print()
    print("Concentración C23:")
    print(result["concentration_g_g"])

    added = calculate_added_c23_mass(
        solution_weight_g=0.15,
        concentration_g_g=result[
            "concentration_g_g"
        ],
    )

    print()
    print("Masa C23 agregada:")
    print(added)


if __name__ == "__main__":
    main()