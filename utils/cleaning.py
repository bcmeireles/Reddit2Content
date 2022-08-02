import shutil

def cleanup():
    shutil.rmtree("temp")

def clearTerminal():
    print("\n" * 100)