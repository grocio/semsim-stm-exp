"""
For analysis purposes, you don't have to run this srcipt as this script is a part of preprocessing.

This script integrates csv files for each participant into one large csv file of all participants' data.
It also deletes personal information, a form of anonymization but reports overall demogratic information (age and gender).
Note that I do not report csv files for each participant to protect participants' privacy. Instead, I report a integrated csv file of anonymized data.
Thus, you don't have to use this script!
"""

BEHAV_DATA = False
DEMOG_DATA = True #Reports demographic data?

import pandas as pd
import glob
import pandas as pd
import statistics as stat
from decimal import Decimal, ROUND_HALF_UP

def correct_round(float_n, digit_n='0.01'):
    """
    Use round half up as a conventional rounding
    """
    return Decimal(float_n).quantize(Decimal(digit_n), rounding=ROUND_HALF_UP)

def responseErrorsChecker(df_path):
    """
    Check whether a participant understood instructions
    Specifically, it checks whether a participants answered a fixation cross as a response more than 4 times

    Some participants typed fixation crosses or "+" as responses
    If particpants responded "+" more than 4 times, we judged that they did not understand instructions as we intended
    Data for these particiapnts were excluded

    Parameters
    ----------
    df_path: str
        path for a csv file of a participant's memory performance data

    Returns
    -------
    bool (True or False)
        Whether participant's responses of "+" > 4 times
    """

    df = pd.read_csv(df_path)
    df = df.query('test_part == "main_response"')
    if sum(["+" in str(s) for s in df['responses']]) > 4:
        print('File {} includes more than 4 "+"s as responses'.format(df_path))
        return True
    else:
        return False

def forSingleCSV(df_path):
    """
    It takes raw data for a participant's memory performance and calculates correct_in_position and item correct scorings
    It also specifies words position information (position 0 - position 5)

    Parameters
    ----------
    df_path: str
        path for a csv file of a participant's memory performance data

    Returns
    -------
    results_df: pandas.DataFrame
        Participant's memory perforamnce scored by correct-in-position and item correct
        It also contains word's position data (ranging from position 0 to position 5)
    """

    df = pd.read_csv(df_path)
    stimulus_df = df.query('test_part == "main_stimulus"')[['stimulus', 'listID']]
    response_df = df.query('test_part == "main_response"')[['responses', 'listID']]

    # stimulus was presented like <p style="font-size: 48px;">STIMULUS</p>
    # response was recorded like {"Q0":"RESPONSE"}
    # we got to get rid of irrelevant parts of strings
    stimulus_df['stimulus'] = [s.replace('<p style="font-size: 48px;">', '').replace('</p>', '') for s in stimulus_df['stimulus']]
    response_df['responses']  = [s.replace('{"Q0":"', '').replace('"}', '').lower() for s in response_df['responses']]

    # Check the number of targeted responses or stimuli (150 = 25 main trials * 6 words)
    if (len(stimulus_df['stimulus']) != 150) or (len(response_df['responses']) != 150):
        print('WARNING: Response length is invalid\nCheck on the file {}'.format(df_path))

    # Check whether each trial has 6 words
    for current_listID in set(stimulus_df['listID']):
        if len([str(s) for s in stimulus_df.query('listID == @current_listID')['stimulus']]) != 6:
            print('WARNING: Length of within list position is not 6\nCheck on the file {}'.format(df_path))

    stimulus_df = stimulus_df.reset_index(drop=True)
    response_df = response_df.reset_index(drop=True)

    # Below two scoring methos, Correct-in-position and Item correct, are used
    # Note that Order errors can be calculated as
    #   Order errors = Item correct - Correct-in-position

    # Scoring 1: Correct-in-position
    correct_in_position = stimulus_df['stimulus'] == response_df['responses']

    # Scoring 2: Item correct
    item_correct = []
    for word_i in range(len(stimulus_df)):
        current_listID = stimulus_df['listID'][word_i]
        if str(response_df['responses'][word_i]) in [str(s) for s in stimulus_df.query('listID == @current_listID')['stimulus']]:
            item_correct.append(1)
        else:
            item_correct.append(0)

    # Add within-list position information (from 0 to 5) to each row
    position = []
    previous_listID = None
    for word_i in range(len(stimulus_df)):
        current_listID = int(stimulus_df['listID'][word_i])
        # When lists change
        if current_listID != previous_listID:
            position_i = 0
            previous_listID = current_listID
        # If a word's listID == the previous word's listID
        elif current_listID == previous_listID:
            position_i += 1
        position.append(position_i)

    results_df = pd.DataFrame({
                'listID': [int(listID_one) for listID_one in stimulus_df['listID']],
                'stimulus': stimulus_df['stimulus'],
                'response': response_df['responses'],
                'correct_in_position': correct_in_position,
                'item_correct': item_correct,
                'position':position})

    results_df = results_df.astype({'correct_in_position': int})

    return results_df

all_files = glob.glob('../DataFromServer/*')
all_files = [file_name for file_name in all_files if not 'data_pilot' in file_name]
all_files = [file_name for file_name in all_files if file_name.endswith('.csv')]

# Drop data in which particiapnts reported "+" as responses more than 4 times
all_files = [file_name for file_name in all_files if not responseErrorsChecker(file_name)]

all_files.sort()

# Report overall memory performance data (behavioral data)
if BEHAV_DATA:
    for file_index in range(len(all_files)):
        print('File index: {} File name: {}'.format(file_index, all_files[file_index]))
        current_df = forSingleCSV(all_files[file_index])
        current_df = current_df.reset_index(drop=True)
        subjectID = pd.Series([file_index for i in range(len(current_df))])
        subjectID.name = 'subjectID'

        if file_index == 0:
            all_results_df = pd.concat([subjectID, current_df], axis=1)
        else:
            one_results_df = pd.concat([subjectID, current_df], axis=1)
            one_resulst_df = one_results_df.reset_index(drop=True)
            all_results_df = all_results_df.reset_index(drop=True)
            all_results_df = pd.concat([all_results_df, one_results_df], axis=0)

    all_results_df = all_results_df.reset_index(drop=True)
    all_results_df.to_csv('../Data/behav_data.csv')

# Report demographic data
if DEMOG_DATA:
    age_li = []
    gender_li = []
    for file_path in all_files:
        df = pd.read_csv(file_path)

        age = int(df.query('test_part == "age"')['responses'].values[0].replace('{"age":"', '').replace('"}', ''))
        gender = df.query('test_part == "gender"')['responses'].values[0].replace('{"Q0":"', '').replace('"}', '')

        age_li.append(age)
        gender_li.append(gender)

    rounded_mean_age = correct_round(stat.mean(age_li))
    rounded_sd_age = correct_round(stat.stdev(age_li))

    print('Age Mean: {}\nAge SD: {}'.format(rounded_mean_age, rounded_sd_age))

    for gender_category in set(gender_li):
        print('Gender Category: {} Count: {}'.format(gender_category, gender_li.count(gender_category)))
