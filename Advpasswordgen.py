import random
import string
import re
import nltk
import os
nltk.download('words')
from nltk.corpus import words

# Load the dictionary of English words
word_list = words.words()
word_set = set(word_list)  # Using a set for faster lookup

def load_common_passwords(file_path):
    try:
        with open(file_path, 'r') as file:
            common_passwords = set(line.strip().lower() for line in file)
        return common_passwords
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return set()

def load_saved_path(config_file='config.txt'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            path = file.readline().strip()
            if os.path.exists(path):
                return path
    return None

def save_path(path, config_file='config.txt'):
    with open(config_file, 'w') as file:
        file.write(path)

def get_custom_patterns():
    custom_patterns = []
    print("Enter custom patterns to avoid (leave blank to stop):")
    while True:
        pattern = input("Pattern: ").strip()
        if not pattern:
            break
        custom_patterns.append(pattern.lower())  # Store patterns in lowercase for consistent checking
    return custom_patterns

def is_sequential(password):
    sequential_patterns = [''.join([chr(ord(char) + i) for i in range(3)]) for char in string.ascii_lowercase[:24]]
    sequential_patterns += [''.join([chr(ord(char) - i) for i in range(3)]) for char in string.ascii_lowercase[2:]]
    sequential_patterns += [str(i) + str(i+1) + str(i+2) for i in range(8)]
    sequential_patterns += [str(i+2) + str(i+1) + str(i) for i in range(8)]

    for pattern in sequential_patterns:
        if pattern in password:
            return True
    return False

def is_repeated_pattern(password):
    for i in range(1, len(password)//2 + 1):
        if password[:i] * (len(password) // i) == password:
            return True
    return False

def contains_common_substitutions(password):
    substitutions = {
        '4': 'a', '@': 'a', '3': 'e', '1': 'l', '0': 'o', '$': 's', '!': 'i'
    }

    for sub, char in substitutions.items():
        if sub in password.lower() or char in password.lower():
            return True
    return False

def contains_dictionary_word(password):
    lower_password = password.lower()
    for i in range(len(lower_password)):
        for j in range(i+1, len(lower_password)+1):
            if lower_password[i:j] in word_set:
                return True
    return False

def contains_custom_patterns(password, custom_patterns):
    lower_password = password.lower()
    for pattern in custom_patterns:
        if pattern in lower_password:
            return True
    return False

def is_common_password(password, common_passwords):
    return password.lower() in common_passwords

def is_complex_pattern(password, custom_patterns, common_passwords):
    return (
        is_sequential(password) or
        is_repeated_pattern(password) or
        contains_common_substitutions(password) or
        contains_dictionary_word(password) or
        contains_custom_patterns(password, custom_patterns) or
        is_common_password(password, common_passwords)
    )

def generate_secure_password(length, include_upper, include_numbers, include_symbols, custom_patterns, common_passwords):
    pool = string.ascii_lowercase
    if include_upper:
        pool += string.ascii_uppercase
    if include_numbers:
        pool += string.digits
    if include_symbols:
        pool += string.punctuation

    max_attempts = 100000000  # Adjust the number of attempts as needed
    for attempt in range(max_attempts):
        password = ''.join(random.choice(pool) for _ in range(length))
        if not is_complex_pattern(password, custom_patterns, common_passwords):
            return password

    print("Could not generate a password meeting all criteria after 100000000 attempts.")
    return password  # Return the last attempted password (may not meet all criteria)

# Load or prompt for the common passwords file path
saved_path = load_saved_path()

if saved_path:
    print(f"Using saved path: {saved_path}")
    common_passwords = load_common_passwords(saved_path)
else:
    common_passwords_file = input("Enter the path to your common passwords file: ")
    common_passwords = load_common_passwords(common_passwords_file)
    save_path(common_passwords_file)

# Get user-defined patterns
custom_patterns = get_custom_patterns()

# User inputs
length = int(input("Enter the desired password length: "))
include_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
include_numbers = input("Include numbers? (y/n): ").lower() == 'y'
include_symbols = input("Include special characters? (y/n): ").lower() == 'y'

# Generate password
password = generate_secure_password(length, include_upper, include_numbers, include_symbols, custom_patterns, common_passwords)
print("Generated Secure Password:", password)
