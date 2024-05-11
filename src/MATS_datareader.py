def MATS_TLEs_txt_file_parse(file_path):
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
