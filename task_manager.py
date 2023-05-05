# ======== Importing libraries ========
from datetime import datetime
from os.path import exists

# ======== Login Section ========

username_list = []
password_list = []
user_count = 0

# Open and read the user.txt file to interpret the login info.
login_data = open('user.txt', 'r+') 
for line in login_data:
     # We turn each line / string into a list of words, and extract the 1st
     # word as the username, the 2nd word as the password. 
     # 
     # Thread each together into 2 seperate lists - username and password.
     username_list.append(line.split(', ')[0])
     password_list.append(line.split(', ')[1])
     user_count += 1

print("***** PLEASE LOG IN *****")
name = input("Enter your username: ")
password = input("Enter your password: ")

# Checks to see if the input username & password combinaton is valid
check1 = False    # check1 is if the username is valid
check2 = False    # check2 is given the username is valid, if the password is valid

while (check1 == False) or (check2 == False):
    check1 = (name in username_list)
    if check1 == True:                    # only if the username is valid, do we check the password
        i = username_list.index(name)     # find index/location of the valid username in our list
        check2 = (password in password_list[i])
        if check2 == True:
            print("***** YOU ARE LOGGED IN *****")
            break
    # Unless the username & password combination are both valid, then
    # keep prompting for user to enter in new combination.
    print("***** INVALID LOGIN CREDENTIALS, PLEASE RE-ENTER *****")
    name = input("Enter your username: ")
    password = input("Enter your password: ")

# ======== Defining Functions ========
# ======== MENU: r - Registering a user ========
def reg_user(name):
    # Allow only if user is admin.
    if name == 'admin':
        # Request input of a new username, password and password confirmation.
        reconfirm_password = ""
        new_name = input("Enter username for new user: ")
        # If entered name already exists, keep prompting for another name.
        while new_name in username_list:
            print("***** USERNAME ALREADY IN USE. PLEASE ENTER ANOTHER USERNAME *****")
            new_name = input("Enter username for new user: ")
        new_password = input("Enter password for new user: ")
        # If new password and reconfirmed password does not match, ask again until they match. 
        while reconfirm_password != new_password:
            print("***** PASSWORDS DO NOT MATCH *****")
            reconfirm_password = input("Reconfirm password for new user: ")
        # If the new password and reconfirmed password are the same, add them to the user.txt file. 
        login_data.write(f"\n{new_name}, {new_password}")
        print("***** USER SUCCESSFULLY REGISTERED *****")
    else:
        print("***** USERS CAN ONLY BE REGISTERED BY ADMIN *****")

# ======== MENU: a - Adding a task ========
def add_task():
    # Prompt user to enter in all new task information.
    task_user = input("Enter the username of the person whom the task is assigned to: ")
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the description of the task (no commas please): ").replace(",", "")
    task_due = input("Enter the due date of the task (dd mmm yyyy): ")
    today = datetime.today().strftime("%d %b %Y")
    task_completion = "No"
    # Add all new task data to task.txt file. 
    all_tasks = open('tasks.txt', 'a+')
    all_tasks.write(f"\n{task_user}, {task_title}, {task_description}, {task_due}, {today}, {task_completion}")
    all_tasks.close()
    print("***** TASK SUCCESSFULLY ADDED *****")

# ======== MENU: va - View all tasks ========
def view_all():
    print("***** HERE ARE ALL OF THE TASKS *****")
    # Read line by line (task by task) from the tasks.txt file. 
    # Split 1 line/task into a list of it's indivdual pieces of information, 
    # and reformat into a more friendly format. 
    all_tasks = open('tasks.txt', 'r')
    for task in all_tasks:
        task_info_list = task.split(", ")     
        print(f'''
            -----------------------------------------------------
            Task Title:          {task_info_list[1]}
            Assigned to:         {task_info_list[0]}
            Date assigned:       {task_info_list[3]}
            Due date:            {task_info_list[4]}
            Task complete?       {task_info_list[5]}
            Task description: 
                {task_info_list[2]}
            -----------------------------------------------------
            ''')
    all_tasks.close()

