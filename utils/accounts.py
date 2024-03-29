import json

def loadDB():
    with open("db.json", "r") as f:
        return json.load(f)

def saveDB(info):
    with open("db.json", "w") as f:
        json.dump(info, f)

def addAcc(service, username, password, tags=[], subs=[]):
    accs = loadDB()
    accs[service].append({
        "username": username,
        "password": password,
        "tags": tags,
        "subs": subs,
        "doneVids": [],
        "enabled": "False"
    })
    saveDB(accs)

    print("Account added!")

def deleteAcc(service, username):
    accs = loadDB()
    for acc in accs[service]:
        if acc["username"] == username:
            accs[service].remove(acc)
            break

    saveDB(accs)

    print("Account deleted!")

def enableAcc(service, username):
    accs = loadDB()
    for acc in accs[service]:
        if acc["username"] == username:
            acc["enabled"] = "True"
            break

    saveDB(accs)

    print("Account enabled!")

def disableAcc(service, username):
    accs = loadDB()
    for acc in accs[service]:
        if acc["username"] == username:
            acc["enabled"] = "False"
            break

    saveDB(accs)

    print("Account disabled!")

def editTags(service, username, newTags):
    accs = loadDB()
    for acc in accs[service]:
        if acc["username"] == username:
            acc["tags"] = newTags
            break

    saveDB(accs)

    print("Tags edited!")

def editSubs(service, username, newSubs):
    accs = loadDB()
    for acc in accs[service]:
        if acc["username"] == username:
            acc["subs"] = newSubs
            break

    saveDB(accs)

    print("Subs edited!")