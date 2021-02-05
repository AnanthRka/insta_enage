from os import system,name
from time import sleep
from instapy import InstaPy
from instapy.util import smart_run
from getpass import getpass
from datetime import date
import sys



# to check for exiting users username and last last login date
def users():
    try:
        f = open('users.txt','r+')
        details = [i.strip('\n') for i in f.readlines()]
        f.close()

        if len(details) ==0:
            user = input('Enter username: ')
            password = getpass('Enter password: ')
            details.append(user)
            details.append(password)
            clear_screen()
        
        return details

    # locally saves the file
    except FileNotFoundError:       # if using for first time
        f = open('users.txt','x')
        f.close()
        details = users()
        return details


# to clear the screen for better input visibility
def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# main 
if '__main__':
    
    logged_in_today = False
    user_details = users()      # to get user details

    if len(user_details) == 2:
        user_details.append(str(date.today()))      # if using for first time
    else:
        if user_details[2] == str(date.today()):    # if you have already used once a day
            logged_in_today = True
    
    # writing into file for reference
    with open('users.txt','w') as f:
        f.truncate(0)
        
        for i in range(len(user_details)):

            if i != len(user_details)-1:
                f.write(user_details[i]+'\n')
            else:
                f.write(user_details[i])

    # creating lists for storage of tags, comments and don't include tags
    tags = []
    comments = []
    dont_tags = []

    if not logged_in_today:     # if using for the first time in a day

        print('You can enter upto 2 tags and atleast 1 tag to proceed')
        print('Press Enter to stop input.')
    
        for i in range(2):      # get input tags
            a= input('Enter a tag: ')
            if a == '':
                if i ==0:
                    tags.append(input('Input cannot be empty. Please enter a tag: '))
                    if tags[0] == '':
                        print('Exiting code due to invalid input')
                        sys.exit()
                break
            tags.append(a)
        clear_screen()
        print('You can enter upto 5 different comments (You can emojis too by pressing "Windows + . ")')
        print('Press Enter to stop the input.')
        
        for i in range(5):      # get input comments
            a= input('Enter a comment: ')
            if a == '':
                if i ==0:
                    comments.append(input('Input cannot be empty. Please enter a comment: '))
                    if comments[0] == '':
                        print('Exiting code due to invalid input')
                        sys.exit()
                break
            comments.append(a)
        clear_screen()

        # assigning values for likes, comments and follows based on the inputs
        if len(tags) == 1:
            like_amount = 5
            comment_percentage = 15
            follow_percentage = 20
        else:
            like_amount = 1
            comment_percentage = 10
            follow_percentage = 20
    
    else:       # if already used the code for a day

        print('Since you have already used the program once today there are some restrictions appied by default')

        print()
        tags.append(input('You can enter only one tag. Enter the tag name: '))
        clear_screen()

        print()
        print('You can enter 3 comments. Press Enter to stop input.')

        for i in range(3):
            a = input('Enter the comment: ')
            if a =='':
                if i ==0:
                    comments.append(input('Input cannot be empty. Please enter a comment: '))
                    if comments[0] == '':
                        print('Exiting code due to invalid input')
                        sys.exit()
                break
            comments.append(a)
        clear_screen()
        like_amount = 1
        comment_percentage = 10
        follow_percentage = 20
   

    # input for don't include tags
    # these tags prevent you from mixing up tags which are not related to the tag you want
    # but are rather used for promotional purposes
    print()
    print("Enter the tags you don't want to include. This helps in preventing commenting on inappropiate posts.")
    print('Press Enter to stop the input.')
    
    while True:
        a = input("Enter a don't include tag: ")
        if a =='':
            if i ==0:
                    dont_tags.append(input('Input cannot be empty. Please enter a tag: '))
                    if dont_tags[0] == '':
                        print('Exiting code due to invalid input')
                        sys.exit()
            break
        dont_tags.append(a)
    clear_screen()

    print()
    print('The tags you have entered are: ')
    for i in tags:
        print(i)
    
    print()
    print('The comments you have entered are: ')
    for i in comments:
        print(i)
    
    print()
    print("The don't include tags are: ")
    for i in dont_tags:
        print(i)

    print()
    print('Starting the bot...')
    sleep(10)
    clear_screen()
    # starting session with instapy
    session = InstaPy(username=user_details[0], password= user_details[1])
    with smart_run(session):
        session.login()
        session.set_do_follow(True,percentage=follow_percentage, times=2)
        session.set_comments(comments)
        session.set_do_comment(True, percentage=comment_percentage)
        session.set_dont_like(dont_tags)
        session.like_by_tags(tags,amount=like_amount)
    session.end()