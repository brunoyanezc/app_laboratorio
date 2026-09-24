def calculate_wfamex(
    area_x,
    area_c23,
    mass_c23_added,
    tcf,
    c23_tag_factor,
):
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
    return wfamex * ffax


def calculate_g100g(
    wx,
    sample_weight_g,
):
    return (
        wx
        / sample_weight_g
        * 100
    )