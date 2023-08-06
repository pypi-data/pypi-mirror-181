import sys
from prompt_toolkit.shortcuts import checkboxlist_dialog, input_dialog
from prompt_toolkit.completion import FuzzyWordCompleter

from ndcc import validate


def get_selected_charts() -> list[str]:
    selected_charts: list[str] = checkboxlist_dialog(
        text="Select value charts to use",
        values=[
            ("Jimmy Johnson", "Jimmy Johnson"),
            ("Rich Hill", "Rich Hill"),
            ("Fitzgerald/Spielberger", "Fitzgerald/Spielberger"),
            ("Kevin Meers", "Kevin Meers"),
            ("PFF", "PFF"),
            ("Michael Lopez", "Michael Lopez"),
            ("Chase Stuart", "Chase Stuart"),
        ],
        default_values=(
            "Jimmy Johnson",
            "Rich Hill",
            "Fitzgerald/Spielberger",
            "Kevin Meers",
            "PFF",
            "Michael Lopez",
            "Chase Stuart",
        ),
    ).run()
    if selected_charts is None:
        sys.exit()
    return selected_charts


def get_collection_count() -> int:
    selected_number_of_pick_collections: int = int(
        input_dialog(
            text="Enter the number of pick collections to compare: ",
            validator=validate.get_collection_count_validator(),
        ).run()
    )
    if selected_number_of_pick_collections is None:
        sys.exit()
    return selected_number_of_pick_collections


def get_collection_name(collection_number: int) -> str:
    collection_name: str = input_dialog(
        text=f"Enter a name/identifier for collection {collection_number}, e.g. 'MIN receive': ",
        validator=validate.get_collection_name_validator(),
        completer=FuzzyWordCompleter(
            [
                "ARZ",
                "ATL",
                "BLT",
                "BUF",
                "CAR",
                "CHI",
                "CIN",
                "CLV",
                "DAL",
                "DEN",
                "DET",
                "GB",
                "HST",
                "IND",
                "JAX",
                "KC",
                "LV",
                "LAC",
                "LAR",
                "MIA",
                "MIN",
                "NE",
                "NO",
                "NYG",
                "NYJ",
                "PHI",
                "PIT",
                "SF",
                "SEA",
                "TB",
                "TEN",
                "WAS",
                "receive",
                "old",
                "new",
            ],
        ),
    ).run()
    if collection_name is None:
        sys.exit()
    return collection_name


def get_picks(collection_number: int) -> list[int]:
    picks_raw: list[str] = (
        input_dialog(
            text=f"Enter the picks in collection {collection_number}, separated by spaces: ",
            validator=validate.get_pick_validator(),
        )
        .run()
        .split()
    )
    if picks_raw is None:
        sys.exit()
    picks: list[int] = [int(i) for i in picks_raw]
    return picks
