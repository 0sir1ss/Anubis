# Made by 0sir1ss @ https://github.com/0sir1ss/Anubis
import ast, io, tokenize, os, sys, platform, re, random, string, base64, hashlib, subprocess, requests
from regex import F
from Crypto import Random
from Crypto.Cipher import AES

is_windows = True if platform.system() == "Windows" else False

if is_windows:
    os.system("title Anubis @ github.com/0sir1ss/Anubis")

def clear():
    if is_windows:
        os.system("cls")
    else:
        os.system("clear")

def pause():
    if is_windows:
        os.system(f"pause >nul")
    else:
        input()

def leave():
    try:
        sys.exit()
    except:
        exit()

def error(error):
    print(red(f"        [!] Error : {error}"), end="")
    pause(); clear(); leave()

def red(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 250
        for character in line:
            green -= 5
            if green < 0:
                green = 0
            faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
        faded += "\n"
    return faded

def blue(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 0
        for character in line:
            green += 3
            if green > 255:
                green = 255
            faded += (f"\033[38;2;0;{green};255m{character}\033[0m")
        faded += "\n"
    return faded

def water(text):
    os.system(""); faded = ""
    green = 10
    for line in text.splitlines():
        faded += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return faded

def purple(text):
    os.system("")
    faded = ""
    down = False

    for line in text.splitlines():
        red = 40
        for character in line:
            if down:
                red -= 3
            else:
                red += 3
            if red > 254:
                red = 255
                down = True
            elif red < 1:
                red = 30
                down = False
            faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
    return faded

def remove_docs(source):
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    out = '\n'.join(l for l in out.splitlines() if l.strip())
    return out

def do_rename(pairs, code):
    for key in pairs:
        code = re.sub(fr"\b({key})\b", pairs[key], code, re.MULTILINE)
    return code

def carbon(code):
    code = remove_docs(code)
    parsed = ast.parse(code)

    funcs = {
        node for node in ast.walk(parsed) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    classes = {
        node for node in ast.walk(parsed) if isinstance(node, ast.ClassDef)
    }
    args = {
        node.id for node in ast.walk(parsed) if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load)
    }
    attrs = {
        node.attr for node in ast.walk(parsed) if isinstance(node, ast.Attribute) and not isinstance(node.ctx, ast.Load)
    }
    for func in funcs:
        if func.args.args:
            for arg in func.args.args:
                args.add(arg.arg)
        if func.args.kwonlyargs:
            for arg in func.args.kwonlyargs:
                args.add(arg.arg)
        if func.args.vararg:
            args.add(func.args.vararg.arg)
        if func.args.kwarg:
            args.add(func.args.kwarg.arg)

    pairs = {}
    used = set()
    for func in funcs:
        if func.name == "__init__":
            continue
        newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        while newname in used:
            newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        used.add(newname)
        pairs[func.name] = newname

    for _class in classes:
        newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        while newname in used:
            newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        used.add(newname)
        pairs[_class.name] = newname

    for arg in args:
        newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        while newname in used:
            newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        used.add(newname)
        pairs[arg] = newname

    for attr in attrs:
        newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        while newname in used:
            newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        used.add(newname)
        pairs[attr] = newname

    string_regex = r"('|\")[\x1f-\x7e]{1,}?('|\")"

    original_strings = re.finditer(string_regex, code, re.MULTILINE)
    originals = []

    for matchNum, match in enumerate(original_strings, start=1):
        originals.append(match.group().replace("\\", "\\\\"))

    placeholder = os.urandom(16).hex()
    code = re.sub(string_regex, f"'{placeholder}'", code, 0, re.MULTILINE)

    for i in range(len(originals)):
        for key in pairs:
            originals[i] = re.sub(r"({.*)(" + key + r")(.*})", "\\1" + pairs[key] + "\\3", originals[i], re.MULTILINE)

    cycles = [
        "[   > >                                                                                           ]", 
        "[   > > > >                                                                                       ]", 
        "[   > > > > > >                                                                                   ]", 
        "[   > > > > > > > >                                                                               ]", 
        "[   > > > > > > > > > >                                                                           ]", 
        "[   > > > > > > > > > > > >                                                                       ]", 
        "[   > > > > > > > > > > > > > >                                                                   ]", 
        "[   > > > > > > > > > > > > > > > >                                                               ]", 
        "[   > > > > > > > > > > > > > > > > > >                                                           ]", 
        "[   > > > > > > > > > > > > > > > > > > > >                                                       ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > >                                                   ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > >                                               ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > >                                           ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > >                                       ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >                                   ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >                               ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >                           ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >                       ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >                   ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >               ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >           ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >       ]", 
        "[   > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >   ]", 
    ]

    i = int(0)

    while True:
        print("\r"+f"        {cycles[i]}", end="")
        i += 1
        if i == len(cycles):
            i = int(0)
        found = False
        code = do_rename(pairs, code)
        for key in pairs:
            if re.findall(fr"\b({key})\b", code):
                found = True
        if found == False:
            break

    replace_placeholder = r"('|\")" + placeholder + r"('|\")"
    for original in originals:
        code = re.sub(replace_placeholder, original, code, 1, re.MULTILINE)
    print("\r"+f"        {cycles[len(cycles) -1]}\n\n", end="")

    return code

def oxyry(code):
    try:
        src = '__all__ = []\n' + code.replace('"', '\"').replace("'", "\'").replace("\\", "\\\\")
        url = "https://pyob.oxyry.com/obfuscate"
        payload = {
            "append_source": False,
            "remove_docstrings": True,
            "rename_nondefault_parameters": True,
            "rename_default_parameters": True,
            "preserve": "",
            "source": src
        }
        r = requests.post(url, headers={}, json=payload)
        data = r.json()
        try:
            code = data['dest'].replace("\\\\", "\\")
            code = re.sub("#\w*:[0-9]*", "", code)
            code = code.replace(f'__all__=[]\n', "").replace(f'__all__ =[]\n', "").replace(f'__all__ = []\n', "").replace(f'__all__= []\n', "")
            return code
        except:
            error(f"{data['errorMessage']}\n        [!] Please make sure your code is Python 3.3 - 3.7 compatible")
    except:
        error("A problem occurred whilst obfuscating")

def bugs(code):
    dbg = """import ctypes, sys
if not ctypes.windll.shell32.IsUserAnAdmin() != 0:
    print("Please run this program as administrator.")
    sys.exit(0)
import binascii, threading, time
try:
    from psutil import process_iter
except:
    import os
    os.system("pip install psutil")
d = [
    '53757370656e64', '50726f67726573732054656c6572696b20466964646c657220576562204465627567676572', '466964646c6572', '57697265736861726b',
    '64756d70636170', '646e537079', '646e5370792d783836', '6368656174656e67696e652d7838365f3634', '4854545044656275676765725549',
    '50726f636d6f6e', '50726f636d6f6e3634', '50726f636d6f6e363461', '50726f636573734861636b6572',
    '783332646267', '783634646267', '446f744e657444617461436f6c6c6563746f723332',
    '446f744e657444617461436f6c6c6563746f723634', '485454504465627567676572537663', '48545450204465627567676572', '696461', '6964613634', '69646167', '696461673634',
    '69646177', '696461773634', '69646171', '696461713634', '69646175', '696461753634',
    '7363796c6c61', '7363796c6c615f783634', '7363796c6c615f783836', '70726f74656374696f6e5f6964',
    '77696e646267', '7265736861636b6572', '496d706f7274524543', '494d4d554e4954594445425547474552',
    '4d65676144756d706572', '646973617373656d626c79', '4465627567', '5b435055496d6d756e697479',
    '4d65676144756d70657220312e3020627920436f6465437261636b6572202f20536e44', '436861726c6573', '636861726c6573', '4f4c4c59444247', '496d706f72745f7265636f6e7374727563746f72',
    '636f6465637261636b6572', '646534646f74', '696c737079', '67726179776f6c66',
    '73696d706c65617373656d626c796578706c6f726572', '7836346e657464756d706572', '687864',
    '7065746f6f6c73', '73696d706c65617373656d626c79', '68747470616e616c797a6572', '687474706465627567', '70726f636573736861636b6572', '6d656d6f727965646974', '6d656d6f7279',
    '646534646f746d6f64646564', '70726f63657373206861636b6572', '70726f63657373206d6f6e69746f72',
    '717435636f7265', '696461', '696d6d756e697479', '68747470', '74726166666963',
    '77697265736861726b', '666964646c6572', '7061636b6574', '6861636b6572', '6465627567', '646e737079', '646f747065656b', '646f747472616365', '70726f6364756d70', '6d616e61676572',
    '6d656d6f7279', '6e65744c696d6974', '6e65744c696d69746572', '73616e64626f78'
]
d = [binascii.unhexlify(i.encode()).decode() for i in d]
def debugger():
    while True:
        try:
            for proc in process_iter():
                for i in d:
                    if i.lower() in proc.name().lower():
                        proc.kill()
        except Exception:
            pass
        time.sleep(0.5)
threading.Thread(target=debugger, daemon=True).start()\n\n"""
    code = dbg + code
    return code

def anubis(code):
    newcode = "\n"
    classes = ["".join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(random.randint(8, 20))) for i in range(random.randint(2, 5))]
    for i in classes:
        newcode += f"class {i}:\n    def __init__(self):\n"
        funcs = ["__"+"".join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(random.randint(8, 20))) for i in range(random.randint(5, 15))]
        for i in funcs:
            newcode += f"        self.{i}()\n"
        for i in funcs:
            newcode += f"    def {i}(self, {', '.join([''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(random.randint(5, 20))) for i in range(random.randint(1, 7))])}):\n        return self.{random.choice(funcs)}()\n"
    newcode += code + "\n"
    classes = ["".join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(random.randint(8, 20))) for i in range(random.randint(2, 5))]
    for i in classes:
        newcode += f"class {i}:\n    def __init__(self):\n"
        funcs = ["__"+"".join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(random.randint(8, 20))) for i in range(random.randint(5, 15))]
        for i in funcs:
            newcode += f"        self.{i}()\n"
        for i in funcs:
            newcode += f"    def {i}(self, {', '.join([''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(random.randint(5, 20))) for i in range(random.randint(1, 7))])}):\n        return self.{random.choice(funcs)}()\n"
    return newcode

