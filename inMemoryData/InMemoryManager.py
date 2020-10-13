import logging
from dataclasses import dataclass
from datetime import datetime
from os import path

import pandas as pdb

import definitions
from utils.print_enh import print_begin

who_pd: pdb.DataFrame = pdb.DataFrame()
current_logger = definitions.setup_logger(__name__, level=logging.DEBUG)


@dataclass
class ActivityNote:
    """Note"""
    Mbr_Id: str
    Date_Time: str
    Case_Id: str
    Activity_Type: str
    Note: str
    Author: str


excel_columns = ['Mbr_Id', 'Date_Time', 'Case_Id', 'Activity_Type', 'Note']


class InMemoryManager:

    @staticmethod
    def dataframes_load(author: str) -> None:
        global who_pd
        logtest = 'dataframes_load method'
        print_begin(f'Enter {logtest}')
        current_logger.info(f'Entered {logtest}')

        if path.exists(f'inputs/{author}-Activity-Note.xlsx'):
            who_pd = pdb.read_excel(f'inputs/{author}-Activity-Note.xlsx', index_col=None,
                                    names=['Mbr_Id', 'Date_Time', 'Case_Id', 'Activity_Type', 'Note'], header=None,
                                    dtype=str, keep_default_na=False)
        else:
            who_pd = pdb.read_excel(f'inputs/Authors-Activity-Note-Template.xlsx', index_col=None,
                                    names=['Mbr_Id', 'Date_Time', 'Case_Id', 'Activity_Type', 'Note'], header=None,
                                    dtype=str, keep_default_na=False)

        if who_pd.empty:
            current_logger.info(f'Failed to load Excel to PDF in {logtest}')
            # return False
        print_begin(f'Exiting {logtest}')

    def dataframes_search(self, speech_text: str) -> str:
        logtest = f'dataframes_search method with - :{speech_text}'
        print_begin(f'Enter {logtest}')
        current_logger.info(f'Entered {logtest}')
        result = speech_text.split(" ")
        words = '|'.join(result)
        # 'Mbr_Id', 'Date_Time', 'Case_Id', 'Activity_Type', 'Note'
        s = who_pd['Mbr_Id'] + who_pd['Date_Time'] + who_pd['Case_Id'] + who_pd['Activity_Type'] + who_pd['Note']
        who_results = who_pd[s.str.contains(words, case=False, regex=True)]
        print_begin(f'Exiting {logtest}')
        return who_results.to_json()

    def workbook_add(self, activity_note: ActivityNote) -> bool:
        logtest = f'workbook_add method with - :{activity_note.Activity_Type}'
        print_begin(f'Enter {logtest}')
        current_logger.info(f'Entered {logtest}')

        if not path.exists(f'inputs/{activity_note.Author}-Activity-Note.xlsx'):
            df = pdb.read_excel(f'inputs/Authors-Activity-Note-Template.xlsx', index_col=None, names=excel_columns,
                                dtype=str, keep_default_na=False)
            df.to_excel(f'inputs/{activity_note.Author}-Activity-Note.xlsx')

        df = pdb.read_excel(f'inputs/{activity_note.Author}-Activity-Note.xlsx', index_col=None, names=excel_columns,
                            header=None, dtype=str, keep_default_na=False)
        # print(activity_note.__dict__)

        new_df = df.append(activity_note.__dict__, ignore_index=True)
        # print(new_df)
        new_df.to_excel(f'inputs/{activity_note.Author}-Activity-Note.xlsx')

        return True
