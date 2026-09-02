import secrets
import bcrypt
from datetime import datetime, timezone
import json
import copy


max_retries = 3
logged_in = False

default_users = {

"sammy" : {
            "password" : "Hello@123",
            "attempts" : 0,
            "locked" : False,
            "role" : "root",
            "last_login" : None
        }



    }

def view_all_users():
    for key in users:
        print(f"username: {key} | role: {users[key]['role']} | locked: {users[key]['locked']}" )
def view_user_details():
    inspect_user_choice = input("Enter a username to inspect: ")
    if inspect_user_choice in users:
        print (f"username {inspect_user_choice} | role: {users[inspect_user_choice]['role']} | locked: {users[inspect_user_choice]['locked']} | Failed Attempts {users[inspect_user_choice]['attempts']}" )
    else:
        print("User not found")
def lock_unlock_user(current_user):
    target_user_unlock = input("WHich User would you like to unlock or lock: ")
    if target_user_unlock in users:
        print (f"Current account status of {target_user_unlock} is {users[target_user_unlock]['locked']}")
        allowed = False
        if users[current_user]["role"] == "root":
            if users[target_user_unlock]["role"] != "root":
                allowed = True
        elif users[current_user]["role"] == "admin":
            if users[target_user_unlock]["role"] == "user":
                allowed = True

        if allowed == True:
            if users[target_user_unlock]['locked'] == False:
                status_change = input("Do u wanna lock this user y / n : ")
                if status_change == "y":
                    users[target_user_unlock]['locked'] = True
                    save_users(users)
                    print("this user is now officialy locked")
                else:
                    print("aint ***** change bruh")
            else:
                status_change = input("Do you wanna unlock this user y / n :")
                if status_change == "y":
                    users[target_user_unlock]['locked'] = False
                    users[target_user_unlock]['attempts'] = 0
                    save_users(users)
                    print ("This user officially unlocked and attempts are reset now kick rocks")
                else:
                    print("aint ***** change bruh")
        else:
            print("You aint got permission")
    else:
        print("User not FOund")
def password_reset(current_user):
    target_password_reset = input("Sup Fn whos password would you like to change")
    if target_password_reset in users:
        print (f"Current account status of {target_password_reset} is {users[target_password_reset]['locked']}")
        allowed = False
        if users[current_user]["role"] == "root":
            if users[target_password_reset]["role"] != "root":
                allowed = True
        elif users[current_user]["role"] == "admin":
            if users[target_password_reset]['role'] ==  "user":
                allowed = True
        if allowed:
            reset_logic = input("youre about to reset a users password would you like to proceed or nahh y / n: ")
            if reset_logic == "y":
                while True: 
                    admin_passwd_change = input("what would you like to change it too")
                    if validate_password(admin_passwd_change):
                        confirm_admin_passwd_change = input("Nice now plz renter")
                        if confirm_admin_passwd_change == admin_passwd_change:
                            users[target_password_reset]["password"] = password_hash(admin_passwd_change)
                            save_users(users)
                            print("Password is now chnaged")
                            break
                        else:
                            print("passwords do not match, try again")
                    else:
                        print("requiements failed")         
            else:
                print("reset canceled  fn")
        else:
            print("perismison Canceled")
    else:
        print("user not found  fn")
def rename_user(current_user):
    if users[current_user]["role"] == "user":
        target_user_rename = current_user 
        allowed = True
    else: 
        print("heres a list of elgibe users you can change names of")
        for key in users:
            if key == current_user or users[key]["role"] != "root":
                print(key)
        target_user_rename = input("Sup fn whos username would you like to change")
        if target_user_rename in users:
            allowed = False
            if users[current_user]["role"] == "root":
                if users[target_user_rename]["role"] != "root" or target_user_rename == current_user:
                    allowed = True
            elif users[current_user]["role"] == "admin":
                if users[target_user_rename]["role"] == "user"or target_user_rename == current_user :
                    allowed = True
        else:
            print("User not found")
            return current_user
    if allowed:
        rename_change = input("What would you like to rename the user too")
        if rename_change in users:
            print("cant use that bruh choose again")
        else:
            confirm_name = input(f"Confirm name change {rename_change} y / n: ")
            if confirm_name == "y":
                users[rename_change] = users[target_user_rename] 
                del users[target_user_rename]
                save_users(users)
                if target_user_rename == current_user:
                    return rename_change
                else:
                    return current_user
            return current_user
                            
    else:
        print("Permission denied")


    return current_user
