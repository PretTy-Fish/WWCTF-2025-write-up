# Domain of Doom write-up (WWCTF 2025)

**Name:** Domain of Doom

**Description:** You're querying domains, but some lead to dangerous places
- The flag is hidden in an environment variable.

**Type:** Web Exploitation

**Difficulty:** ~Medium~ Easy

**Points:** 100

**Author:** dxler

**Files:** [Domain_of_Doom.zip (unzipped)](/Domain%20of%20Doom/Domain%20of%20Doom)

## Analysis

Have a look at [app.py](/Domain%20of%20Doom/Domain%20of%20Doom/code/app.py):
```python
@app.route('/flag')
def flag():
    flag = os.environ.get('FLAG', 'WWF{placeholder_flag}')
    return render_template('index.html', flag=flag)
```
...wut?

## Solution

Visit `https://instance_hash_here.chall.wwctf.com/flag`:
![flag.png](/Domain%20of%20Doom/flag.png)
**Flag:** `wwf{CommAnd_lnj3cti0n_1s_c0ol}`

---
<details>
<summary>Afterthought</summary>

![annoucement.png](/Domain%20of%20Doom/annoucement.png)

For a proper solution, check out other's Domain of Doom Revenge write-ups.

</details>
