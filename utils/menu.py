from utils.accounts import addAcc, deleteAcc, enableAcc, disableAcc, editTags, editSubs, loadDB
from utils.cleaning import clearTerminal

def logo():
    print("""
 _______   ________  _______   _______   ______  ________         ______          ______    ______   __    __  ________  ________  __    __  ________ 
/       \ /        |/       \ /       \ /      |/        |       /      \        /      \  /      \ /  \  /  |/        |/        |/  \  /  |/        |
|$$$$$$$  |$$$$$$$$/ $$$$$$$  |$$$$$$$  |$$$$$$/ $$$$$$$$/       /$$$$$$  |      /$$$$$$  |/$$$$$$  |$$  \ $$ |$$$$$$$$/ $$$$$$$$/ $$  \ $$ |$$$$$$$$/ 
|$$ |__$$ |$$ |__    $$ |  $$ |$$ |  $$ |  $$ |     $$ |         $$____$$ |      $$ |  $$/ $$ |  $$ |$$$  \$$ |   $$ |   $$ |__    $$$  \$$ |   $$ |   
|$$    $$< $$    |   $$ |  $$ |$$ |  $$ |  $$ |     $$ |          /    $$/       $$ |      $$ |  $$ |$$$$  $$ |   $$ |   $$    |   $$$$  $$ |   $$ |   
|$$$$$$$  |$$$$$/    $$ |  $$ |$$ |  $$ |  $$ |     $$ |         /$$$$$$/        $$ |   __ $$ |  $$ |$$ $$ $$ |   $$ |   $$$$$/    $$ $$ $$ |   $$ |   
|$$ |  $$ |$$ |_____ $$ |__$$ |$$ |__$$ | _$$ |_    $$ |         $$ |_____       $$ \__/  |$$ \__$$ |$$ |$$$$ |   $$ |   $$ |_____ $$ |$$$$ |   $$ |   
|$$ |  $$ |$$       |$$    $$/ $$    $$/ / $$   |   $$ |         $$       |      $$    $$/ $$    $$/ $$ | $$$ |   $$ |   $$       |$$ | $$$ |   $$ |   
|$$/   $$/ $$$$$$$$/ $$$$$$$/  $$$$$$$/  $$$$$$/    $$/          $$$$$$$$/        $$$$$$/   $$$$$$/  $$/   $$/    $$/    $$$$$$$$/ $$/   $$/    $$/    


                   """)

def serviceSelector():
    clearTerminal()
    logo()
    service = input("""Choose a service:
    
[1] Instagram
[2] YouTUbe
[3] Tiktok
[4] Make Video Only

[!] > """)
    if service == "1":
        return "instagram"
    elif service == "2":
        return "youtube"
    elif service == "3":
        return "tiktok"
    elif service == "4":
        return "makevideo"

def menu():
    clearTerminal()
    logo()
    a = input("""                                                                                                                                   
                                                                                                                                                      
[1] Run
[2] List accounts
[3] Manage accounts
[4] Exit

[!] > """)
    if a == "1":
        return

    if a == "2":
        printAccounts()

    elif a == "3":
        accountManager()

def printAccounts():
    clearTerminal()
    logo()
    accs = loadDB()
    for service in accs:
        print(f"""===============================================================
=                                                             =
=                                                             =
                           {service}                           
=                                                             =
=                                                             =
===============================================================""")
        print("| Enabled ")
        for acc in accs[service]:
            if acc["enabled"] == "True":
                print(f"|-- {acc['username']} -- {acc['subs']} -- {acc['tags']}")
        print("===============================================================")
        print("| Disabled ")
        for acc in accs[service]:
            if acc["enabled"] == "False":
                print(f"|-- {acc['username']} -- {acc['subs']} -- {acc['tags']}")
        
    input("\n\n\nPress ENTER to return to the main menu.")
    menu()

def accountManager():
    clearTerminal()
    logo()
    a = input("""[1] Add account
[2] Delete account
[3] Enable account
[4] Disable account
[5] Edit tags
[6] Edit subs
[7] Back

[!] > """)

    if a == "1":
        service = serviceSelector()
        username = input("Username: ")
        password = input("Password: ")
        tags = input("Tags (separated by spaces): ")
        tags = tags.split(" ")
        addAcc(service, username, password, tags)

    elif a == "2":
        service = serviceSelector()
        username = input("Username: ")
        deleteAcc(service, username)

    elif a == "3":
        service = serviceSelector()
        username = input("Username: ")
        enableAcc(service, username)

    elif a == "4":
        service = serviceSelector()
        username = input("Username: ")
        disableAcc(service, username)
    
    elif a == "5":
        service = serviceSelector()
        username = input("Username: ")
        tags = input("Tags (separated by spaces): ")
        tags = tags.split(" ")
        editTags(service, username, tags)

    elif a == "6":
        service = serviceSelector()
        username = input("Username: ")
        subs = input("Subs (separated by spaces): ")
        subs = subs.split(" ")
        editSubs(service, username, subs)

    input("\n\n\nPress ENTER to return to the main menu.")
    menu()