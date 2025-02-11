def validate_name(name):
    #names cannot be greater than 8 characters
    #alphnumeric, spaces, and apostrophes are allowed
    if len(name) > 8:
        return False

    for char in name:
        if not (char.isalnum() or char == " " or char == "'"):
            return False

    return True