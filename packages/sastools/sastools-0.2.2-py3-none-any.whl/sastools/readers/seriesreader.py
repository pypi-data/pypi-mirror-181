"""Module for parsing AnIMLDocument objects for Series elements by their
seriesID attribute and create Pandas DataFrames from them.
"""

import pandas as pd

from pyaniml import AnIMLDocument


class SeriesReader:
    """Read an AnIML document and create a `pandas.DataFrame` from any
    Series element within.
    """

    def __init__(self, animl_doc: AnIMLDocument):
        """Pass an AnIMLDocument object from which one or more Series
        elements should be read.

        Args:
            animl_doc (AnIMLDocument): AnIML document containing one or more Series to be read.
        """
        self._animl_doc = animl_doc
        self._available_seriesIDs = []
        self._selected_seriesIDs = []

    def __repr__(self):
        return "AnIML Series-element Reader"

    def _parse_available_seriesIDs(self) -> list[str]:
        # Parse AnIMLDocument object and return the seriesID attribute
        # from every Series element within the document.
        available_seriesIDs = []
        experiment_steps = self._animl_doc.experiment_step_set.experiment_steps
        for experiment_step in experiment_steps:
            results = experiment_step.result.results
            for result in results:
                # check Series in Result
                try:
                    available_seriesIDs.append(result.id[:-2])
                except:
                    pass
                # check Series in Result.SeriesSet
                try:
                    for series in result.series:
                        available_seriesIDs.append(series.id[:-2])
                except:
                    pass
                # check Categories
                try:
                    for category in result.content:
                        # check for Series in Result.Category
                        try:
                            available_seriesIDs.append(category.id[:-2])
                        except:
                            pass
                        # check for Series in Result.Category.SeriesSet
                        try:
                            for series in category.series:
                                available_seriesIDs.append(series.id[:-2])
                        except:
                            pass
                except:
                    pass
        return list(dict.fromkeys(available_seriesIDs))

    def create_dataframe(self) -> pd.DataFrame:
        """Create `pandas.DataFrame` from `selected_seriesID` property
        and return it.

        Returns:
            pandas.DataFrame: DataFrame containing all Series elements selected by their seriesID attribute.
        """
        dict_of_data = {}
        for sample_id in self._selected_seriesIDs:
            experiment_steps = (
                self._animl_doc.experiment_step_set.experiment_steps
            )
            for experiment_step in experiment_steps:
                results = experiment_step.result.results
                for result in results:
                    # check Series in Result
                    try:
                        if sample_id in result.id:
                            dict_of_data[
                                result.id
                            ] = result.individual_value_set.data
                    except:
                        pass
                    # check Series in Result.SeriesSet
                    try:
                        for series in result.series:
                            if sample_id in series.id:
                                dict_of_data[
                                    series.id
                                ] = series.individual_value_set.data
                    except:
                        pass
                    # check Categories
                    try:
                        for category in result.content:
                            # check for Series in Result.Category
                            try:
                                if sample_id in category.id:
                                    dict_of_data[
                                        category.id
                                    ] = category.individual_value_set.data
                            except:
                                pass
                            # check for Series in Result.Category.SeriesSet
                            try:
                                for series in category.series:
                                    if sample_id in series.id:
                                        dict_of_data[
                                            series.id
                                        ] = series.individual_value_set.data
                            except:
                                pass

                    except:
                        pass
        return pd.DataFrame(
            {key: pd.Series(value) for key, value in dict_of_data.items()}
        )

    @property
    def available_seriesIDs(self) -> list[str]:
        """Get SeriesID elements available in the AnIML document."""
        self._available_seriesIDs = self._parse_available_seriesIDs()
        return self._available_seriesIDs

    @property
    def selected_seriesIDs(self) -> list[str]:
        """Get list of seriesID selected so far."""
        return self._selected_seriesIDs

    @selected_seriesIDs.setter
    def selected_seriesIDs(self, list_of_ids: list[str]) -> None:
        for series_id in list_of_ids:
            self._selected_seriesIDs.append(series_id)
