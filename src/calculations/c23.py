def calculate_c23_concentration(
    stock_mass_g,
    flask_volume_ml,
    density_g_ml,
    purity,
):
    """
    Reproduce la hoja Concentración C23
    """

    solvent_mass_g = (
        flask_volume_ml * density_g_ml
    )

    concentration_g_g = (
        stock_mass_g
        / solvent_mass_g
    )

    concentration_g_g *= purity

    return {
        "solvent_mass_g": solvent_mass_g,
        "concentration_g_g": concentration_g_g,
    }


def calculate_added_c23_mass(
    solution_weight_g,
    concentration_g_g,
):
    """
    Masa real de C23 agregada a una muestra
    """

    return (
        solution_weight_g
        * concentration_g_g
    )