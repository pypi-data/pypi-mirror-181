# type: ignore

# Damon's utilities for working with XLSX files.

from io import BytesIO

import pandas as pd
from openpyxl import load_workbook
from openpyxl.workbook import Workbook


def load_xlsx_workbook(filepath: str) -> Workbook:
    """
    Load an XLSX workbook from a blob
    """
    return load_workbook(filename=filepath, data_only=True, read_only=True)


def retrieve_xlsx_worksheet(xlsx_workbook: Workbook,
                            sheet_name: str) -> pd.DataFrame:
    """
    Get an XLSX worksheet from an XLSX workbook, by name.
    """
    if sheet_name not in xlsx_workbook:
        raise ValueError(
            f"No sheet named {sheet_name} in workbook."
            + f"Sheets: {[x.title for x in xlsx_workbook.worksheets]}"
        )
    worksheet = xlsx_workbook[sheet_name]

    pdf_worksheet = pd.DataFrame(worksheet.values)
    new_header = pdf_worksheet.iloc[0]
    pdf_worksheet = pdf_worksheet[1:]
    pdf_worksheet.columns = new_header
    return pdf_worksheet


def load_xlsx_worksheet(filepath: str, sheet_name: str) -> pd.DataFrame:
    """
    Load a specific worksheet from a file
    """
    return retrieve_xlsx_worksheet(load_xlsx_workbook(filepath), sheet_name)
