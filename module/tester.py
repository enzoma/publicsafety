#!/usr/bin/env python
# encoding: utf-8
"""
tester.py

Created by Ed on 2013-07-10.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import Tool


def main():
# Place holder for file directory 
f= '/Users/Ed/mounts/cpd/crimes_2013.csv'
Tool.load_data_from_csv(f)


if __name__ == '__main__':
  main()

