# 🛡️ Cryptographically Secure Brute-Force Resistant Password Generator

A high-entropy, brute-force-resistant password generator written in Python and vanilla HTML/JavaScript. Built with industry-standard Cryptographically Secure Pseudo-Random Number Generators (**CSPRNG**), ensuring mathematical unpredictability and extreme resistance to modern GPU-based cracking attacks.

---

## ✨ Features

- **🔐 Cryptographically Secure:** Uses Python's `secrets` module and the Web Crypto API (`window.crypto.getRandomValues`) instead of predictable pseudo-random engines like `random`.
- **💥 Extreme Character Pool Diversity:**
  - Uppercase letters (`A-Z`)
  - Lowercase letters (`a-z`)
  - Digits (`0-9`)
  - Special symbols (`!@#$%^&*()_+-=[]{}|;:,.<>?~`)
  - Extended unicode / Turkish characters (`ç, ğ, ı, ö, ş, ü, Ç, Ğ, İ, Ö, Ş, Ü`)
- **🎯 Guaranteed Complexity:** Ensures that at least one character from every active character pool is included in the output, then securely shuffled using Fisher-Yates.
- **📊 Real-time Entropy & Brute-Force Analysis:**
  - Calculates information entropy in **bits** ($E = L \times \log_2(N)$).
  - Estimates cracking time against extreme attack hardware ($10^{11}$ guesses/sec — modern supercomputers / high-end GPU clusters).
- **📋 Auto Clipboard Copy:** Instantly copies generated passwords to the clipboard on Windows and modern browsers.
- **🌐 Dual Interface:** Ready-to-use Command Line Interface (CLI) + standalone sleek single-file Web UI (`index.html`).

---

## 📁 Project Structure

```
password_generator/
├── password_gen.py      # Python CLI password generator with entropy analysis
├── index.html           # Standalone responsive Web GUI (Zero dependencies)
└── README.md            # Documentation and usage guide
```

---

## 🚀 Quick Start & Usage

### 1. Command Line Interface (Python)

#### Prerequisites
Python 3.8 or higher is required. No external libraries needed (uses standard library modules: `secrets`, `string`, `math`, `subprocess`).

#### Quick Generation (Argument Mode)
Specify the desired length directly as a parameter:

```bash
# Generate a 10-character password
python password_gen.py 10
```

**Example Output:**
```text
Password: ?AW3]üDk($
Entropy: 66.58 bits | Estimated Crack Time: ~17.5 years
```

```bash
# Generate a 16-character password (recommended)
python password_gen.py 16
```

**Example Output:**
```text
Password: PV%~ME40~|jıçiOC
Entropy: 106.53 bits | Estimated Crack Time: ~1.86e+13 years (Longer than the age of the Universe!)
```

#### Interactive CLI Mode
Run without arguments to enter interactive mode:

```bash
python password_gen.py
```

```text
=================================================================
  🛡️  BRUTE-FORCE RESISTANT SECURE PASSWORD GENERATOR 🛡️
=================================================================
• Cryptographic Randomness: Python 'secrets' module (CSPRNG)
• Supported: Uppercase, Lowercase, Digits, Symbols, Extended Unicode
-----------------------------------------------------------------

Enter password length (e.g. 10, 16, 24) ['q' to exit]: 16
How many passwords to generate? [Default: 1]: 3
Include extended/Turkish characters? (ç, ğ, ı, ö, ş, ü...) [Y/n]: y

-----------------------------------------------------------------
🔑 Password #1 : 9!hüG$0dIĞp=7.LÖ
   📊 Entropy       : 106.53 bits (Pool: 101 unique chars)
   ⏳ Crack Time    : ~1.86e+13 years (at 100 Billion guesses/sec)
-----------------------------------------------------------------
🔑 Password #2 : şY8?xZ(m!K6#ü.D9
   📊 Entropy       : 106.53 bits (Pool: 101 unique chars)
   ⏳ Crack Time    : ~1.86e+13 years (at 100 Billion guesses/sec)
-----------------------------------------------------------------
🔑 Password #3 : c+Ğ2M@1p_ü5~Xo$W
   📊 Entropy       : 106.53 bits (Pool: 101 unique chars)
   ⏳ Crack Time    : ~1.86e+13 years (at 100 Billion guesses/sec)
-----------------------------------------------------------------
```

---

### 2. Graphical Web Interface (Browser)

Simply double-click `index.html` or open it with any web browser:

- Real-time length slider (6 to 64 characters).
- Checkboxes to toggle uppercase, lowercase, numbers, symbols, and extended characters.
- Live entropy calculation and crack time estimator with color-coded strength bar.
- One-click copy with toast notification.

---

## 🔒 Security & Mathematical Background

### Why is Brute-Force Ineffective?

Brute-force attacks search the entire password space $S = N^L$, where:
- $N$ = Character pool size (up to $101$ with all sets enabled)
- $L$ = Password length

| Length ($L$) | Pool Size ($N$) | Total Combinations ($N^L$) | Entropy (Bits) | Avg. Crack Time ($10^{11}\text{ guesses/sec}$) |
|:---:|:---:|:---:|:---:|:---:|
| **8** | 101 | $\approx 1.08 \times 10^{16}$ | 53.2 bits | **~15 hours** |
| **10** | 101 | $\approx 1.10 \times 10^{20}$ | 66.5 bits | **~17.5 years** |
| **12** | 101 | $\approx 1.12 \times 10^{24}$ | 79.9 bits | **~178,000 years** |
| **16** | 101 | $\approx 1.17 \times 10^{32}$ | 106.5 bits | **$\approx 1.8 \times 10^{13}$ years** |

> ℹ️ **Note:** The age of the observable universe is approximately $1.38 \times 10^{10}$ years. A 16-character password generated by this tool would take over **1,300 times the age of the universe** to crack using a modern supercomputing cluster.

---

## 📜 License

This project is licensed under the MIT License — feel free to use and adapt it for personal or production security workflows.
