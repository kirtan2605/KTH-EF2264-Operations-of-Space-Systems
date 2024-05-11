def get_dimensions(lst):
    # Check if the list is empty
    if not lst:
        return 0, 0

    # Get the number of rows (length of the outer list)
    num_rows = len(lst)

    # Get the number of columns (length of the first inner list, assuming all inner lists have the same length)
    num_columns = len(lst[0])

    return num_rows, num_columns
