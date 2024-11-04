import argparse
import filetype
import os
import pandas as pd
import shutil
from file_sorter_classes import *
from file_sorter_constants import *
from pathlib import Path

def handle_options():
    parser = argparse.ArgumentParser(
        description="file_sorter_functions.py that sort files and can creat an output \
            that contains file information"
    )
    parser.add_argument("-p",
                        "--path",
                        required=False,
                        default=os.path.join(os.path.dirname(__file__), "files"),
                        type=str,
                        help="location of files to sort and get information. default is \
                            the files folder in the current location of the script")
    parser.add_argument("-d",
                        "--output_loc",
                        required=False,
                        default=os.path.dirname(__file__),
                        type=str,
                        help="location for output. default is current location of the \
                            script")
    parser.add_argument("-o",
                        "--output",
                        required=False,
                        action="store_false",
                        help="output a text file containing files' information. default \
                            is True")
    parser.add_argument("-e",
                        "--excel",
                        required=False,
                        action="store_false",
                        help="output an excel file containing files' information. \
                            default is True")
    
    args = parser.parse_args()
    option_values = vars(args)

    return option_values

def is_dir_found(path):
    file_path = Path(path)
    if not file_path.is_dir():
        print("Path does not exist.")
        exit(0)
    
    return True

def list_files(path):
    if is_dir_found(path):
        files = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]
    
    if len(files) <= 0:
        print("Path is empty.")
        exit(0)
        
    return files

def copy_file(src_path, dst_path, filename):
    src = os.path.join(src_path, filename)
    dst = os.path.join(dst_path, filename)
    shutil.copy(src, dst)

def sort_files(file_path, output_path, files):
    ft = ""
    ft_objs = {}

    for file in files:
        if filetype.is_image(os.path.join(file_path, file)):
            if IMG not in ft_objs.keys():
                ft_objs[IMG] = ImageType(output_path)
            ft = IMG
        elif file.lower().endswith(".pdf"):
            if PDF not in ft_objs.keys():
                ft_objs[PDF] = PDFType(output_path)
            ft = PDF
        elif file.lower().endswith(".txt"):
            if TXT not in ft_objs.keys():
                ft_objs[TXT] = TXTType(output_path)
            ft = TXT
        else:
            print("File type of " + file + " is out of scope. Skipped.")
        
        copy_file(file_path, ft_objs[ft].output_dir, file)
        ft_objs[ft].df = ft_objs[ft].save_info(file, ft_objs[ft].df, file_path)

    print("Sort complete")
    return ft_objs

def write_output(path, objs):
    report = os.path.join(path, TXT_OUTPUT)

    with open(report, "w") as fp: pass

    for obj in objs.values():
        with open(report, "a") as f:
            df_string = obj.df.to_string(index=False)
            f.write(obj.type + NEWLINE)
            f.write(df_string + NEWLINES)

    print("Output file complete")

def write_excel(path, objs):
    report = os.path.join(path, EXCEL_OUTPUT)
    summary_df = pd.DataFrame()
    file_types = []
    file_count = []

    for obj in objs.values():
        file_types.append(obj.type)
        file_count.append(len(obj.df))
    summary_df[FILE_TYPES] = file_types
    summary_df[COUNT] = file_count

    with pd.ExcelWriter(report) as writer:
        summary_df.to_excel(writer, SUMMARY, index=False)

        for obj in objs.values():
            obj.df.to_excel(writer, obj.type, index=False)
    
    print("Excel file complete")