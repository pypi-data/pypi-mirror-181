from officialator.io.xlsxio import load_xlsx_worksheet
import pandas as pd

def load_nso_or_so_signups(workbook_path: str, worksheet_name: str,
                           so_or_nso: str) -> pd.DataFrame:
    """Load either the NSO or SO signups from worksheet worksheet_name
    in workbook workbook_path.

    Args:
        workbook_path (str): XLSX path
        worksheet_name (str): worksheet to load
        so_or_nso (str): SO or NSO

    Returns:
        pd.DataFrame: _description_
    """
    assert(so_or_nso in ["NSO", "SO"])

    pdf_signup_worksheet = load_xlsx_worksheet(workbook_path, worksheet_name)
    pdf_allgame_signups = pd.DataFrame(pdf_signup_worksheet.values[1:,:],
                                    columns=pdf_signup_worksheet.values[0, :])
    pdf_allgame_signups = pdf_allgame_signups[pdf_allgame_signups.Day == "Sunday"]
    pdf_result = pdf_allgame_signups[["Day", "Time", "Mins", "Scrim Structure",
                                           "What", "Who"]].copy()  
    
    pdf_allgame_officials = pdf_allgame_signups[so_or_nso]
    allgame_signedup_people = []
    for i, vals in pdf_allgame_officials.iterrows():
        signedup_people = sorted([x for x in set(vals) if x is not None])
        allgame_signedup_people.append(signedup_people)
    pdf_result["signedup_people"] = allgame_signedup_people
    
    return pdf_result