import os.path

import pandas
from rich.table import Table

from ndcc import input


class DraftCapitalComparator:
    def __init__(self):
        self.tables: list[Table] = []
        self.collection_rows: list[tuple] = []
        self.charts_df = self._get_charts_df()

    def get_tables(self) -> list[Table]:
        collection_count: int = input.get_collection_count()
        self._add_pick_tables(collection_count)
        self._add_comparison_table()

        return self.tables

    def _get_charts_df(self) -> pandas.DataFrame:
        selected_charts: list[str] = input.get_selected_charts()
        index_and_selected_charts: list[str] = ["Pick #"] + selected_charts

        cwd: str = os.path.dirname(os.path.realpath(__file__))
        csv_path: str = os.path.join(cwd, "data", "charts.csv")

        charts_df: pandas.DataFrame = pandas.read_csv(
            csv_path, usecols=index_and_selected_charts, index_col=0
        )
        return charts_df

    def _add_comparison_table(self):
        comparison_table: Table = Table(title="Comparison", style="purple")
        comparison_table.add_column("Collection")
        for chart in self.charts_df.columns:
            comparison_table.add_column(chart)
        for row in self.collection_rows:
            comparison_table.add_row(*row)

        self.tables.insert(0, comparison_table)

    def _add_pick_tables(self, collection_count: int):
        for collection_number in range(1, collection_count + 1):

            collection_name: str = input.get_collection_name(collection_number)
            picks: list[int] = input.get_picks(collection_number)

            filtered_df: pandas.DataFrame = self.charts_df[
                self.charts_df.index.isin(picks)
            ]
            collection_row: tuple = (collection_name,)
            for chart in filtered_df.columns:
                collection_row += (str(filtered_df[chart].sum()),)

            self.collection_rows.append(collection_row)
            self.tables.append(self._get_pick_table(collection_name, filtered_df))

    def _get_pick_table(
        self, collection_name: str, filtered_df: pandas.DataFrame
    ) -> Table:

        pick_table: Table = Table(title=collection_name)
        pick_table.add_column("Pick", style="cyan")

        pick_rows: list[tuple] = []

        for tup in filtered_df.itertuples(name=None):
            new_tup = tuple()
            for i in tup:
                new_tup += (str(i),)
            pick_rows.append(new_tup)

        for chart in filtered_df.columns:
            pick_table.add_column(chart)

        for row in pick_rows:
            pick_table.add_row(*row)

        return pick_table
