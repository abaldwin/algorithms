import cProfile
from rle import RunLengthEncoding

rle = RunLengthEncoding()

# Generate regex expressions
cProfile.run('rle.compress("aaazzyxbbcccdsst")')
cProfile.run('rle.decompress("a3z2yxb2c3ds2t")')

# Run speed tests for large input strings
cProfile.run('rle.compress("aaazzyxbbcccdsst" * 200000)')
cProfile.run('rle.decompress("a3z2yxb2c3ds2t" * 200000)')
