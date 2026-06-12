"""
Frequency Analysis Attack on Monoalphabetic Substitution Cipher

This script demonstrates how to break a monoalphabetic substitution cipher
by analyzing letter frequency distribution in the ciphertext and comparing
it to standard English letter frequencies.

Usage:
    python freq_attack.py
    python freq_attack.py --ciphertext "YOUR CIPHERTEXT HERE"
    python freq_attack.py --file ciphertext.txt
"""

import argparse
import string
from collections import Counter

# Standard English letter frequencies (in percentage)
ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.49,
    'V': 0.98, 'K': 0.077, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07,
}

# Common English bigrams
COMMON_BIGRAMS = [
    'TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND',
    'TI', 'ES', 'OR', 'TE', 'OF', 'ED', 'IS', 'IT', 'AL', 'AR',
]

# Common English trigrams
COMMON_TRIGRAMS = [
    'THE', 'AND', 'ING', 'HER', 'HAT', 'HIS', 'THA', 'ERE',
    'FOR', 'ENT', 'ION', 'TER', 'WAS', 'YOU', 'ITH', 'GHT',
]


def create_sample_ciphertext():
    """Create a sample ciphertext using a random substitution."""
    # A known substitution mapping for demonstration
    # Plain:  ABCDEFGHIJKLMNOPQRSTUVWXYZ
    # Cipher: QWERTYUIOPASDFGHJKLZXCVBNM
    mapping = str.maketrans(
        string.ascii_uppercase,
        'QWERTYUIOPASDFGHJKLZXCVBNM'
    )

    plaintext = (
        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. "
        "CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES FOR "
        "SECURE COMMUNICATION IN THE PRESENCE OF ADVERSARIES. "
        "MODERN CRYPTOGRAPHY EXISTS AT THE INTERSECTION OF THE "
        "DISCIPLINES OF MATHEMATICS COMPUTER SCIENCE AND ELECTRICAL "
        "ENGINEERING. APPLICATIONS INCLUDE ELECTRONIC COMMERCE "
        "CHIP-BASED PAYMENT CARDS DIGITAL CURRENCIES AND COMPUTER "
        "PASSWORDS. THE FIELD OF CRYPTOGRAPHY INCLUDES ENCRYPTION "
        "WHICH PROTECTS THE CONFIDENTIALITY OF DATA AND DIGITAL "
        "SIGNATURES WHICH AUTHENTICATE THE IDENTITY OF USERS."
    )

    ciphertext = plaintext.upper().translate(mapping)
    return ciphertext, mapping


def count_frequencies(text):
    """Count letter frequencies in text."""
    letters = [c for c in text.upper() if c.isalpha()]
    total = len(letters)
    freq = Counter(letters)

    # Convert to percentages
    freq_pct = {}
    for letter in string.ascii_uppercase:
        count = freq.get(letter, 0)
        freq_pct[letter] = (count / total * 100) if total > 0 else 0

    return freq_pct, freq, total


def display_frequencies(title, freq_pct, bar_width=40):
    """Display letter frequencies with visual bars."""
    print(f"\n--- {title} ---")
    max_freq = max(freq_pct.values()) if freq_pct else 1
    for letter in sorted(freq_pct, key=freq_pct.get, reverse=True):
        pct = freq_pct[letter]
        if pct > 0:
            bar_len = int(pct / max_freq * bar_width)
            bar = '\u2588' * bar_len
            print(f"  {letter}: {pct:6.2f}%  {bar}")


def bigram_analysis(text, top_n=15):
    """Perform bigram frequency analysis."""
    letters = ''.join(c for c in text.upper() if c.isalpha())
    bigrams = [letters[i:i+2] for i in range(len(letters) - 1)]
    freq = Counter(bigrams)
    total = sum(freq.values())

    print(f"\n--- Top {top_n} Bigrams in Ciphertext ---")
    for bigram, count in freq.most_common(top_n):
        pct = count / total * 100 if total > 0 else 0
        print(f"  {bigram}: {count:4d} ({pct:.2f}%)")


