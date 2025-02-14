def validate_name(name):
    #names cannot be greater than 8 characters
    #alphnumeric, spaces, and apostrophes are allowed
    if len(name) > 8:
        return False

    for char in name:
        if not (char.isalnum() or char == " " or char == "'"):
            return False

    return True

def validate_port(port):
    if not port.isdigit():
        return False

    port = int(port)
    if port < 1024 or port > 65535:
        return False

    return True

def validate_address(address):
    if address.count(".") != 3:
        return False

    parts = address.split(".")
    for part in parts:
        if not part.isdigit():
            return False

        part = int(part)
        if part < 0 or part > 255:
            return False

    return True