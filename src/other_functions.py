def get_dimensions(lst):
    # Check if the list is empty
    if not lst:
        return 0, 0

    # Get the number of rows (length of the outer list)
    num_rows = len(lst)

    # Get the number of columns (length of the first inner list, assuming all inner lists have the same length)
    num_columns = len(lst[0])

    return num_rows, num_columns

def txt_file_parse(file_path):
    try:
        # Open the file for reading
        with open(file_path, 'r') as file:
            # Read all lines from the file and store them as strings in a list
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None
