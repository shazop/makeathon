
def print_in_lines_of_10(text):
    for i in range(0, len(text), 10):
        print(text[i:i+10])

# Example usage
your_string = '''"><iframe/src='http://rush-hour.ctf.umasscybersec.org/user/fefc3785-e0cb-4d5d-8d0c-d44470e3f536-admin"'''
print_in_lines_of_10(your_string)
