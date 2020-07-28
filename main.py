#!/usr/bin/env python3.8
# by default, read example.yaml and generate csv

import yaml
import optparse
import pandas as pd
import datetime


def output_data(config):
    cars = {'Brand': ['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
            'Price': [22000, 25000, 27000, 35000]
            }
    df = pd.DataFrame(cars, columns=['Brand', 'Price'])

    print(df)

    if config['row']['format'] != 'timerange':
        return
    start = config['row']['range_start']
    end = config['row']['range_end']

    # TODO: frequence should read from yaml
    a = pd.date_range(start, end, freq='min')
    print(a)


class Confighandler:
    def __init__(self, docs):
        if len(docs) > 1:
            print('Not support moltiple config in one yaml file')
            return
        if len(docs) == 0:
            print('No config in yaml')
            return
        self.doc = docs[0]
        self.basic_check()

    def summerize(self):
        print("[INFO] title" + self.doc['name'])
        # print(self.doc['columns'])
        print("[INFO] Num of columns: " +
              str(len(self.doc['columns'])))
        # print(self.doc['row'])

    def basic_check(self):
        # will raise KeyError is the key not exist
        if self.doc['name'] and self.doc['columns'] and self.doc['row']:
            pass

        if len(self.doc['columns']) == 0:
            raise Exception('Columns need to be at least one')


def generate_data(docs):
    try:
        c = Confighandler(docs)
        c.summerize()
    except (KeyError):
        print("Make sure Necessary fields are specified in config yaml file")
        raise
    output_data(c.doc)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-c', '--config', dest='config',
                      default='example.yaml',
                      help="set an  configuration file", metavar='CONFIG')
    (options, args) = parser.parse_args()

    config_file = options.config
    stream = open(config_file, 'r')
    docs = yaml.safe_load(stream)
    # print(docs)
    generate_data(docs)
