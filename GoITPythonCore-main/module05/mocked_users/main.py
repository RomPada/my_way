from mock import get_mocked_user
import json

filename = input("Enter filename >>> ")
amount = int(input("How many fake users you want >>> "))


with open(filename, "w") as file:
    mocked_users = []
    for i in range(amount):
        mocked_users.append(get_mocked_user())
    
    json.dump(mocked_users, file, indent=4, sort_keys=True)



