# Based 64 write-up (WWCTF 2025)

**Name:** Based 64

**Description:** My friend told me there are some interesting properties of base64...

**Type:** Cryptography

**Difficulty:** Beginner

**Points:** 100

**Author:** 

**Files:** [based64.txt](/Based%2064/based64.txt)

## Analysis

Opened up the text file and found lines of very short base64 strings, presumably each encodes one character, so I threw them into [CyberChef](https://gchq.github.io/CyberChef/) and got:
```
SORRY THERE IS NO FLAG TO BE FOUND HERE. PLEASE DO NOT CONTINUE LOOKING.
```
A quick google on "base64 interesting properties" gives https://stackoverflow.com/questions/30429168/is-a-base64-encoded-string-unique, where the answer says:
> **multiple base64 encoded strings may represent a single binary/hex value.**

I checked the text file again and indeed found something peculiar: the `R`s in the first and second words are encoded to `Un==` and `Ul==` respectively. This hinted that something is hiding in the padding.

The [Wikipedia page](https://en.wikipedia.org/wiki/Base64#Examples) shows that for a single character, the last 4 bits of the second encoded sextet are the padded part, so I quickly launched up Python and got to work:
```python
>>> alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
>>> pads = []
>>> with open("based64.txt") as f:
...     for line in f.readlines()[:-1]:
...         pads.append(alphabet.index(line[1]) % 16)
...
>>> pads
[7, 7, 7, 7, 6, 6, 7, 11, 7, 5, 6, 14, 5, 5, 7, 3, 3, 3, 6, 4, 5, 15, 6, 2, 3, 1, 7, 4, 7, 3, 5, 15, 3, 3, 7, 1, 7, 5, 3, 4, 6, 12, 7, 10, 5, 15, 7, 3, 7, 4, 3, 3, 6, 7, 3, 0, 5, 15, 6, 6, 7, 5, 6, 14, 7, 13, 0, 0, 0, 0]
```
The last line is ignored as it encodes the last two characters `G.`. It is also consistent with the direct encoding of `G.`, showing that its padding is 0. This is like the last few lines, so we can assume they all contain no interesting information.

The 4-bit segments must combine pairwise to give meaningful ASCII characters. To be extra certain, I also checked the endian: Since the numbers in the tens all appear second in each pair, the first of each pair must be the high 4 bits. The message can then be decoded:
```python
>>> ''.join([chr(pads[2*n] * 16 + pads[2*n+1]) for n in range(len(pads)//2)])
'wwf{unUs3d_b1ts_3qu4lz_st3g0_fun}\x00\x00'
```

## Solution

The full Python code is then:
```python
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
pads = []
with open("based64.txt") as f:
    for line in f.readlines()[:-1]:
        pads.append(alphabet.index(line[1]) % 16)
flag = ''.join([chr(pads[2*n] * 16 + pads[2*n+1]) for n in range(len(pads)//2)])
print(flag)
```
**Flag:** `wwf{unUs3d_b1ts_3qu4lz_st3g0_fun}`