# ======== MENU: vm - View my tasks ========
def view_mine():
    print(f"***** HERE ARE THE TASKS FOR USER {name} *****")
    all_tasks = open('tasks.txt', 'r+')
    count = 0
    task_list = []
    for task in all_tasks:
        task_info_list = task.split(", ")
        task_list.append(task)
        count += 1    # Counter to track the task number 
        # Same as va, except we show only the tasks relevant to current user   
        if name == task_info_list[0]: 
            print(f'''
            -----------------------------------------------------
            TASK {count}
            -----------------------------------------------------
            Task Title:          {task_info_list[1]}
            Assigned to:         {task_info_list[0]}
            Date assigned:       {task_info_list[3]}
            Due date:            {task_info_list[4]}
            Task complete?       {task_info_list[5]}
            Task description: 
                {task_info_list[2]}
            -----------------------------------------------------
            ''')
    all_tasks.close()

    while True:
        # Allow user to access specific task, by referencing the task number
        # Subtract one to align with zero indexing
        task_index = int(input("Please select a task number, or enter -1 to return to main menu: ")) - 1
        # If invalid option, keep prompting until valid selection made
        if task_index not in [-2, range(0,len(task_list))]:
            print("***** Invalid option selected. Please try again. *****")
            continue
        elif task_index in range(0,len(task_list)):
            while True:
                task_menu = int(input('''Select one of the following options below:
                1 - Mark task as complete
                2 - Edit task
                '''))
                # If invalid option, keep prompting until valid selection made
                if not task_menu in range(1, 3):
                    print("***** Invalid option selected. Please try again. *****")
                    continue
                else:
                    if task_menu == 1:
                        task_list[task_index] = task_list[task_index].replace("No", "Yes")
                        print(task_list[task_index])
                        # Re-open tasks.txt so that the whole file will be overwritten
                        # with the updated task completion
                        all_tasks = open('tasks.txt', 'w')
                        all_tasks.write(''.join(task_list))
                        all_tasks.close()  
                    elif task_menu == 2:
                        if "Yes" in task_list[task_index]: # if the task is complete
                            print("***** CANNOT EDIT COMPLETE TASK *****")
                        else:
                            while True:
                                edit_menu = int(input('''Select what you want to change about the task entry:
                                1 - Change the task's assigned user
                                2 - Change the task's due date
                                '''))
                                # If invalid option, keep prompting until valid selection made
                                if not edit_menu in range(1, 3):
                                    print("***** Invalid option selected. Please try again. *****")
                                    continue
                                else:
                                    # Same as before, split the current task into a list of 
                                    # its composite information
                                    task_info_list = task_list[task_index].split(", ")
                                    if edit_menu == 1:
                                        new_name = input(f"Task is current assigned to {task_info_list[0]}. Please enter the new assigned username: ")
                                        task_info_list[0] = new_name
                                    elif edit_menu == 2:
                                        new_date = input(f"Task is current due on {task_info_list[4]}. Please enter the new due date (dd-mmm-yyyy): ")
                                        task_info_list[4] = new_date
                                    # After modifying, rejoin into 1 string / 1 task again
                                    # and overwrite original task.txt.
                                    task_list[task_index] = ', '.join(task_info_list)
                                    all_tasks = open('tasks.txt', 'w')
                                    all_tasks.write(task_list)
                                    all_tasks.close()  
                                    break
                break
            break
        elif task_index == -2:
            # This is if user selects -1, then break out of this 
            # and return to main menu
            break
    
