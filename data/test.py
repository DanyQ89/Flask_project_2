url = 'http://localhost:8888/api/'

# FOR JOBS

# GET

# print(get(url + 'jobs').json())
#
# print(get(url + 'jobs/2').json())
#
# print(get(url + 'jobs/999').json())
#
# print(get(url + 'jobs/m').json())
#


# POST

# # empty
# print(post(url + 'jobs', json={}).json())
#
# # not all parameters
# print(post(url + 'jobs',
#            json={'job': 'Заголовок'}).json())
#
# # not all parameters
# print(post(url + 'jobs', json={'team_leader': 228}).json())
#
#

# #good one
# print(post(url + 'jobs',
#            json={'job': 'Заголовок',
#                  'team_leader': 1,
#                  'work_size': 10,
#                  'collaborators': '1, 2, 3',
#                  'hazard': 2,
#                  'is_finished': False}).json())


# DELETE


# #not number
# print(delete(url + 'jobs/Ф').json())
#
# #not found error
# print(delete(url + 'jobs/999').json())
#
# #good one
# print(delete(url + 'jobs/6').json())


# PUT


# # empty
# print(put(url + 'jobs/6', json={}))
#
# # letter
# print(put(url + 'jobs/a', json={}))
#
# # good one
# print(put(url + 'jobs/5', json={'job': 'smth',
#                                                     'team_leader': 3,
#                                                     'work_size': 100,
#                                                     'collaborators': '2, 4',
#                                                     'hazard': 3,
#                                                     'is_finished': True
#                                                     }).json())


# FOR USERS

# print(put(url + 'users/8', json={
#     'name':'test_name',
#     'surname':'test_surname',
#     'age': 33,
#     'position': 'captain of meow',
#     'speciality': 'work',
#     'address': 'Saint-Petersburg, petrogradskaya 5',
#     'email': 'meow_2@icloud.com',
#     'hashed_password': 'meow'
# }))

# print(put(url + 'users/1', json={'position': 'captain of meow'}))


# print(delete(url + 'users/8').json())
