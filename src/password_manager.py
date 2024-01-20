from cryptography.fernet import Fernet

class PasswordManager:
    
    #Basic constructor
    def __init__(self):
        self.key = None # By default, no key for encryption or decryption
        self.password_file = None # No password file specified
        self.password_dict = {} # Empty dictionary for passwords
        
    # Need a key to encrypt/decrypt whatever we to open
    def create_key(self, path):
        self.key = Fernet.generate_key() 
        # store key into file -> 'wb' = writing bytes
        with open(path, 'wb') as f:
            f.write(self.key)
        # print(self.key)
    
    # decrypt the with existing key
    def load_key(self, path):
        # 'rb' = reading bytes
        with open(path, 'rb') as f:
            self.key = f.read()
    
    # initial values = none at the beginning; can pass dictionary with key value pairs
    def create_password_file(self, path, initial_values = None):
        self.password_file = path
        
        if initial_values is not None: 
            for key, value in initial_values.items():
                self.add_password(key,value)
    
    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(",")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
    
    def add_password(self, site, password):
        self.password_dict[site] = password
        if self.password_file is not None:
            # appending mode, because 'w' -> writing mode overwrites
            with open(self.password_file, 'a+') as f:
                encrypted = Ferent(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")
    
    def get_password(self, site):
        return self.password_dict[site]
    
    
    pm = PasswordManager()
    pm.create_key("mykey.key")
    
    def main():
        print("bug")
        password = {
            "email": "test email",
            "facebook": "test",
            "youtube": "testing channel",
            "instagram": "test"
        }
        
        pm = PasswordManager()
        
        print("""What do you want to do?
              1) Create new key
              2) Load existing key
              3) Create new password file
              4) Load exisiting password file
              5) Add a new password
              6) Get a password
              q) Quit""")
        
        done = False
        
        while not done:
            choice = input("Enter your choice: ")
            if choice == "1":
                path = input("Enter path: ")
                pm.create_key(path)
            elif choice == "2":
                path = input("Enter path: ")
                pm.load_key(path)
            elif choice == "3":
                path = input("Enter path: ")
                pm.create_password_file(path, password)
            elif choice == "4":
                path = input ("Enter path: ")
                pm.load_password_file(path)
            elif choice == "5":
                site = input("Enter the site: ")
                password = input("Enter the password: ")
                pm.add_password(site, password)
            elif choice == "6":
                site = input("What site do you want: ")
                print(f"Password for {site} is {pm.get_password(site)}")
            elif choice == "q":
                done = True
                print("done")
            else: 
                print("Invalid choice")

    if __name__ == "__main__":
        print("bug2")
        main()
