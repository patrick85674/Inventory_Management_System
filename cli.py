from menu.cli_user import user_menu  # Importiere die user_menu Funktion

IS_CLI = True  # Indicate that the program is running through CLI

def main():
    """
    Starts the program and shows the main menu.
    """
    print("Welcome to the system!")
    
    # Hier wird das Benutzer-Menü aufgerufen
    user_menu()  # Aufruf der Funktion user_menu aus menu/user.py

if __name__ == "__main__":
    main()