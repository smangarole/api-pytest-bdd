import requests
import json

from pytest_bdd import scenarios, given, then, parsers

EXTRA_TYPES = {
    'String': str,
    'Number': int
}

# Shared Variables

RESOURCE_API = 'https://jsonplaceholder.typicode.com'
RESOURCE_API_TODOS = RESOURCE_API + '/todos'
RESOURCE_API_USERS = RESOURCE_API + '/users'

# Scenarios

scenarios('../features/todos.feature')


# Here I will get all users who have tasks assigned to them. Even though all users have tasks,
# I want to make sure that I get users with tasks in case some users are added where not tasks are assigned to them
# store users in a list
@given(parsers.cfparse('user has todos tasks'), target_fixture='users_with_tasks')
def users_with_tasks():
    params = {'format': 'json'}
    raw_json = requests.get(RESOURCE_API_TODOS, params=params)
    users_with_task = []
    for entry in raw_json.json():
        if entry['userId'] not in users_with_task:
            users_with_task.append(entry['userId'])

    print(users_with_task)
    return users_with_task


# Filter by city "FanCode" - given Lat and Long. Store users in a list
@given(parsers.cfparse('user belongs to the city "{city:String}"', extra_types=EXTRA_TYPES),
       target_fixture='filter_by_city')
def filter_by_city(users_with_tasks, city):
    params = {'format': 'json'}
    raw_json = requests.get(RESOURCE_API_USERS, params=params)
    users_in_fancode = []

    for entry in raw_json.json():
        if entry['id'] in users_with_tasks:
            lat = float(entry['address']['geo']['lat'])
            long = float(entry['address']['geo']['lng'])
            if lat <= 5 and lat >= -40 and long >= 5 and long <= 100:
                users_in_fancode.append(entry['id'])
                print(entry)

    return users_in_fancode


# check completed task percentage per user
@then(parsers.cfparse('user completed task are more than "{phrase:String}"', extra_types=EXTRA_TYPES))
def half_plus_tasks_completed(filter_by_city):
    params = {'format': 'json'}
    raw_json = requests.get(RESOURCE_API_TODOS, params=params)
    json_data = json.loads(raw_json.text)
    final_ids = []

    for userid in filter_by_city:
        output_dict = [x for x in json_data if x['userId'] == userid]
        completed = [y for y in output_dict if y['completed'] == True]
        print(completed)
        count_output = len(output_dict)
        count_complete = len(completed)
        percent = count_complete / count_output * 100

        if percent > 50:
            final_ids.append(userid)

    print(final_ids)
