import sys
import datetime
import os

print('Hello ' + sys.argv[1])
time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(f'time={time}', file=fh)