def view_locked_users():

    found_locked = False
    for key in users:
        if users[key]["locked"] == True:
            found_locked = True
            print(f"username {key}")
        
    if found_locked == False:
        print("No locked users")
def delete_user():
    delete_target_user = input("Yo fn who you tryna delet: ")
    if delete_target_user in users:
        if users[delete_target_user]["role"] == "root":
            print("My brother in christ u cannot do that")
        else:
            confirm_user_delete = input(f"are you sure you would like to delete{delete_target_user} Y / N: ")
            if confirm_user_delete == "Y":
                del users[delete_target_user]
                save_users(users)
                print(f"user{delete_target_user} is succeffuly gone")
            else:
                print("canceled operation")

    else:
        print("User not found")
def change_user_role():
    print("Here is a list of all users and their assigned roles: ")
    for key in users:
        print(f"username: {key} | role: {users[key]['role']}")
    change_user_target_role = input("Which user would you like to modify: ")
    if change_user_target_role in users:
        if users[change_user_target_role]["role"] != "root":
            print("Here are your allowed roles")
            print("1. User")
            print("2. Admin")
            role_choices = input("Please pick a number fn: ")
            if role_choices != "1" and role_choices != "2":
                    print("try again dummy")
            else:
                if role_choices == "1":
                        new_roles = "user"
                elif role_choices == "2":
                        new_roles = "admin"
                if new_roles == users[change_user_target_role]["role"]:
                        print ("Twin im ngl they already got that role bruh")
                else:
                    confirm_role_change = input(f"twin are you sure you want to change {users[change_user_target_role]['role']} to the role {new_roles}  y / n")
                    if confirm_role_change == "n":
                            print("canceling make up your mind next time fn")
                    elif confirm_role_change == "y":
                            users[change_user_target_role]["role"] = new_roles
                            save_users(users)
        else:
                print("My brother in Christ you CANNOT modify another root user role")
    else:
        print("user not found fn")
