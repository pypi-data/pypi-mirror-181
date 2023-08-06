from __future__ import unicode_literals
from os.path import abspath, join, dirname
import random


__title__ = 'namesfr'
__version__ = '0.0.1'
__author__ = 'Nicolas Renard'
__license__ = 'MIT'


def full_path(filename):
    return abspath(join(dirname(__file__), filename))


FILES = {
    'first:male': full_path('dist.male.first'),
    'first:female': full_path('dist.female.first'),
    'last': full_path('dist.all.last'),
}


def get_name(filename):
    selected = random.random() * 90
    with open(filename, encoding="UTF-8") as name_file:
        for line in name_file:
            name, _, cummulative, _ = line.split(";")
            if float(cummulative) > selected:
                return name.rstrip()
    return ""  # Return empty string if file is empty


def get_first_name(gender=None):
    if gender is None:
        gender = random.choice(('male', 'female'))
    if gender not in ('male', 'female'):
        raise ValueError("Only 'male' and 'female' are supported as gender")
    return get_name(FILES['first:%s' % gender]).capitalize()


def get_last_name():
    return get_name(FILES['last']).capitalize()


def get_full_name(gender=None):
    return "{0} {1}".format(get_first_name(gender), get_last_name())
