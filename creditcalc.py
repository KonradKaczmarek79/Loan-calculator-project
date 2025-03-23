import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--principal")
parser.add_argument("--payment")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--type")

args = parser.parse_args()
