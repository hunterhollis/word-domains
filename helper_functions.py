import whois
import validators
import pandas as pd
from tqdm import tqdm

# basic lookup of domain
def dm_lookup(dm):
    if validators.domain(dm):
        try:
            dm_info = whois.whois(dm)
            return dm_info
        except Exception as e:
            e_text = e.__str__().lower()
            if e_text.startswith('no match for'):
                return f"{dm} is not registered"
            elif e_text.startswith('domain not found'):
                return "Unavailable TLD"
            else:
                return "Other exception"
    else:
        return "Invalid domain format"
    
# return flag based on registered, unregistered, or invalid
def dm_flag(dm):
    dm_info = dm_lookup(dm)
    if type(dm_info) == whois.parser.WhoisCom:
        return 1
    elif dm_info == f"{dm} is not registered":
        return 0
    elif dm_info == "Unavailable TLD":
        return -1
    elif dm_info == "Other exception":
        return -2
    elif dm_info == "Invalid domain format":
        return -3

# create list of flags for all words in given df
def flag_loop(word_df, word_length):
    word_list = list(word_df['word'])
    dm_list = [i+".com" for i in word_list]
    flag_list = []

    for i in tqdm(range(len(dm_list)), desc=f"{word_length}-letter words"):
        flag = dm_flag(dm_list[i])
        flag_list.append(flag)

    return flag_list

# run process with given length of words to search
def run_loop(start_length, end_length, words_df):
    words_df['adj_length'] = words_df['length'].clip(None, 20)

    # allow nullable cmd argument to mean searching for 1 length
    # if an end_length is not specified, end_length defaults to None
    if end_length==None:
        end_length = start_length
    elif end_length < start_length:
        start_arg = start_length
        end_arg = end_length
        end_length = start_arg
        start_length = end_arg

    for word_length in range(start_length, end_length+1):
        df = words_df[words_df['adj_length']==word_length].copy()
        df['reserved'] = flag_loop(df, word_length)
        df.to_csv(f"results/dm_results_{word_length}_letters.csv")