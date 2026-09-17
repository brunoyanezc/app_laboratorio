from config.profile_loader import (
    load_profile
)


def main():

    profile = load_profile(
        "PVGC2"
    )

    print()

    print(
        profile["profile_name"]
    )

    print()

    print(
        profile["report_order"][:5]
    )

    print()

    print(
        "Numero analitos:",
        len(
            profile["report_order"]
        )
    )

    print()

    print(
        "Aliases:",
        profile["aliases"]
    )


if __name__ == "__main__":
    main()