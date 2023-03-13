from getpass import getpass

def authy():
    # prompt user for their username
    username = input("Please enter your username: ")
    # Ask user if they want to fill in the password field
    fill_password = input("Do you want to fill in the password field? (y/n): ")
    if fill_password.lower() == 'y':
        show_password = input("Do you want to hide the password while type? (y/n): ")
        if show_password.lower() == 'y':
            password = getpass(prompt="Enter your password: ")
        else:
            password = input("Enter your password: ")
            
    return username,password,fill_password