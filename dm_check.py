from helper_functions import run_loop
import argparse
import pandas as pd

if __name__ == '__main__':
    # get cmd line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("start_length", type=int, choices=range(21),
                        help="lowest number of letters to search for")
    parser.add_argument("-e", "--end_length", type=int, choices=range(21),
                        help="optional, highest number of letters to search for")
    args = parser.parse_args()

    # import word frequencies
    words_df = pd.read_csv("data/unigram_freq.csv")

    # add column for word length
    words_df['length'] = words_df['word'].str.len()

    # remove words 4 letters and fewer - all domains are believed to be taken
    words_df = words_df[words_df['length']>4].reset_index().rename(columns={'index': 'rank'})

    # search only top 50k terms
    words_df = words_df[words_df['rank']<50000]

    # retrieve and export results of given length range
    run_loop(args.start_length, args.end_length, words_df)
else:
    print(f"Run {__name__}.py directly")