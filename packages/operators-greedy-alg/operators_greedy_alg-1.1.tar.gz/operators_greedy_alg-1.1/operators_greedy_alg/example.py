"""example module"""

from greedy_alg import greedy

print('example 1')
phone_operator_regions_1 = {'MTS': {4, 5, 7, 9},
                            'MEGAFON': {1, 2, 3, 4, 5, 6},
                            'YOTA': {1, 4, 5, 10, 11}}
regions_1 = {1, 2, 3, 4, 5, 7, 11}
print(phone_operator_regions_1, regions_1,)
print(greedy(phone_operator_regions_1, regions_1))

print('example 2')
phone_operator_regions_2 = {'MTS': {4, 5, 7, 9},
                            'MEGAFON': {1, 2, 3, 4, 5, 6},
                            'YOTA': {1, 4, 5, 10, 11}}
regions_2 = {1, 2, 3, 4, 5, 7, 77}
print(phone_operator_regions_2, regions_2)
print(greedy(phone_operator_regions_2, regions_2))

print('example 3')
phone_operator_regions_3 = {'YOTA': {1, 5, 19, 77, 1001},
                            'MTS': {2, 3, 4, 5, 6, 7},
                            'MEGAFON': {1, 3, 5, 177}}
regions_3 = {2, 5, 6, 7, 77, 177, 1001}
print(phone_operator_regions_3, regions_3)
print(greedy(phone_operator_regions_3, regions_3))
