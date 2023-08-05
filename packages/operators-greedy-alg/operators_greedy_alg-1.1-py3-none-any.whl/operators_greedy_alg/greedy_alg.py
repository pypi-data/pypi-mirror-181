"""The module "greedy alg"
a) select the operator covering the largest number
of regions and not yet included in the coverage. If the operator will cover
some regions already included in the coverage, this is normal;
b) repeat until uncovered elements of the set remain"""


def greedy(phone_operator_regions, regions):
    """
        module example:
        >>> greedy({'MTS': {4, 5, 7, 9}, 'MEGAFON': {1, 2, 3, 4, 5, 6}}, {1, 2, 3, 4, 5, 7})
        ['MEGAFON', 'MTS']
        >>> greedy({'MTS': {4, 5, 7, 9}, 'MEGAFON': {1, 2, 3, 4, 5, 6}}, {1, 2, 3, 4, 5, 1001})
        'Один из регионов не входит в покрытие всех операторов'
        :param phone_operator_regions: dictionary with operators
        :param regions: set of regions
        :return: list with answer
        """
    phone_operator = list(phone_operator_regions)
    answer = []
    while regions != set():
        hit_max = name_of_max = 0
        for i in range(len(phone_operator)):
            hits = len(phone_operator_regions[phone_operator[i]] & regions)
            if hits > hit_max:
                hit_max = hits
                name_of_max = phone_operator[i]
        try:
            regions = regions.difference(phone_operator_regions[name_of_max])
            del phone_operator_regions[name_of_max]
            phone_operator.remove(name_of_max)
            answer.append(name_of_max)
        except KeyError:
            print('Один из регионов не входит в покрытие всех операторов')
            return ''
    return answer


if __name__ == '__main__':
    import doctest
    doctest.testmod()
