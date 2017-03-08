import random
import unittest
from string import ascii_lowercase, digits, printable, whitespace

import rle

class TestRleCompression(unittest.TestCase):

    def setUp(self):
        self.rle = rle.RunLengthEncoding()
    
    def testCanCompressOneLetter(self):
        for letter in ascii_lowercase:
            output_string = self.rle.compress(letter)
            self.assertEqual(output_string, letter)
    
    def testCanCompressMultipleLetters(self):
        self.assertEqual('a3z2yxb2c3ds2t', self.rle.compress('aaazzyxbbcccdsst'))
        self.assertEqual('a9ab9b2', self.rle.compress('aaaaaaaaaabbbbbbbbbbb'))
        self.assertEqual('a8b9b2c', self.rle.compress('aaaaaaaabbbbbbbbbbbc'))
        self.assertEqual('a9b9b2c', self.rle.compress('aaaaaaaaabbbbbbbbbbbc'))
        self.assertEqual('a9ab9b2cd2', self.rle.compress('aaaaaaaaaabbbbbbbbbbbcdd'))
            
    def testCanCompressMultipleLettersOfVaryingLengths(self):
        for num, letter in enumerate(ascii_lowercase, start=1):
            input_string = num * letter
            
            expected_output = ''
            groups_of_nine = num // 9
            if groups_of_nine > 0:
                expected_output += (letter + '9') * groups_of_nine
            
            final_group_count = num % 9
            if final_group_count > 0:
                expected_output += letter
                if final_group_count >= 2:
                    expected_output += str(final_group_count)
            
            output_string = self.rle.compress(input_string)
            self.assertEqual(output_string, expected_output)
            
    def testCompressedStringContainsOnlyValidCharacters(self):
        for num, letter in enumerate(ascii_lowercase, start=1):
            input_string = num * letter
            
            output_string = self.rle.compress(input_string)
            for character in output_string:
                self.assertTrue(character in ascii_lowercase
                                or character in digits)

    def testCompressionWithInvalidCharacterRaisesError(self):        
        invalid_chars = [c for c in printable 
                                    if c not in ascii_lowercase
                                    and c not in whitespace]
        invalid_chars.append(' ')
        for character in invalid_chars:
            self.assertRaises(ValueError, self.rle.compress, character)
            
    def testCompressionWithInvalidCharactersInStringRaisesError(self):
        input_string = ''
        for num, letter in enumerate(ascii_lowercase, start=1):
            input_string += letter * num
        len_input_string = len(input_string)
        
        invalid_chars = [c for c in printable 
                                    if c not in ascii_lowercase
                                    and c not in whitespace]
        invalid_chars.append(' ')
        for character in invalid_chars:
            idx = random.randint(1, len_input_string - 2)
            num = random.randint(1, 3)
            input_string_as_list = list(input_string)
            input_string_as_list.insert(idx, character * num)
            new_input_string = ''.join(input_string_as_list)
            assert(new_input_string.find(character) > -1)
            self.assertRaises(ValueError, self.rle.compress, new_input_string)
            
    def testCompressionOfInvalidCharactersAtBeginningOfStringRaisesError(self):
        input_string = ''
        for num, letter in enumerate(ascii_lowercase, start=1):
            input_string += letter * num
        len_input_string = len(input_string)
        
        invalid_chars = [c for c in printable 
                                    if c not in ascii_lowercase
                                    and c not in whitespace]
        for character in invalid_chars:
            num = random.randint(1, 3)
            new_input_string = character * num + input_string
            assert(new_input_string.find(character) > -1)
            self.assertRaises(ValueError, self.rle.compress, new_input_string)
    
    def testCompressionOfInvalidCharactersAtEndOfStringRaisesError(self):
        input_string = ''
        for num, letter in enumerate(ascii_lowercase, start=1):
            input_string += letter * num
        len_input_string = len(input_string)
        
        invalid_chars = [c for c in printable 
                                    if c not in ascii_lowercase
                                    and c not in whitespace]
        for character in invalid_chars:
            num = random.randint(1, 3)
            new_input_string = input_string + character * num
            assert(new_input_string.find(character) > -1)
            self.assertRaises(ValueError, self.rle.compress, new_input_string)
            

