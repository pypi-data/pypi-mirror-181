__author__ = "Damon May"

import random
import pandas as pd

# Counts of people needed in each NSO role, in descending order of priority
NSO_ROLE_COUNTS_PRIORITY_DESC = {
    "Jam Timer": 1,
    "Penalty Box Timer": 2,
    "Scoreboard Operator": 1,
    "Score Keeper": 2,
    "Penalty Tracker": 1,
    "Penalty Box Manager": 1,
    "Penalty - Lineup Tracker": 2,
    "Lineup Tracker": 2,
    "Penalty Box Minion": 1,
    "Penalty Wrangler": 1,
    "Alternate": 100
}

def assign_game_nso_roles(pdf_nso_signups: str, game_idx: int) -> pd.DataFrame:
    """Assign NSO roles for a single game.

    Args:
        pdf_nso_signups (str): signup dataframe with one row per game.
            Has lists of signed-up officials in column signedup_people 
            and game identifier in Who
        game_idx (int): index of game to assign

    Returns:
        pd.DataFrame: _description_
    """
    game_name = list(pdf_nso_signups.Who)[game_idx]
    signed_up_people = list(pdf_nso_signups.signedup_people)[game_idx]

    signed_up_people = random.sample(signed_up_people, len(signed_up_people))

    roles_assigned = []
    people_assigned = []
    for role in NSO_ROLE_COUNTS_PRIORITY_DESC:
        for _ in range(NSO_ROLE_COUNTS_PRIORITY_DESC[role]):
            if signed_up_people:
                roles_assigned.append(role)
                people_assigned.append(signed_up_people.pop())
            else:
                break

    pdf_role_assignments = pd.DataFrame({
        "game": game_name,
        "role": roles_assigned,
        "person": people_assigned
    })
    return pdf_role_assignments


def assign_nso_roles_all_games(pdf_nso_signups: pd.DataFrame) -> pd.DataFrame:
    """Assign all NSO roles for all games. 

    Args:
        pdf_nso_signups (pd.DataFrame): signup dataframe with one row per game.
            Has lists of signed-up officials in column signedup_people

    Returns:
        pd.DataFrame: Assignments for all games.
    """
    pdf_game_assignment_pdfs = [
        assign_game_nso_roles(pdf_nso_signups, i)
        for i in range(len(pdf_nso_signups))
    ]
    pdf_all_game_assignments = pd.concat(pdf_game_assignment_pdfs)
    return pdf_all_game_assignments
