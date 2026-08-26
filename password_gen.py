import secrets
import string
import math
import subprocess
import sys

# Ensure UTF-8 console support across platforms
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

if sys.stdin.encoding != 'utf-8':
    try:
        sys.stdin.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Character Pools
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
PUNCTUATION = "!@#$%^&*()_+-=[]{}|;:,.<>?~"
EXTENDED_CHARS = "çğıöşüÇĞİÖŞÜ"

def generate_password(
    length: int = 16,
    include_upper: bool = True,
    include_lower: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    include_extended: bool = True
) -> str:
    """
    Generates a cryptographically secure password (using CSPRNG / secrets module).
    Guarantees at least one character from each enabled character pool.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters (12+ recommended for security).")

    pools = []
    guaranteed_chars = []

    if include_upper:
        pools.append(UPPERCASE)
        guaranteed_chars.append(secrets.choice(UPPERCASE))
    if include_lower:
        pools.append(LOWERCASE)
        guaranteed_chars.append(secrets.choice(LOWERCASE))
    if include_digits:
        pools.append(DIGITS)
        guaranteed_chars.append(secrets.choice(DIGITS))
    if include_symbols:
        pools.append(PUNCTUATION)
        guaranteed_chars.append(secrets.choice(PUNCTUATION))
    if include_extended:
        pools.append(EXTENDED_CHARS)
        guaranteed_chars.append(secrets.choice(EXTENDED_CHARS))

    if not pools:
        raise ValueError("At least one character pool must be selected!")

    if length < len(guaranteed_chars):
        raise ValueError(f"Password length must be at least {len(guaranteed_chars)} to include all selected character types.")

    all_characters = "".join(pools)
    remaining_length = length - len(guaranteed_chars)

    # Cryptographically random selection for remaining characters
    random_chars = [secrets.choice(all_characters) for _ in range(remaining_length)]

    # Combine and shuffle securely
    full_password_list = guaranteed_chars + random_chars
    secrets.SystemRandom().shuffle(full_password_list)

    return "".join(full_password_list)

def calculate_entropy_and_crack_time(password: str) -> dict:
    """
    Calculates password entropy in bits and estimates brute-force cracking time
    against modern high-performance GPU clusters (100 Billion guesses/sec).
    """
    charset_size = 0
    has_lower = any(c in LOWERCASE for c in password)
    has_upper = any(c in UPPERCASE for c in password)
    has_digit = any(c in DIGITS for c in password)
    has_symbol = any(c in PUNCTUATION for c in password)
    has_extended = any(c in EXTENDED_CHARS for c in password)

    if has_lower:
        charset_size += len(LOWERCASE)
    if has_upper:
        charset_size += len(UPPERCASE)
    if has_digit:
        charset_size += len(DIGITS)
    if has_symbol:
        charset_size += len(PUNCTUATION)
    if has_extended:
        charset_size += len(EXTENDED_CHARS)

    length = len(password)
    total_combinations = charset_size ** length if charset_size > 0 else 0
    entropy_bits = length * math.log2(charset_size) if charset_size > 0 else 0

    # Modern attacker capacity: 100 Billion guesses/sec (10^11/s - GPU cluster)
    guesses_per_sec = 10**11
    seconds = (total_combinations / 2) / guesses_per_sec if guesses_per_sec > 0 else 0

    return {
        "entropy_bits": round(entropy_bits, 2),
        "charset_size": charset_size,
        "total_combinations": total_combinations,
        "time_str": format_duration(seconds)
    }

def format_duration(seconds: float) -> str:
    if seconds < 0.001:
        return "Instant (< 1 millisecond)"
    elif seconds < 1:
        return f"{seconds*1000:.1f} milliseconds"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"
    elif seconds < 31536000 * 100:
        return f"{seconds/31536000:.1f} years"
    elif seconds < 31536000 * 10**6:
        return f"{seconds/31536000:.1e} years (Millions of years)"
    else:
        return f"{seconds/31536000:.2e} years (Longer than the age of the Universe!)"

def copy_to_clipboard(text: str) -> bool:
    try:
        if sys.platform == "win32":
            subprocess.run("clip", input=text.encode("utf-16"), check=True, shell=True)
            return True
    except Exception:
        pass
    return False

def interactive_cli():
    print("=" * 65)
    print("  🛡️  BRUTE-FORCE RESISTANT SECURE PASSWORD GENERATOR 🛡️")
    print("=" * 65)
    print("• Cryptographic Randomness: Python 'secrets' module (CSPRNG)")
    print("• Supported: Uppercase, Lowercase, Digits, Symbols, Extended Unicode")
    print("-" * 65)

    while True:
        try:
            val = input("\nEnter password length (e.g. 10, 16, 24) ['q' to exit]: ").strip()
            if val.lower() == 'q':
                print("Exiting...")
                break

            length = int(val)
            if length < 6:
                print("⚠️  Warning: Passwords shorter than 6 characters are weak against brute-force. 12-16+ recommended.")

            count_val = input("How many passwords to generate? [Default: 1]: ").strip()
            count = int(count_val) if count_val.isdigit() and int(count_val) > 0 else 1

            ext_val = input("Include extended/Turkish characters? (ç, ğ, ı, ö, ş, ü...) [Y/n]: ").strip().lower()
            include_ext = False if ext_val == 'n' else True

            print("\n" + "-" * 65)
            last_pwd = ""
            for i in range(count):
                pwd = generate_password(length=length, include_extended=include_ext)
                last_pwd = pwd
                analysis = calculate_entropy_and_crack_time(pwd)

                print(f"🔑 Password #{i+1} : {pwd}")
                print(f"   📊 Entropy       : {analysis['entropy_bits']} bits (Pool: {analysis['charset_size']} unique chars)")
                print(f"   ⏳ Crack Time    : ~{analysis['time_str']} (at 100 Billion guesses/sec)")
                print("-" * 65)

            if count == 1 and last_pwd:
                if copy_to_clipboard(last_pwd):
                    print("📋 Password copied to clipboard automatically!")
        except ValueError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        length = int(sys.argv[1])
        include_ext = "--no-ext" not in sys.argv
        pwd = generate_password(length=length, include_extended=include_ext)
        analysis = calculate_entropy_and_crack_time(pwd)
        print(f"Password: {pwd}")
        print(f"Entropy: {analysis['entropy_bits']} bits | Estimated Crack Time: {analysis['time_str']}")
    else:
        interactive_cli()
