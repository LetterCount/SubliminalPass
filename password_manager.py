import json
import getpass

class PasswordManager:
    def __init__(self, filename):
        self.filename = filename
        self.master_password = None
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def set_master_password(self):
        while True:
            master_password = getpass.getpass("Enter master password: ")
            confirm_password = getpass.getpass("Confirm master password: ")
            if master_password == confirm_password:
                self.master_password = master_password
                print("Master password set successfully!")
                break
            else:
                print("Passwords do not match. Please try again.")

    def authenticate(self):
        while True:
            master_password = getpass.getpass("Enter master password: ")
            if master_password == self.master_password:
                print("Authentication successful!")
                break
            else:
                print("Incorrect password. Please try again.")

    def add_password(self, website, username, password):
        if website not in self.data:
            self.data[website] = {}
        self.data[website][username] = password
        self.save_data()

    def get_password(self, website, username):
        if website in self.data and username in self.data[website]:
            return self.data[website][username]
        else:
            return None

    def list_websites(self):
        return list(self.data.keys())

# Example usage
if __name__ == "__main__":
    manager = PasswordManager("passwords.json")
    
    # Set master password
    manager.set_master_password()

    # Authenticate
    manager.authenticate()

    while True:
        print("\n1. Add Password")
        print("2. Get Password")
        print("3. List Websites")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            manager.add_password(website, username, password)
            print("Password added successfully!")

        elif choice == "2":
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = manager.get_password(website, username)
            if password:
                print(f"Password for {username} at {website}: {password}")
            else:
                print("Password not found.")

        elif choice == "3":
            websites = manager.list_websites()
            print("Websites:")
            for website in websites:
                print(website)

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
