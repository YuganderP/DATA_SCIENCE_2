# API Endpoint Fuzzer

## Project Overview

This project is a simple **API endpoint fuzzer** built using Python.

The script:
- Reads words from standard input
- Appends them to a base API URL
- Sends HTTP GET requests
- Checks whether the endpoint exists
- Prints successful responses

It helps discover:
- Valid API endpoints
- Hidden routes
- Accessible resources

---

# Project Flow

```text
Input Words → Build URL → Send Request → Check Status → Print Valid Response
```

Example:

Input:

```text
posts
users
admin
todos
```

Generated URLs:

```text
https://jsonplaceholder.typicode.com/posts
https://jsonplaceholder.typicode.com/users
https://jsonplaceholder.typicode.com/admin
https://jsonplaceholder.typicode.com/todos
```

---

# Source Code

```python
import requests
import sys
import random

count = 0

for word in sys.stdin:

    word = word.strip()

    sample = f"https://jsonplaceholder.typicode.com/{word}"

    res = requests.get(url=sample)

    data = res

    if(res.status_code == 200):

        print(data)

        print(res.text)
```

---

# Modules Used

| Module | Purpose |
|---|---|
| `requests` | Send HTTP requests |
| `sys` | Read input from terminal/stdin |
| `random` | Imported but not used |

---

# How the Code Works

## 1. Read Input

```python
for word in sys.stdin:
```

Reads endpoint names line by line from terminal input.

Example:

```text
posts
users
comments
```

---

## 2. Remove Extra Spaces

```python
word = word.strip()
```

Removes:
- Newline characters
- Extra spaces

---

## 3. Build API URL

```python
sample = f"https://jsonplaceholder.typicode.com/{word}"
```

Creates endpoint URLs dynamically.

Example:

```python
word = "posts"
```

Result:

```text
https://jsonplaceholder.typicode.com/posts
```

---

## 4. Send HTTP Request

```python
res = requests.get(url=sample)
```

Sends GET request to API.

---

## 5. Check Response Status

```python
if(res.status_code == 200):
```

Checks whether endpoint exists successfully.

`200` means:
- Request succeeded
- Valid endpoint found

---

## 6. Print Response

```python
print(data)
print(res.text)
```

Displays:
- Response object
- API response body

---

# Example Usage

## Input File (`wordlist.txt`)

```text
posts
users
todos
invalid
```

---

## Run Command

```bash
python fuzzer.py < wordlist.txt
```

---

## Sample Output

```text
<Response [200]>
[
  {
    "userId": 1,
    "id": 1,
    "title": "...",
    "body": "..."
  }
]
```

---

# Improvements You Can Add

## 1. Handle Errors

```python
try:
    res = requests.get(sample)
except:
    print("Connection Error")
```

---

## 2. Add Timeout

```python
requests.get(sample, timeout=5)
```

---

## 3. Save Results to File

```python
with open("results.txt", "a") as f:
    f.write(sample + "\n")
```

---

## 4. Show Only Valid Endpoints

```python
print(f"[+] Found: {sample}")
```

---

## 5. Use Multithreading

Makes fuzzing faster.

Libraries:
- `threading`
- `concurrent.futures`

---

# Limitations

- Only supports GET requests
- No concurrency
- No authentication support
- No rate limiting handling
- No response filtering

---

# Educational Purpose

This project helps learn:
- APIs
- HTTP requests
- Status codes
- Automation
- Cybersecurity basics
- Endpoint enumeration

---

# Example Improved Version

```python
import requests
import sys

for word in sys.stdin:

    word = word.strip()

    url = f"https://jsonplaceholder.typicode.com/{word}"

    try:

        res = requests.get(url, timeout=5)

        if res.status_code == 200:

            print(f"[+] Valid Endpoint Found: {url}")

        else:

            print(f"[-] Invalid: {url}")

    except requests.exceptions.RequestException:

        print(f"[!] Error accessing {url}")
```

---

# Conclusion

This project is a beginner-friendly API fuzzing tool that demonstrates:
- Dynamic URL generation
- HTTP request handling
- Endpoint discovery
- Basic fuzz testing concepts

It is useful for:
- Learning APIs
- Practicing Python automation
- Introductory security testing concepts