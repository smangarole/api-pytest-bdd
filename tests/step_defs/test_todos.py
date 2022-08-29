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


@given(parsers.cfparse('user has todos tasks'), target_fixture='users_with_tasks')
@given("user has todos tasks", target_fixture='users_with_tasks')
def users_with_tasks():
    params = {'format': 'json'}
    response = requests.get(RESOURCE_API_USERS, params=params)

    print(response)
    return response


@given(parsers.cfparse('user belongs to the city "{city:String}"', extra_types=EXTRA_TYPES),
       target_fixture='filter_by_city')
@given('user belongs to the city "FanCode"', target_fixture='filter_by_city')
def filter_by_city(user_with_tasks, city):
    pass


@then(parsers.cfparse('user completed task are more than "{phrase:String}"', extra_types=EXTRA_TYPES))
@then('user completed task are more than "half"')
def half_plus_tasks_completed(filter_by_city, phrase):
    pass
