Run-length encoding of lowercase ASCII strings

Input text is limited to the characters from a to z. If there is only one 
occurrence of a letter, the output is just the letter, but if there 
are 2­-9 letters, print the letter plus the number of occurrences.  If there are 
more than 9 occurrences of one letter in a row, you compress the first 9, 
then continue. 

To use the module, instantiate the class and run compress or decompress on
an appropriate string:

    import rle

    example_string1 = 'aaazzyxbbcccdsst'
    example_string2 = 'aaaaaaaaaabbbbbbbbbbb' # 10 A’s followed by 11 B’s

    r = rle.RunLengthEncoding()
    r.compress(example_string1) # 'a3z2yxb2c3ds2t'
    r.compress(example_string2) # 'a9ab9b2'
    
    r.decompress('a3z2yxb2c3ds2t') # 'aaazzyxbbcccdsst'
    r.decompress('a9ab9b2') # 'aaaaaaaaaabbbbbbbbbbb'
    
    example_string1 == r.decompress(r.compress(example_string1)) # True
    example_string2 == r.decompress(r.compress(example_string2)) # True

The program can be run from the command line. To see what options
are available, run the command:

    python rle.py --help
