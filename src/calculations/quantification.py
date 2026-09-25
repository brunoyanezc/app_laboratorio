def calculate_wfamex(
    area_x,
    area_c23,
    mass_c23_added,
    tcf,
    c23_tag_factor,
):

    if area_c23 is None:
        return 0.0

    if area_c23 <= 0:
        return 0.0

    return (
        area_x
        / area_c23
        * mass_c23_added
        * tcf
        * c23_tag_factor
    )


def calculate_wx(
    wfamex,
    ffax,
):

    if wfamex is None:
        return 0.0

    return wfamex * ffax


def calculate_g100g(
    wx,
    sample_weight_g,
):

    if sample_weight_g is None:
        return 0.0

    if sample_weight_g <= 0:
        return 0.0

    return (
        wx
        / sample_weight_g
        * 100
    )