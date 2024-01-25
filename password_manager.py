import json
from cryptography.fernet import Fernet
import getpass

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.passwords = {}

    def _encrypt(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def _decrypt(self, data):
        return self.cipher_suite.decrypt(data).decode()

    def save_password(self, service, password):
        encrypted_password = self._encrypt(password)
        self.passwords[service] = encrypted_password
        print(f"Password for {service} saved successfully.")

    def get_password(self, service):
        if service in self.passwords:
            decrypted_password = self._decrypt(self.passwords[service])
            print(f"Password for {service}: {decrypted_password}")
        else:
            print(f"No password found for {service}.")

    def delete_password(self, service):
        if service in self.passwords:
            del self.passwords[service]
            print(f"Password for {service} deleted successfully.")
        else:
            print(f"No password found for {service}.")

    def save_to_file(self, filename='passwords.json'):
        data = {'master_password': self.master_password, 'passwords': self.passwords}
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_from_file(self, filename='passwords.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.master_password = data['master_password']
                self.passwords = data['passwords']
        except FileNotFoundError:
            print("No previous data found.")

def main():
    print("Welcome to the Password Manager!")
    master_password = getpass.getpass("Enter your master password: ")
    password_manager = PasswordManager(master_password)

    while True:
        print("\nOptions:")
        print("1. Save Password")
        print("2. Get Password")
        print("3. Delete Password")
        print("4. Save to File")
        print("5. Load from File")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            service = input("Enter the service name: ")
            password = getpass.getpass("Enter the password: ")
            password_manager.save_password(service, password)

        elif choice == '2':
            service = input("Enter the service name: ")
            password_manager.get_password(service)

        elif choice == '3':
            service = input("Enter the service name: ")
            password_manager.delete_password(service)

        elif choice == '4':
            filename = input("Enter the filename to save to (default: passwords.json): ").strip() or 'passwords.json'
            password_manager.save_to_file(filename)

        elif choice == '5':
            filename = input("Enter the filename to load from (default: passwords.json): ").strip() or 'passwords.json'
            password_manager.load_from_file(filename)

        elif choice == '6':
            password_manager.save_to_file()
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
