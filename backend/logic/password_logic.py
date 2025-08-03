import string
import secrets
import math

# --- Built-in Wordlist for Memorable Passwords ---
# Sourced from a common, effective wordlist for generating passphrases.
EASY_WORDS = [
    "acid", "acorn", "acre", "acts", "afar", "affix", "aged", "agent",
    "agile", "aging", "agony", "ahead", "aide", "aids", "aim", "air",
    "aisle", "ajar", "alarm", "album", "ale", "alert", "alga", "alia",
    "alias", "alibi", "alien", "align", "alike", "alive", "alkali",
    "all", "alley", "alloy", "ally", "aloe", "aloft", "aloha", "alone",
    "amaze", "amber", "ambit", "amble", "ambush", "amend", "amid",
    "amide", "amino", "ample", "amply", "amuck", "amuse", "anew",
    "ankle", "annex", "annoy", "annul", "anthem", "any", "anyhow",
    "anyway", "apart", "apathy", "apex", "aphid", "aplomb", "appeal",
    "apple", "apply", "apron", "apt", "aptly", "arbor", "arc", "arcane",
    "arch", "area", "arena", "argon", "argue", "arise", "ark", "arm",
    "armful", "armpit", "army", "aroma", "array", "arrow", "arson",
    "art", "ascot", "ashen", "ash", "aside", "ask", "askew", "asleep",
    "aspect", "assay", "asset", "atlas", "atom", "atomic", "attic",
    "audio", "audit", "auger", "aunt", "aura", "auto", "autumn", "avail",
    "avert", "avian", "avoid", "await", "awake", "award", "aware",
    "awash", "away", "awful", "awoke", "axial", "axiom", "axis", "axle",
    "bacon", "badge", "badly", "bag", "baggy", "bail", "bait", "bake",
    "baker", "balance", "bald", "ball", "ballet", "ballot", "balm",
    "balsa", "bamboo", "band", "banjo", "bank", "bar", "barb", "bard",
    "barely", "barge", "bark", "barley", "barn", "baron", "barrel",
    "base", "basic", "basil", "basin", "basis", "basket", "bass",
    "bat", "batch", "bath", "baton", "battle", "bay", "beach", "bead",
    "beak", "beam", "bean", "bear", "beard", "beast", "beat", "beauty",
    "beaver", "beckon", "bed", "bee", "beech", "beef", "beep", "beer",
    "beet", "befit", "beg", "began", "beget", "begin", "begun", "beige",
    "being", "belch", "bell", "belly", "below", "belt", "bench", "bend",
    "best", "bet", "beta", "bevel", "bevy", "bias", "bible", "bicep",
    "bidet", "big", "bike", "bile", "bilge", "bill", "billion", "bin",
    "bind", "bingo", "biped", "birch", "bird", "birth", "bison", "bit",
    "bitch", "bite", "black", "blade", "blame", "bland", "blast",
    "blaze", "bleak", "bleat", "bleed", "bleep", "blend", "bless",
    "blimp", "blink", "blip", "bliss", "blitz", "bloat", "blob", "block",
    "blond", "blood", "bloom", "blow", "blue", "bluff", "blunt", "blur",
    "blurt", "blush", "boar", "board", "boast", "boat", "body", "bog",
    "bogus", "boil", "bold", "bolt", "bomb", "bond", "bone", "bonnet",
    "bonus", "bony", "book", "boom", "boost", "boot", "booth", "booze",
    "bop", "borax", "bore", "born", "boron", "boss", "botch", "both",
    "bottle", "bottom", "bough", "bouncy", "bound", "bow", "bowl",
    "box", "boy", "bra", "brace", "brad", "brag", "braid", "brain",
    "brake", "bran", "brand", "brash", "brass", "brat", "brave", "brawl",
    "brawn", "bread", "break", "breed", "breeze", "bribe", "brick",
    "bride", "brief", "brig", "brim", "brine", "bring", "brink", "brisk",
    "broad", "broil", "broke", "bronze", "brood", "brook", "broom",
    "broth", "brown", "browse", "brunt", "brush", "brute", "bubble",
    "buck", "bucket", "buckle", "buddy", "budge", "budget", "buff",
    "bug", "buggy", "build", "bulb", "bulge", "bulk", "bulky", "bull",
    "bully", "bump", "bumpy", "bunch", "bungee", "bunk", "bunny",
    "bunt", "buoy", "burly", "burn", "burp", "burrow", "bursar", "burst",
    "bus", "bush", "bust", "busy", "but", "butane", "butch", "butt",
    "buy", "buyer", "buzz", "bye", "bygone", "bylaw", "bypass", "byte"
]

def calculate_strength(password, char_pool_size):
    """Calculates password strength based on entropy."""
    if not password or not char_pool_size:
        return {"text": "N/A", "color": "bg-gray-500", "width": "0%"}
    
    # Calculate the number of possible combinations (entropy)
    entropy = len(password) * math.log2(char_pool_size)
    
    # Determine strength level based on entropy score
    if entropy < 40:
        text, color, width = "Very Weak", "bg-red-500", "20%"
    elif entropy < 60:
        text, color, width = "Weak", "bg-orange-500", "40%"
    elif entropy < 80:
        text, color, width = "Medium", "bg-yellow-500", "60%"
    elif entropy < 100:
        text, color, width = "Strong", "bg-blue-500", "80%"
    else:
        text, color, width = "Very Strong", "bg-green-500", "100%"
        
    return {"text": text, "color": color, "width": width}

def generate_random_password(length, use_uppercase, use_lowercase, use_numbers, use_special, exclude_similar):
    """
    Generates a cryptographically strong random password.
    
    Uses the 'secrets' module for generating random characters, which is
    suitable for cryptographic applications.
    """
    char_pool_str = ""
    if use_uppercase: char_pool_str += string.ascii_uppercase
    if use_lowercase: char_pool_str += string.ascii_lowercase
    if use_numbers: char_pool_str += string.digits
    if use_special: char_pool_str += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    # Exclude visually similar characters if requested
    if exclude_similar:
        char_pool_str = "".join(c for c in char_pool_str if c not in "il1LoO")

    if not char_pool_str:
        return "", 0 # Return empty if no character sets are selected

    # Generate the password by choosing characters from the pool
    password = "".join(secrets.choice(char_pool_str) for _ in range(length))
    
    # Return the password and the size of the character pool for strength calculation
    return password, len(char_pool_str)

def generate_memorable_password(word_count, separator):
    """
    Generates a memorable passphrase using a wordlist (Diceware style).
    """
    # Select a number of random words from the list
    words = [secrets.choice(EASY_WORDS) for _ in range(word_count)]
    
    # Join the words with the chosen separator
    password = separator.join(words)
    
    # The "pool size" for a memorable password is the total number of words available
    return password, len(EASY_WORDS)
