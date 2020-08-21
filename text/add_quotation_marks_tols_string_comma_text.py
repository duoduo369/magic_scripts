#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
abc,
bcd,
adsf,

-->

"abc",
"bcd",
"adsf",
'''

def transform_text(text):
    text.replace(' ', '').replace('\n', '')
    return
import click
import re

RE = re.compile(r'[\t\n ]')

@click.command()
@click.option('--input_path', required=True, help="input data path")
@click.option('--output_path', default='/tmp/quotationed_text.txt', help="output data path")
def run(input_path, output_path):
    with open(input_path) as f:
        text = f.read()
    result = ' '.join('"{}",'.format(each) for each in RE.sub('', text).split(',') if each)
    with open(output_path, 'w') as f:
        f.write(result)


if __name__ == '__main__':
    run()
