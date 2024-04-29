import os
import re
import math
import argparse
import ipaddress
from pathlib import Path
from collections import deque
import logging

# Pre-compile regex patterns
regex_patterns = {
    'cidr': re.compile(r'^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$'),
    'lastOctet': re.compile(r'^(\d{1,3}\.){3}\d{1,3}-\d{1,3}$'),
    'allOctets': re.compile(r'^(\d{1,3}\.){3}(\d{1,3})-(\d{1,3}\.){3}\d{1,3}$'),
    'single': re.compile(r'^(\d{1,3}\.){3}(\d{1,3})$')
}

def expand(ipRange):
    scope = []
    if regex_patterns['cidr'].search(ipRange):
        net = ipaddress.ip_network(ipRange)
        for adder in net:
            scope.append(str(ipaddress.IPv4Address(adder)))
    elif regex_patterns['lastOctet'].search(ipRange):
        adder = ipRange.split('.')
        startEnd = adder[3].split('-')
        start = int(startEnd[0])
        end = int(startEnd[1])
        for i in range(start, end + 1):
            scope.append(adder[0] + '.' + adder[1] + '.' + adder[2] + '.' + str(i))
    elif regex_patterns['allOctets'].search(ipRange):
        startEnd = ipRange.split('-')
        start_ip = ipaddress.IPv4Address(startEnd[0])
        end_ip = ipaddress.IPv4Address(startEnd[1])
        for ip_int in range(int(start_ip), int(end_ip) + 1):
            scope.append(str(ipaddress.IPv4Address(ip_int)))
    elif regex_patterns['single'].search(ipRange):
        scope.append(ipRange)
    else:
        logging.warning("Cannot parse: " + ipRange)
        return []
    return scope

def process_file(input_file_path, exclude_set, output_file_path):
    with open(input_file_path, 'r') as inputFile, open(output_file_path, 'a') as outputFile:
        for case in inputFile:
            case = case.rstrip("\n")
            for ip in expand(case):
                if ip not in exclude_set:
                    outputFile.write(ip + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Path to input file')
    parser.add_argument('-e', '--exclude', help='Path to exclude file')
    parser.add_argument('-o', '--output', default=os.getcwd() + "/output.txt", help='Output file')
    parser.add_argument('-s', '--split', type=int, default=1, help='Number of files to split results into')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    # Convert exclude list to a set for efficient lookup
    exclude_set = set()
    if args.exclude:
        try:
            with open(args.exclude, 'r') as excludeFile:
                for line in excludeFile:
                    line = line.strip()
                    exclude_set.update(expand(line))
        except IOError:
            logging.error("Failed to read exclude file")


    # Process input file
    process_file(args.input, exclude_set, Path(args.output))

    # File splitting logic
    if args.split > 1:
        allIps = deque([])
        with open(args.output, 'r') as fullList:
            for line in fullList:
                allIps.append(line)
        numPerFile = math.ceil(len(allIps)/args.split)
        print(len(allIps))
        print(numPerFile)
        for fileNum in range(args.split):
            with open(Path(str(args.output) + str(fileNum)), 'a') as outputFile:
                for _ in range(numPerFile):
                    if allIps:
                        print(allIps.popleft().rstrip("\n"), file=outputFile)
                    else:
                        break

if __name__ == "__main__":
    main()
