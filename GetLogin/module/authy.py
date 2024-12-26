from getpass import getpass

def authy():
    # Prompt user for their username
    username = input("Please enter your username: ")
    # Ask user if they want to fill in the password field
    fill_password = input("Do you want to fill in the password field? (y/n): ")
    
    password = None  # Initialize password as None
    if fill_password.lower() == 'y':
        show_password = input("Do you want to hide the password while typing? (y/n): ")
        if show_password.lower() == 'y':
            password = getpass(prompt="Enter your password: ")
        else:
            password = input("Enter your password: ")
    
    return username, password, fill_password