class Encryption:

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw):
        raw = self._pad(str(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode()

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)


    def write(self, key, source):
        wall = "__ANUBIS_ENCRYPTED__" * 25
        newcode = f"{wall}{key}{wall}"
        for line in source.split("\n"):
            newcode += self.encrypt(line) + wall
        code = f"import ancrypt\nancrypt.load(__file__)\n'''\n{newcode}\n'''"
        return code


banner = f"""



                                  /$$$$$$  /$$   /$$ /$$   /$$ /$$$$$$$  /$$$$$$  /$$$$$$ 
                                 /$$__  $$| $$$ | $$| $$  | $$| $$__  $$|_  $$_/ /$$__  $$
                                | $$  \ $$| $$$$| $$| $$  | $$| $$  \ $$  | $$  | $$  \__/
                                | $$$$$$$$| $$ $$ $$| $$  | $$| $$$$$$$   | $$  |  $$$$$$ 
                                | $$__  $$| $$  $$$$| $$  | $$| $$__  $$  | $$   \____  $$
                                | $$  | $$| $$\  $$$| $$  | $$| $$  \ $$  | $$   /$$  \ $$
                                | $$  | $$| $$ \  $$|  $$$$$$/| $$$$$$$/ /$$$$$$|  $$$$$$/
                                |__/  |__/|__/  \__/ \______/ |_______/ |______/ \______/ 



        {purple(f"[>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")}
        
"""

clear()
print(water(banner), end="")
while True:
    file = input(purple("        [>] Enter the python file you wish to obfuscate [script.py] : ") + "\033[38;2;148;0;230m")
    if not os.path.exists(file):
        print(red("        [!] Error : That file does not exist"), end="")
    else:
        break

carbonate = False
oxy = False
junk = False
bug = False

while True:
    ans = input(purple("        [>] AntiDebug [y/n] : ") + "\033[38;2;148;0;230m").lower()
    if ans == "y":
        bug = True
        break
    elif ans == "n":
        bug = False
        break
    else:
        print(red(f"        [!] Error : Invalid option [y/n]"), end="")
    
while True:
    ans = input(purple("        [>] Junk Code [y/n] : ") + "\033[38;2;148;0;230m").lower()
    if ans == "y":
        junk = True
        break
    elif ans == "n":
        junk = False
        break
    else:
        print(red(f"        [!] Error : Invalid option [y/n]"), end="")

while True:
    ans = input(purple("        [>] Rename Classes, Functions, Variables & Parameters [y/n] : ") + "\033[38;2;148;0;230m").lower()
    if ans == "y":
        rename = True
        break
    elif ans == "n":
        rename = False
        break
    else:
        print(red(f"        [!] Error : Invalid option [y/n]"), end="")

if rename:
    while True:
        ans = input(purple("        [>] Carbon (Offline) or Oxyry [c/o] : ") + "\033[38;2;148;0;230m").lower()
        if ans == "c":
            carbonate = True
            break
        elif ans == "o":
            oxy = True
            break
        else:
            print(red(f"        [!] Error : Invalid option [c/o]"), end="")


while True:
    ans = input(purple("        [>] One Line Obfuscation (Can't compile to exe) [y/n] : ") + "\033[38;2;148;0;230m").lower()
    if ans == "y":
        extra = True
        break
    elif ans == "n":
        extra = False
        break
    else:
        print(red(f"        [!] Error : Invalid option [y/n]"), end="")

print(" ")
key = base64.b64encode(os.urandom(32)).decode()
with open(file, "r", encoding='utf-8') as f:
    src = f.read()

if junk:
    src = anubis(src)
if bug:
    src = bugs(src)
if junk:
    src = anubis(src)
if carbonate:
    src = carbon(src)
if oxy:
    src = oxyry(src)
if extra:
    src = Encryption(key.encode()).write(key, src)


name = f"{file[:-3]}-obf.py"
with open(name, "w", encoding='utf-8') as f:
    f.write(src)

print(blue(f"        [>] Code has been successfully obfuscated @ {name}"), end="")

if extra == False:
    compile = False
    while True:
        ans = input(purple("        [>] Would you like to compile to an exe [y/n] : ") + "\033[38;2;148;0;230m").lower()
        if ans == "y":
            compile = True
            break
        elif ans == "n":
            compile = False
            break
        else:
            print(red(f"        [!] Error : Invalid option [y/n]"), end="")

    if compile == True:
        basic_params = ["nuitka", "--mingw64", "--onefile", "--enable-plugin=numpy", "--include-module=psutil", "--remove-output", "--assume-yes-for-downloads", name]
        p = subprocess.Popen(basic_params, stdout=subprocess.DEVNULL, shell=True, cwd=os.getcwd())
        print(red("\n        [!] Exe may take a while to compile\n        [!] Nuitka Information:\n\n"), end="")
        p.wait()
        print(blue(f"\n        [>] Code has been successfully compiled @ {name[:-3] + '.exe'}"), end="")

print(blue("\n        [>] Press any key to exit... "), end="")
pause(); clear(); leave()
