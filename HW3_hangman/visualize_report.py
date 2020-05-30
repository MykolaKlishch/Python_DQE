import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind


def enter_and_validate_filename():
    """Gets filename from user input and verifies it.
    Both absolute and relative file names are accepted
    If no input is provided, default filename is used.
    """
    inp_msg = "Enter the name of csv report: "
    while True:
        file_name = input(inp_msg)
        if not file_name:
            file_name = "report_2020-05-30_21-51-11.048004.csv"
        if not os.path.isfile(file_name):
            inp_msg = "Couldn't find such file.\n" \
                      "Please, try again: "
            continue
        return file_name


if __name__ == "__main__":
    filename = enter_and_validate_filename()
    df = pd.read_csv(filename, encoding="utf-8", index_col="word")
    df_avgs = df.mean(axis=0)
    print(df_avgs)
    print(ttest_ind(df["by_word_count_total"],
                    df["by_letter_count_total"]))
    df.plot(kind="box")
    plt.title("Compare the number of attempts")
    plt.ylabel("Number of attempts to guess a letter")
    plt.show()