class TestRleDecompression(unittest.TestCase):

    def setUp(self):
        self.rle = rle.RunLengthEncoding()
        
    def testCanDecompressSingleLetter(self):
        for letter in ascii_lowercase:
            output_string = self.rle.decompress(letter)
            self.assertEqual(output_string, letter)
            
    def testCanDecompressSingleLetterGroup(self):
        for num in range(1, 10):
            string = 'a'
            if num > 1:
                string += str(num)
            self.assertEqual('a' * num, self.rle.decompress(string))
            
    def testCanDecompressMultipleLetterGroups(self):
        self.assertEqual('aaazzyxbbcccdsst', self.rle.decompress('a3z2yxb2c3ds2t'))
        self.assertEqual('aaaaaaaaaabbbbbbbbbbb', self.rle.decompress('a9ab9b2'))
        
    def testDecompressedStringContainsOnlyValidCharacters(self):
        for num, letter in enumerate(ascii_lowercase, start=1):
            input_string = num * letter
            
            output_string = self.rle.compress(input_string)
            for string in ['a3z2yxb2c3ds2t', 'a9ab9b2']:
                output_string = self.rle.decompress(string)
                for character in output_string:
                    self.assertTrue(character in ascii_lowercase)
    
    def testDecompressionWithInvalidGroupLengthsRaisesError(self):        
        invalid_strings = ['a1', 'a1b5', 'a4b1', 'a10', 'a10b5',
                           'a5b10']
        for string in invalid_strings:
            self.assertRaises(ValueError, self.rle.decompress, string)

    def testDecompressionWithInvalidCharacterRaisesError(self):        
        invalid_chars = [c for c in printable 
                                    if c not in ascii_lowercase
                                    and c not in whitespace]
        invalid_chars.append(' ')
        for character in invalid_chars:
            self.assertRaises(ValueError, self.rle.decompress, character)
            
    def testDecompressionWithInvalidCharactersInStringRaisesError(self):
        input_string = 'a3z2yxb2c3ds2t'
        len_input_string = len(input_string)
        
        invalid_chars = [c for c in printable 
                                    if c not in ascii_lowercase
                                    and c not in whitespace
                                    and c not in digits]
        invalid_chars.append(' ')
        for character in invalid_chars:
            idx = random.randint(1, len_input_string - 2)
            num = random.randint(1, 3)
            input_string_as_list = list(input_string)
            input_string_as_list.insert(idx, character * num)
            new_input_string = ''.join(input_string_as_list)
            assert(new_input_string.find(character) > -1)
            self.assertRaises(ValueError, self.rle.decompress, new_input_string)
            
    def testDecompressionOfInvalidCharactersAtBeginningOfStringRaisesError(self):
        input_string = 'a3z2yxb2c3ds2t'
        len_input_string = len(input_string)
        
        invalid_chars = [c for c in printable 
                                    if c not in ascii_lowercase
                                    and c not in whitespace
                                    and c not in digits]
        for character in invalid_chars:
            num = random.randint(1, 3)
            new_input_string = character * num + input_string
            assert(new_input_string.find(character) > -1)
            self.assertRaises(ValueError, self.rle.decompress, new_input_string)
    
    def testDecompressionOfInvalidCharactersAtBeginningOfStringRaisesError(self):
        input_string = 'a3z2yxb2c3ds2t'
        len_input_string = len(input_string)
        
        invalid_chars = [c for c in printable 
                                    if c not in ascii_lowercase
                                    and c not in whitespace
                                    and c not in digits]
        for character in invalid_chars:
            num = random.randint(1, 3)
            new_input_string = input_string + character * num
            assert(new_input_string.find(character) > -1)
            self.assertRaises(ValueError, self.rle.decompress, new_input_string)

if __name__ == '__main__':
    unittest.main()
