"""testing module for greedy_alg()"""


from greedy_alg import greedy


class TestClass:
    def test_one(self):
        assert greedy({'MTS': {4, 5, 7, 9},
                       'MEGAFON': {1, 2, 3, 4, 5, 6},
                       'YOTA': {1, 4, 5, 10, 11}},
                      {1, 2, 3, 4, 5, 7, 11}) == ['MEGAFON', 'MTS', 'YOTA']

    def test_two(self):
        assert greedy({'MTS': {4, 5, 7, 9},
                       'MEGAFON': {1, 2, 3, 4, 5, 6},
                       'YOTA': {1, 4, 5, 10, 11}},
                      {1, 2, 3, 4, 5, 7, 77}) == ['Один из регионов '
                                                  'не входит в покрытие всех операторов']

    def test_three(self):
        assert greedy({'YOTA': {1, 5, 19, 77, 1001},
                       'MTS': {2, 3, 4, 5, 6, 7},
                       'MEGAFON': {1, 3, 5, 177}},
                      {2, 5, 6, 7, 77, 177, 1001}) == ['MTS', 'YOTA', 'MEGAFON']