def trigram_analysis(text, top_n=10):
    """Perform trigram frequency analysis."""
    letters = ''.join(c for c in text.upper() if c.isalpha())
    trigrams = [letters[i:i+3] for i in range(len(letters) - 2)]
    freq = Counter(trigrams)
    total = sum(freq.values())

    print(f"\n--- Top {top_n} Trigrams in Ciphertext ---")
    for trigram, count in freq.most_common(top_n):
        pct = count / total * 100 if total > 0 else 0
        print(f"  {trigram}: {count:4d} ({pct:.2f}%)")


def propose_mapping(cipher_freq, english_freq):
    """Propose a substitution mapping based on frequency comparison."""
    # Sort cipher letters by frequency (descending)
    cipher_sorted = sorted(cipher_freq, key=cipher_freq.get, reverse=True)
    # Sort English letters by frequency (descending)
    english_sorted = sorted(english_freq, key=english_freq.get, reverse=True)

    mapping = {}
    for i, cipher_letter in enumerate(cipher_sorted):
        if i < len(english_sorted):
            mapping[cipher_letter] = english_sorted[i]

    return mapping


def decrypt_with_mapping(ciphertext, mapping):
    """Decrypt ciphertext using the proposed mapping."""
    result = []
    for c in ciphertext:
        if c.upper() in mapping:
            decrypted = mapping[c.upper()]
            if c.islower():
                decrypted = decrypted.lower()
            result.append(decrypted)
        else:
            result.append(c)
    return ''.join(result)


def calculate_accuracy(decrypted, known_plaintext):
    """Calculate decryption accuracy by comparing with known plaintext."""
    dec_letters = [c for c in decrypted.upper() if c.isalpha()]
    plain_letters = [c for c in known_plaintext.upper() if c.isalpha()]

    if len(plain_letters) == 0:
        return 0.0

    min_len = min(len(dec_letters), len(plain_letters))
    correct = sum(1 for i in range(min_len) if dec_letters[i] == plain_letters[i])

    return correct / len(plain_letters) * 100


def interactive_refinement(ciphertext, mapping):
    """Allow interactive refinement of the mapping."""
    print("\n--- Interactive Refinement ---")
    print("Current mapping:")
    for cipher, plain in sorted(mapping.items()):
        print(f"  {cipher} -> {plain}")

    print("\nDecrypted text:")
    decrypted = decrypt_with_mapping(ciphertext, mapping)
    print(f"  {decrypted[:80]}...")

    print("\nYou can refine the mapping by swapping letters.")
    print("Enter 'done' to finish, or 'XY' to swap X and Y in the mapping.")

    while True:
        user_input = input("\nSwap (e.g., 'ET'): ").strip().upper()
        if user_input == 'DONE':
            break
        if len(user_input) == 2:
            c1, c2 = user_input[0], user_input[1]
            # Find the cipher letters that map to c1 and c2
            reverse_mapping = {v: k for k, v in mapping.items()}
            if c1 in reverse_mapping and c2 in reverse_mapping:
                mapping[reverse_mapping[c1]] = c2
                mapping[reverse_mapping[c2]] = c1
                decrypted = decrypt_with_mapping(ciphertext, mapping)
                print(f"\n  Updated decryption:")
                print(f"  {decrypted[:80]}...")
            else:
                print("  Letter not found in mapping. Try again.")

    return mapping