def validate_password(password):
    if len(password) < 8:
        return False
    if not any (char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    special_characters = "!@#$%^&*?`~/.,-="
    if not any (char in special_characters for char in password):
        return False
    return True
def password_hash(password):
    user_password_string = password
    bytes_data = bytes(user_password_string, encoding='utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes_data, salt)
    return hashed_password

default_users["sammy"]["password"] = password_hash(default_users["sammy"]["password"])

def verify_password(entered_password, stored_hash):
    byte_data = bytes(entered_password, encoding= 'utf-8')
    return bcrypt.checkpw(
        byte_data,
        stored_hash
    )
def change_own_password(current_user):
    while True:
        self_passwd_chnge = input("Plz enter your new password fn: ")
        if validate_password(self_passwd_chnge):
            renter_confirm = input("Thank you now plz renter to cofirm")
            if renter_confirm == self_passwd_chnge:
                users[current_user]["password"] = password_hash(self_passwd_chnge)
                save_users(users)
                print("Congrats password has been chnaged")
                return True
            else:
                print("password dont match")

        else:
            print("Requierments changed bruh and that new password dosnet fulfill shit ")
def view_account_status(current_user):
    print(f"Account locked: {users[current_user]['locked']}")
    print(f"Failed attempts: {users[current_user]['attempts']}")
    print(f"Last login: {users[current_user]['last_login']}")
def save_users(user_data, file_name="users.json"):
    user_profile_copy = copy.deepcopy(user_data)
    for key in user_profile_copy:
        if isinstance (user_profile_copy[key]["password"], bytes):
            user_profile_copy[key]["password"] = user_profile_copy[key]["password"].decode('utf-8')
    with open(file_name, "w") as json_file_copy:
       json.dump(user_profile_copy, json_file_copy)
def load_users(file_name = "users.json"):
    try:
        with open(file_name, "r") as json_read_copy:
            json_load = json.load(json_read_copy)
            for key in json_load:
                if isinstance(json_load[key]["password"], str):
                    json_load[key]["password"] = json_load[key]["password"].encode('utf-8')
            return json_load
    except FileNotFoundError:
        return default_users
def authenticate_user(users, username, entered_password):
    if username in users:
        if users[username]["locked"] ==  False:
            if verify_password(entered_password, users[username]["password"]):
                users[username]["attempts"] = 0
                users[username]["last_login"] = datetime.now(timezone.utc).isoformat()
                return True
            else:
                users[username]["attempts"] += 1
                if users[username]["attempts"] >= 3:
                    users[username]["locked"] = True
                    return False
                else:
                    return False
        else:
            return False

    else:
        return False





    
users = load_users()
                


    

if __name__ == "__main__":

    print("Welcome to login system fn")

                    
    while True:
        print ("1. Create Account: ")
        print ("2. Login: ")
        print ("3. Quit: ")

        choice = input("Choose an option: ")

        if choice == "1":

            username_new = input("Create a username fn: ")

            if username_new in users:
                print ("thats an invalid name u cant use it")
            else:
                
                print ("thats allowed proceed fn")
                while True:
                    password_new = input("Now create a password fn: ")
                    if validate_password(password_new):
                        users[username_new] = {
                            "password" : password_hash(password_new),
                            "attempts" : 0,
                            "locked" : False,
                            "role" : "user",
                            "last_login" : None
                        }
                        save_users(users)

                        print(f"Account {username_new} created succesfully")
                        break

                    else:
                        print("Password reuqiemrents failed")
                    
                
        elif choice == "2":
            logged_in = False

            iinput = input("Hi plz enter your username to continue: ")
            if iinput in users:

                if users[iinput]["locked"]:
                    print("account locked lil bruh")
                    continue

                while users[iinput]["attempts"] < max_retries:
                    entered_password = input("Awesome now enter your password: ")
                    login_result = authenticate_user(users, iinput, entered_password)
                    save_users(users)
                    if login_result == True:
                        logged_in = True
                        break 


                if logged_in == True:
                
                    if users[iinput]["role"] == "root":
                        print("Welcome Root USer")

                        while True:
                            print("Welcome to ROOT DASHBOARD FN: ")
                            print("1. View All Users: ")
                            print("2. View User Details: ")
                            print("3. Lock / Unlock User: ")
                            print("4. Delete user: ")
                            print("5. Rename User: ")
                            print("6. Change User Role: ")
                            print("7. Reset User Password: ")
                            print("8. Logout: ")

                            root_choice = input("Choose a root option fn: ")

                            if root_choice == "1":
                                view_all_users()
                            elif root_choice == "2":
                                view_user_details()
                            elif root_choice == "3":
                                lock_unlock_user(iinput)
                            elif root_choice == "4":
                                delete_user()
                            elif root_choice == "5":
                                iinput = rename_user(iinput)
                            elif root_choice == "6":
                                change_user_role()
                            elif root_choice == "7":
                                password_reset(iinput)
                            elif root_choice == "8":
                                logged_in = False
                                break

                    elif users[iinput]["role"] == "admin":
                        print("what up admin user")

                        while True:
                            print("Welcome to admin dashboard fn")
                            print("1. View all users:")
                            print("2. Inspect User detials:")
                            print("3. Lock / Unlock regular users: ")
                            print("4. Reset Regular Users Passwords: ")
                            print("5. Rename Regular Users: ")
                            print("6. View Locked accounts")
                            print("7. Logout: ")

                            admin_choice = input("Pick an option fn")

                            if admin_choice == "1":
                                view_all_users()
                            elif admin_choice == "2":
                                view_user_details()
                            elif admin_choice == "3":
                                lock_unlock_user(iinput)
                            elif admin_choice == "4":
                                password_reset(iinput)
                            elif admin_choice == "5":
                                iinput = rename_user(iinput)
                            elif admin_choice == "6":
                                view_locked_users()
                            elif admin_choice == "7":
                                logged_in = False
                                break

                    elif users[iinput]["role"] == "user":
                        print("user acces get your money up")


                        while True:
                            print("Welcome User ")
                            print("1. View my profile: ")
                            print("2. Change my Password: ")
                            print("3. Rename my account: ")
                            print("4. View Login / Account status: ")
                            print("5. Logout: ")


                            user_choice = input("Pick an option fn: ")

                            if user_choice == "1":
                                print(f"Username | {iinput}")
                                print(f"Role | {users[iinput]['role']}")

                            elif user_choice == "2":
                                change_own_password(iinput)

                            elif user_choice == "3":
                                iinput = rename_user(iinput)

                            elif user_choice == "4":
                                view_account_status(iinput)


                            elif user_choice == "5":
                                logged_in = False
                                break
                else:
                    print("Try again bruh")
                    print(max_retries - users[iinput]["attempts"])

                

               
                    

                if logged_in == False and users[iinput]["locked"] == True:
                    print("Your account is locked fn contact an admin bruh")
                    save_users(users)

            else:
                print("Invalid username fn")

        elif choice == "3":
            quitchoice = input("Are u sure you want y/n: ")
            if quitchoice != "n":
                print ("peace lil bruh")
                break