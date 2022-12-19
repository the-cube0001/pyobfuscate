import random
import string
import keyword
import base64

def obfuscate(code):
    # Remove whitespace and comments
    code = ''.join([line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')])

    # Rename variables and functions
    names = {}
    for word in code.split():
        if word in names:
            continue
        if word.isidentifier() and not keyword.iskeyword(word):
            names[word] = ''.join(random.choices(string.ascii_letters, k=10))
    for old, new in names.items():
        code = code.replace(old, new)

    # Generate multiple random keys
    keys = [''.join(random.choices(string.ascii_letters + string.digits, k=10)) for _ in range(3)]

    # Encode the code with the keys
    encoded_code = code
    for key in keys:
        temp = ''
        for i, c in enumerate(encoded_code):
            temp += chr(ord(c) ^ ord(key[i % len(key)]))
        encoded_code = temp

    # Encode the encoded code in base64
    encoded_code = base64.b64encode(encoded_code.encode()).decode()

    # Wrap the encoded code in a function that decodes and executes the code
    code = f'''
import base64
def run_obfuscated_code():
    keys = {repr(keys)}
    encoded_code = {repr(encoded_code)}
    code = base64.b64decode(encoded_code).decode()
    for key in keys:
        temp = ''
        for i, c in enumerate(code):
            temp += chr(ord(c) ^ ord(key[i % len(key)]))
        code = temp
    exec(code, globals())
run_obfuscated_code()
'''

    return code

# The code that will be obfuscated
code = '''
print("hello")
'''

obfuscated_code = obfuscate(code)

# Write the obfuscated code to a separate script
with open('obfuscated_code.py', 'w') as f:
    f.write(obfuscated_code)

print("Obfuscated code has been exported to 'obfuscated_code.py'.")
