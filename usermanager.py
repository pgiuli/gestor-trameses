import db
import random

from unidecode import unidecode

names = []

cleaned_names = [unidecode(name) for name in names]

#Create users by isolating initials and random password, store them in a csv file aswell

users_dict = {}

def create_users_dict(list):
    for name in list:
        try:
            initials = name.split()[0][0] + name.split()[1][0] + name.split()[2][0]
        except:
            initials = name.split()[0][0] + name.split()[1][0] + '#'
        password = ''.join(random.choices('1234567890', k=3))
        users_dict[initials] = password
    return users_dict

        
def create_users_csv(dict):
    with open('usuaris.csv', 'w') as f:
        for key in dict.keys():
            f.write("%s,%s\n"%(key,dict[key]))
    return f

def create_users(dict):
    for key in dict.keys():
        db.add_user(key, dict[key])

create_users_dict(cleaned_names)
create_users_csv(users_dict)
create_users(users_dict)