from rich.console import Console

from ndcc.compare import DraftCapitalComparator


def main():
    console = Console()
    comparator = DraftCapitalComparator()
    tables = comparator.get_tables()
    for table in tables:
        console.print(table)
