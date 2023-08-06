import json
import sys
from time import sleep

import pandas as pd
import requests


def handle_df(url, file, _from):
    payload = {
        'logs': []
    }
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        ls = row.values
        payload['logs'].append({
            'time': ls[0],
            'level': ls[1],
            'thread': ls[2],
            'message': ls[3],
            'from': _from
        })

    headers = {'Content-type': 'application/json'}
    requests.post(url=url, data=json.dumps(payload), headers=headers)
    open('../log.csv', 'w').close()


if __name__ == '__main__':
    pr, url, file, _from = sys.argv

    while True:
        handle_df(url=url, file=file, _from=_from)
        sleep(60 * 60 * 24)
