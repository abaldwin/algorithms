import sys
from re import match
import argparse
from string import digits


class RunLengthEncoding:
    """Compress or decompress lowercase ASCII strings using run-length encoding"""
    
    def compress(self, input_string):
        """Compress a string using run-length encoding"""
        if not match(r'^[a-z]*$', input_string):
            raise ValueError("Input string must be all lower case letters")
        
        output_string = ''
        idx = 0
        max_idx = len(input_string)

        while idx < max_idx:
            char = input_string[idx]
            char_count = 0
            while idx < max_idx and input_string[idx] == char:
                char_count += 1
                if char_count == 9:
                    output_string += char + '9'
                    char_count = 0
                idx += 1

            if char_count > 0:
                output_string += char
                if char_count >= 2:
                    output_string += str(char_count)                

        return output_string
    
    def decompress(self, input_string):
        """Return the uncompressed version of the input string"""
        if not match(r'^(?:([a-z]){1}([2-9]){1}|[a-z])*$', input_string):
            raise ValueError("Invalid compression")

        output_string = ''
        idx = 0
        max_idx = len(input_string)

        while idx < max_idx:
            char = input_string[idx]
            try:
                if (idx + 1) < max_idx and input_string[idx + 1] in digits:
                    output_string += char * int(input_string[idx + 1])
                    idx += 2
                else:
                    output_string += char
                    idx += 1
            except ValueError:
                sys.exit("Invalid Compression")

        return output_string


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compress or decompress \
                    lowercase ascii strings using run-length encoding')
    parser.add_argument('action',
                        nargs=1,
                        choices=['compress', 'decompress'],
                        help='The action to take (compress or decompress)')
    parser.add_argument('strings',
                        nargs='*',
                        metavar="STRING",
                        default=[],
                        help='The string or strings to process')
    parser.add_argument('-i', '--input', 
                        metavar="FILE", 
                        nargs='?', 
                        type=argparse.FileType('r'), 
                        default=sys.stdin, 
                        help="input filename")
    parser.add_argument('-o', '--output', 
                        metavar="FILE", 
                        nargs='?', 
                        type=argparse.FileType('w'), 
                        default=sys.stdout, 
                        help="output filename")
    
    args = parser.parse_args()
        
    rle = RunLengthEncoding()
    
    action = args.action[0]

    strings = args.strings
    if not strings:
        strings = args.input
    
    for string in strings:
        args.output.write(getattr(rle, action)(string.strip()))
        args.output.write('\n')
    
    