def main():
    parser = argparse.ArgumentParser(
        description='Frequency Analysis Attack on Monoalphabetic Substitution Cipher'
    )
    parser.add_argument(
        '--ciphertext', '-c',
        type=str,
        help='Ciphertext to analyze (in quotes)'
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='File containing the ciphertext'
    )
    parser.add_argument(
        '--no-interactive', '-n',
        action='store_true',
        help='Skip interactive refinement'
    )

    args = parser.parse_args()

    print("=" * 50)
    print("  Frequency Analysis Attack")
    print("=" * 50)

    # Step 1: Get ciphertext
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            ciphertext = f.read()
    elif args.ciphertext:
        ciphertext = args.ciphertext
    else:
        print("\n[Using sample ciphertext for demonstration]")
        ciphertext, known_mapping = create_sample_ciphertext()
        print(f"[Known mapping: A->Q, B->W, C->E, D->R, ...]")

    # Step 2: Display ciphertext
    print(f"\n--- Ciphertext ({len(ciphertext)} chars) ---")
    print(f"  {ciphertext[:100]}{'...' if len(ciphertext) > 100 else ''}")

    # Step 3: Frequency analysis
    cipher_freq, cipher_counts, total = count_frequencies(ciphertext)
    display_frequencies("Letter Frequencies in Ciphertext", cipher_freq)

    # Step 4: Display standard English frequencies for comparison
    display_frequencies("Standard English Frequencies", ENGLISH_FREQ)

    # Step 5: Bigram and Trigram analysis
    bigram_analysis(ciphertext)
    trigram_analysis(ciphertext)

    # Step 6: Propose substitution mapping
    proposed_mapping = propose_mapping(cipher_freq, ENGLISH_FREQ)

    print("\n--- Proposed Substitution Mapping ---")
    print(f"  {'Cipher':>6}  ->  {'Plain':<6}  |  {'Cipher Freq':>11}  |  {'English Freq':>12}")
    print(f"  {'-'*6}  ->  {'-'*6}  |  {'-'*11}  |  {'-'*12}")
    for cipher_letter in sorted(
        proposed_mapping,
        key=lambda x: cipher_freq.get(x, 0),
        reverse=True
    ):
        plain_letter = proposed_mapping[cipher_letter]
        c_freq = cipher_freq.get(cipher_letter, 0)
        e_freq = ENGLISH_FREQ.get(plain_letter, 0)
        print(f"  {cipher_letter:>6}  ->  {plain_letter:<6}  |  {c_freq:10.2f}%  |  {e_freq:11.2f}%")

    # Step 7: Decrypt with proposed mapping
    decrypted = decrypt_with_mapping(ciphertext, proposed_mapping)
    print(f"\n--- Decryption Result (auto) ---")
    print(f"  {decrypted[:120]}{'...' if len(decrypted) > 120 else ''}")

    # Step 8: Calculate accuracy if plaintext is known
    try:
        sample_ciphertext, _ = create_sample_ciphertext()
        if ciphertext == sample_ciphertext:
            known_plaintext = (
                "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. "
                "CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES FOR "
                "SECURE COMMUNICATION IN THE PRESENCE OF ADVERSARIES. "
                "MODERN CRYPTOGRAPHY EXISTS AT THE INTERSECTION OF THE "
                "DISCIPLINES OF MATHEMATICS COMPUTER SCIENCE AND ELECTRICAL "
                "ENGINEERING. APPLICATIONS INCLUDE ELECTRONIC COMMERCE "
                "CHIP-BASED PAYMENT CARDS DIGITAL CURRENCIES AND COMPUTER "
                "PASSWORDS. THE FIELD OF CRYPTOGRAPHY INCLUDES ENCRYPTION "
                "WHICH PROTECTS THE CONFIDENTIALITY OF DATA AND DIGITAL "
                "SIGNATURES WHICH AUTHENTICATE THE IDENTITY OF USERS."
            )
            accuracy = calculate_accuracy(decrypted, known_plaintext)
            print(f"\n--- Accuracy: {accuracy:.1f}% ---")
    except Exception:
        pass

    # Step 9: Interactive refinement
    if not args.no_interactive:
        try:
            refined_mapping = interactive_refinement(ciphertext, proposed_mapping)
            final_decrypted = decrypt_with_mapping(ciphertext, refined_mapping)
            print(f"\n--- Final Decryption Result ---")
            print(f"  {final_decrypted}")
        except (EOFError, KeyboardInterrupt):
            print("\n[Interactive mode skipped]")


if __name__ == '__main__':
    main()
