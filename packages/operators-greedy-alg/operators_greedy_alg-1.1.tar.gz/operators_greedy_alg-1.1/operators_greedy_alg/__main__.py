"""simple interface for demonstration"""

import argparse
import re
from greedy_alg import greedy
try:
    import pytest
except ImportError:
    pytest = None


def main():
    """CLI arguments, possible options for finding set of operators"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-cover', type=str, help='A dictionary whose keys are the names of mobile operators, '
                                                 'and the values are the sets of regions they cover', default='')
    parser.add_argument('-regions', type=str, help='The set of all regions that need to be covered', default='')
    parser.add_argument('-t', '--test', action='store_true', help='test mode')
    args = parser.parse_args()
    phone_operator_regions_str = args.cover
    reg = args.regions
    test = args.test
    if test:
        print('TEST')
        if pytest:
            pytest.main(['-q', 'operators_greedy_alg/test.py'])
        else:
            print('No pytest found, only doctest will run')
    else:
        phone_operator_regions = dict()
        phone_operators = re.findall(r'[a-zA-Z]+', phone_operator_regions_str)
        regions_covered_mas = re.findall(r'\[[^a-zA-Z]+]', phone_operator_regions_str)
        regions_covered = []
        regions = set(map(int, reg[1:-1].split()))
        for i in range(len(regions_covered_mas)):
            regions_covered.append(set(map(int, regions_covered_mas[i][1:-1].split())))
        for j in range(len(phone_operators)):
            phone_operator_regions[phone_operators[j]] = regions_covered[j]
        print(greedy(phone_operator_regions, regions))


if __name__ == '__main__':
    main()
