from file_sorter_constants import OUTPUT_FOLDER
from file_sorter_functions import *

def main():
    # handle parameters
    option_values = handle_options()
    file_location = option_values["path"]
    output_loc = option_values["output_loc"]
    output = option_values["output"]
    excel = option_values["excel"]

    files = list_files(file_location)

    output_location = os.path.join(output_loc, OUTPUT_FOLDER)
    
    ft_objs = sort_files(file_location, output_location, files)
    
    if output and ft_objs:
        write_output(output_location, ft_objs)

    if excel and ft_objs:
        write_excel(output_location, ft_objs)

    print("Output complete. See " + output_location)


if __name__ == "__main__":
    main()