# ======== MENU: gr - Generate Reports ========
def report():
    # ======== task_overview ========
    # Process the contents into a list of tasks
    task_list = []
    all_tasks = open('tasks.txt', 'r')
    for task in all_tasks:
        task_list.append(task) 

    # As before for menu 'va' and 'vm', we turn each task in the list
    # into also a list of it's composites 
    for t in range(0, len(task_list)):
        task_list[t] = task_list[t].replace("\n", "").split(", ") 
    status = []
    dates = []
    assign = []
    # And then extract into a list of completion & a list of due dates
    for info in range(0, len(task_list)):
        task_info_list = task_list[info]
        status.append(task_info_list[-1])
        dates.append(task_info_list[4])
        assign.append(task_info_list[0])
    
    # Calculate metrics
    total_tasks = len(task_list)
    done = status.count("Yes")
    # For overdue tasks, find by comparing each task's date to today
    overdue_list = []
    for d in range(0, len(dates)):
        due = datetime.strptime(dates[d], "%d %b %Y")
        today = datetime.today()
        if due < today:
            # Create a binary result list where 1 = overdue, this will
            # be useful later for user specific statistics
            od = 1
        else:
            od = 0
        overdue_list.append(od)
    # Find tasks that are both overdue & incomplete
    incomplete_overdue = sum((t == 'Yes' for t in status) and (t == 1 for t in overdue_list))

    # ======== user_overview ========
    # Process the contents into a list of tasks
    user_list = []
    login_data = open('user.txt', 'r')
    for user in login_data:    # Take only the first half (usernames)
        user_list.append(user.split(', ')[0])
    total_users = len(user_list)
    # Cteate lists that store the task statistic for each user, by going
    # along the user_list one by one. Each list below is the same length
    # as the number of users.
    user_done_list = []
    user_overdue_list = []
    user_incomplete_overdue_list = []
    user_task_count = []
    for u in range(0, len(user_list)):
        user_task_count.append(assign.count(user_list[u]))
        # Finding user specific task statistics...
        # Double criteria that username must match the task's user, and 
        # the completion status = Yes / task is overdue
        user_done = 0
        user_overdue = 0
        user_incomplete_overdue = 0
        for a in range(0, len(assign)):  
            if assign[a] == user_list[u]: 
                if status[a] == 'Yes':
                    user_done += 1  
                if overdue_list[a] == 1:   
                    user_overdue += 1
                if status[a] == 'No' and overdue_list[a] == 1:
                    user_incomplete_overdue += 1
        # One full for loop of a means we have checked all the tasks for
        # just one user. So we append for a list of results for all users
        user_done_list.append(user_done)
        user_overdue_list.append(user_overdue)
        user_incomplete_overdue_list.append(user_incomplete_overdue)
    
    # ======== Output to text file ========
    # Format data and results for writing to text file. 
    task_text = f'''Total number of tasks: {total_tasks}
Total number of completed tasks: {done}
Total number of incomplete tasks: {total_tasks - done}
Total number of both incomplete & overdue tasks: {incomplete_overdue}
Total % of incomplete tasks: {round((total_tasks - done) / total_tasks * 100, 1)}
Total % of overdue tasks: {round(sum(overdue_list) / total_tasks * 100, 1)}
    '''
    with open('task_overview.txt', 'w') as file:
        file.write(str(task_text))
    
    # For user_overview.txt, use for loop to print results per user
    user_text = (f'''Total number of registered users: {total_users}
Total number of tasks: {total_tasks} \n''')
    with open('user_overview.txt', 'w') as file:
        file.write(str(user_text))
        for u in range(0, len(user_list)): 
            file.write(f'''
    -----------------------------------------------------
    USER {user_list[u]}
    -----------------------------------------------------
    Tasks assigned to user:               {user_task_count[u]} 
    % of total tasks assigned to user:    {round(user_task_count[u] / total_tasks * 100, 1)}
    % of user's completed tasks:          {round(user_done_list[u] / user_task_count[u] * 100, 1)}
    % of user's incomplete tasks:         {round((user_task_count[u] - user_done_list[u]) / user_task_count[u] * 100, 1)}
    % of user's tasks that are both incomplete & overdue: {round(user_incomplete_overdue_list[u] / user_task_count[u] * 100, 1)}
    ----------------------------------------------------- \n''')    



# ======== MENU ========
# Only once successfully logged in, do we get the menu options. 
while True:
    # Presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    #
    # Create conditional menu option only if user is admin. 
    admin_menu = ""
    if name == 'admin':
        admin_menu = "s - View statistics"

    menu = input(f'''Select one of the following options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - Generate report
        e - Exit
        {admin_menu}: ''').lower()
    
    if menu == 'r':
        reg_user(name)

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
    
    elif menu == 'gr':
        report()

    # ======== MENU: s - View statistics ========
    # As per the logic above, this option will only be displayed for admin. 
    elif menu == 's':
        # We add another logic, where if the current user is not admin, but they
        # type 's' anyways (e.g. by accident), then the following still does not
        # display for them
        if name == 'admin':
            # Check if the both overview text files exists
            if exists('task_overview.txt') == False or exists('user_overview.txt') == False:
                # If not, generate files by calling report function
                report()
            # Read first line from each file
            print(open('task_overview.txt').readlines()[0])
            print(open('user_overview.txt').readlines()[0])
        else:
            print("You have made a wrong choice, Please Try again")


    # ======== MENU: e - Exit ========
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")



