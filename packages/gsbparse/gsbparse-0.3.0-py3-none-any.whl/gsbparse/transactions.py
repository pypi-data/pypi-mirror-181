"""Define a representation of transactions."""

from functools import cached_property
from typing import TextIO, Union

import pandas as pd

from gsbparse import AccountFile


class Transactions:
    """Represents transactions of a Grisbi file.

    The difference with an AccountFile["Transaction"] is that we here merge the
    different sections of the AccountFile together to replace "foreign keys" in
    the AccountFile["Transaction"].df records with their names, using the other
    sections of the .gsb file as lookup tables.

    Attributes:
        df (pd.DataFrame): Transactions of the Grisbi file
    """

    def __init__(self, source: Union[str, TextIO]) -> None:
        """Create the user-friendly Transactions df from an AccountFile instance."""
        self.source = source

    def __repr__(self) -> str:
        """Return a representation of an Transaction object."""
        return f"Transactions({self.source})"

    @cached_property
    def account_file(self) -> AccountFile:
        """Return the instantiated account file containing the transactions."""
        return AccountFile(self.source)

    @cached_property
    def _df(self) -> pd.DataFrame:
        """Return the transactions as a pd.DataFrame, with foreign keys merged."""
        return (
            self._format_transactions_columns(self.account_file.transaction)
            .pipe(self._add_account_details)
            .pipe(self._add_party_details)
            .pipe(self._add_currency_details)
            .pipe(self._add_subcategory_details)
            .pipe(self._add_category_details)
            .pipe(self._add_subbudgetary_details)
            .pipe(self._add_budgetary_details)
            .pipe(self._add_financialyear_details)
            .pipe(self._add_reconcile_details)
        )

    def get_transactions(
        self,
        columns: Union[list, dict, None] = None,
        ignore_mother_transactions: bool = False,
    ):
        """Return all or a subset of the transactions."""
        if ignore_mother_transactions:
            df = self._df[~self._df[("Transaction", "Br")]]
        else:
            df = self._df

        if columns is None:
            return df
        elif type(columns) == list:
            return df[columns]
        elif type(columns) == dict:
            # “Columns name mapper doesn't relate with [index] level.”
            # Cf. https://stackoverflow.com/a/67458211/5433628
            cols_rename_mapping = {key[1]: value for key, value in columns.items()}
            return df[columns.keys()].rename(columns=cols_rename_mapping)

    @staticmethod
    def index_column_names(
        df: pd.DataFrame,
        prefix: str,
    ) -> pd.DataFrame:
        """Add a leading prefix to all columns of a dataframe."""
        df.columns = pd.MultiIndex.from_product([[prefix], df.columns])

        return df

    def _add_account_details(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions.merge(
            type(self).index_column_names(
                df=self.account_file.sections["Account"].df,
                prefix=self.account_file.sections["Account"].section,
            ),
            how="left",
            left_on=[("Transaction", "Ac")],
            right_index=True,
            validate="m:1",
        ).drop(columns=[("Transaction", "Ac")])

    def _add_currency_details(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions.merge(
            type(self).index_column_names(
                df=self.account_file.sections["Currency"].df,
                prefix=self.account_file.sections["Currency"].section,
            ),
            how="left",
            left_on=[("Transaction", "Cu")],
            right_index=True,
            validate="m:1",
        ).drop(columns=[("Transaction", "Cu")])

    def _add_party_details(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions.merge(
            type(self).index_column_names(
                df=self.account_file.sections["Party"].df,
                prefix=self.account_file.sections["Party"].section,
            ),
            how="left",
            left_on=[("Transaction", "Pa")],
            right_index=True,
            validate="m:1",
        ).drop(columns=[("Transaction", "Pa")])

    def _add_subcategory_details(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions.merge(
            type(self).index_column_names(
                df=self.account_file.sections["Sub_category"].df,
                prefix=self.account_file.sections["Sub_category"].section,
            ),
            how="left",
            left_on=[("Transaction", "Ca"), ("Transaction", "Sca")],
            right_index=True,
            validate="m:1",
        ).drop(columns=[("Transaction", "Sca")])

    def _add_category_details(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions.merge(
            type(self).index_column_names(
                df=self.account_file.sections["Category"].df,
                prefix=self.account_file.sections["Category"].section,
            ),
            how="left",
            left_on=[("Transaction", "Ca")],
            right_index=True,
            validate="m:1",
        ).drop(columns=[("Transaction", "Ca")])

    def _add_subbudgetary_details(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions.merge(
            type(self).index_column_names(
                df=self.account_file.sections["Sub_budgetary"].df,
                prefix=self.account_file.sections["Sub_budgetary"].section,
            ),
            how="left",
            left_on=[("Transaction", "Bu"), ("Transaction", "Sbu")],
            right_index=True,
            validate="m:1",
        ).drop(columns=[("Transaction", "Sbu")])

    def _add_budgetary_details(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions.merge(
            type(self).index_column_names(
                df=self.account_file.sections["Budgetary"].df,
                prefix=self.account_file.sections["Budgetary"].section,
            ),
            how="left",
            left_on=[("Transaction", "Bu")],
            right_index=True,
            validate="m:1",
        ).drop(columns=[("Transaction", "Bu")])

    def _add_financialyear_details(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions.merge(
            type(self).index_column_names(
                df=self.account_file.sections["Financial_year"].df,
                prefix=self.account_file.sections["Financial_year"].section,
            ),
            how="left",
            left_on=[("Transaction", "Fi")],
            right_index=True,
            validate="m:1",
        ).drop(columns=[("Transaction", "Fi")])

    def _add_reconcile_details(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions.merge(
            type(self).index_column_names(
                df=self.account_file.sections["Reconcile"].df,
                prefix=self.account_file.sections["Reconcile"].section,
            ),
            how="left",
            left_on=[("Transaction", "Re")],
            right_index=True,
            validate="m:1",
        ).drop(columns=[("Transaction", "Re")])

    def _format_transactions_columns(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return self.index_column_names(
            df=self.account_file.sections["Transaction"].df,
            prefix=self.account_file.sections["Transaction"].section,
        )
