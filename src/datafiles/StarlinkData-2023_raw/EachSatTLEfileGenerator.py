import re

def extract_numbers_from_string(string):
    # Define a regex pattern to match numbers
    pattern = r'\d+'

    # Use findall() to extract all numbers from the string
    numbers = re.findall(pattern, string)

    # Convert the numbers from string to integers
    numbers = [int(num) for num in numbers]

    return numbers

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

def save_sat_TLEs_to_file(filename, string_list):
    """
    Save a list of strings to a file in the local directory.

    Parameters:
        filename (str): The name of the file to create.
        string_list (list): A list of strings to save in the file.
    """
    # Open the file in write mode
    with open(filename, 'w') as file:
        # Write each string from the list to the file
        for string in string_list:
            file.write(string)

def extract_tles_for_satellite(file_path, satellite_numbers):
    """
    TBD!!!
    Extract TLEs for a given satellite number from a list of TLEs.

    Parameters:
        tle_list (list): A list of TLEs.
        satellite_numbers (list): The first and the last satellite number whose TLEs are in the file.

    Returns:
        list: A list of TLEs for the specified satellite number.
    """
    # Initialize a list with the given satellite numbers
    satNum = list(range(satellite_numbers[0], satellite_numbers[1] + 1))
    satNum_length = len(satNum)

    lines = txt_file_parse(file_path)
    lines_length = len(lines)

    # Construct the regular expression pattern to match TLEs for the specified satellite number
    # Since sole satellite number is stated in the second line of TLE
    start_ind = [0]
    end_ind = []
    end_ind_val = 0

    for i in range(satNum_length):

        pattern = re.compile(rf'2 {satNum[i]}\s')

        # Iterate through the list of TLEs
        for j in range(start_ind[-1]+1,lines_length,2):
            # Check if the TLE matches the pattern for the specified satellite number
            if pattern.match(lines[j]):
                end_ind_val = j
            else :
                end_ind.append(end_ind_val)
                start_ind.append(end_ind_val+1)
                break

    end_ind.append(lines_length-1)

    # start and end indices of the TLEs for each satellite number obtained

    for i in range(satNum_length):
        filename = f'{str(satNum[i])}.txt'
        save_sat_TLEs_to_file(filename, lines[start_ind[i]:end_ind[i]+1])

    return 0

combined_TLEs_filepath = ("44713-to-44772.txt", "44914-to-44973.txt", "45044-to-45150.txt", "45151-to-45237.txt", "45360-to-45419.txt", "45531-to-45590.txt", "45658-to-45748.txt")

# Split the input file into individual satellite TLE history files
for filepath in combined_TLEs_filepath:
    satelliteNumbers_range = extract_numbers_from_string(filepath)
    extract_tles_for_satellite(filepath, satelliteNumbers_range)

print("Completed Sucessfully")
