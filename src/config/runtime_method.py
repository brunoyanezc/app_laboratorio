import yaml


def create_runtime_method_file(
    density,
    purity,
    flask_volume_ml,
    stock_mass_g,
    c23_tag_factor,
    filename
):

    config = {
        "c23": {
            "density": density,
            "purity": purity,
            "flask_volume_ml": flask_volume_ml,
            "stock_mass_g": stock_mass_g,
            "c23_tag_factor": c23_tag_factor
        },
        "fame": {
            "exclude_internal_standard": True,
            "exclude_ni": False
        }
    }

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        yaml.dump(
            config,
            f,
            sort_keys=False
        )

    return filename