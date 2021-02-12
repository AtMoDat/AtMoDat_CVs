import pandas as pd
import os
import argparse
import shutil


def comand_line_parse():
    """Parser for command line options""" 
    parser = argparse.ArgumentParser(description="Create CV files from check database.")
    parser.add_argument("-c", "--check", help="Specify the name of the chck for which the CV are supposed to be created.", default="all")
    parser.add_argument("-f", "--file", help="Processes the given file")
    return parser.parse_args()


def read_database(file_name, check_name):
    """Read database file
    input: name of the database file and name of the relevant checks
    ouput: pandas dataframe where columns checker = check_name and CV != NA
    """
    df = pd.read_csv(file_name)
    df_CVs = df[df.CV.notna()]
    if check_name == "data_file":
        df_CVs = df_CVs.loc[df_CVs["checker"] == "data_file"]
    elif check_name == "datacite":
        df_CVs = df_CVs.loc[df_CVs["checker"] == "datacite"]
    return df_CVs


def create_CV_directory(check_name):
    """create directory to store CV files"""
    current_path = os.getcwd()
    if check_name != "all":
        new_path = os.path.join(current_path,"CVs_" + check_name)
        # remove directory if it already exists
        if os.path.exists(new_path):
            shutil.rmtree(new_path)
        try:
            os.mkdir(new_path)
        except OSError:
            print ("Creation of the directory %s failed" % new_path)
        else:
            print ("Successfully created the directory %s " % new_path)


def create_CV_files():
    


def main():
    args = comand_line_parse()
    check_overview = read_database(args.file, args.check)
    create_CV_directory(args.check)
    

    


if __name__ == '__main__':
    main()
