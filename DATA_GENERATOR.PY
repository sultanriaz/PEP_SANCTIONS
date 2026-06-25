import csv
import random
from datetime import date, timedelta

# ── Reproducible randomness ──────────────────────────────────────────────────
random.seed(42)

# ══════════════════════════════════════════════════════════════════════════════
# Name pools – each culture provides male/female given names and surnames.
# The "country" field holds the person's primary country (used later).
# ══════════════════════════════════════════════════════════════════════════════
NAME_POOLS = {
    "Pakistani": {
        "given_male": ["Ahmed", "Bilal", "Imran", "Faisal", "Tariq", "Usman", "Hamza", "Asad", "Junaid", "Shahid"],
        "given_female": ["Ayesha", "Sana", "Mehwish", "Nadia", "Rabia", "Fatima", "Hina", "Saima", "Zainab", "Amina"],
        "surname": ["Khan", "Malik", "Sheikh", "Butt", "Qureshi", "Raza", "Chaudhry", "Hussain", "Abbasi", "Farooq"],
        "country": "Pakistan",
    },
    "Indian": {
        "given_male": ["Rajesh", "Amit", "Vikram", "Sanjay", "Arjun", "Rahul", "Suresh", "Anil", "Deepak", "Manoj"],
        "given_female": ["Priya", "Anita", "Kavita", "Sunita", "Pooja", "Neha", "Divya", "Shalini", "Meena", "Rekha"],
        "surname": ["Sharma", "Verma", "Gupta", "Patel", "Reddy", "Iyer", "Nair", "Singh", "Mehta", "Joshi"],
        "country": "India",
    },
    "Bangladeshi": {
        "given_male": ["Rafiq", "Habib", "Shahin", "Mizanur", "Kamal", "Jahangir", "Anwar", "Rashed", "Mahbub", "Saiful"],
        "given_female": ["Sultana", "Nasrin", "Roksana", "Shahida", "Farzana", "Salma", "Jasmin", "Rina", "Lutfa", "Parveen"],
        "surname": ["Rahman", "Islam", "Hossain", "Ahmed", "Chowdhury", "Karim", "Hoque", "Akter", "Uddin", "Talukder"],
        "country": "Bangladesh",
    },
    "Afghan": {
        "given_male": ["Najibullah", "Hamidullah", "Ahmad", "Rashid", "Karim", "Sayed", "Nasir", "Farid", "Zahir", "Khalil"],
        "given_female": ["Soraya", "Laila", "Shabnam", "Naheed", "Freshta", "Zarghona", "Parisa", "Homa", "Wajiha", "Maryam"],
        "surname": ["Noori", "Karimi", "Ahmadi", "Rasouli", "Hotak", "Wardak", "Popal", "Tarin", "Mohmand", "Barakzai"],
        "country": "Afghanistan",
    },
    "Arabic_Gulf": {
        "given_male": ["Mohammed", "Khalid", "Abdullah", "Saeed", "Salem", "Yousef", "Hamad", "Nasser", "Fahad", "Rashid"],
        "given_female": ["Fatima", "Maryam", "Aisha", "Noura", "Layla", "Hessa", "Salma", "Amal", "Shaikha", "Reem"],
        "surname": ["Al-Maktoum", "Al-Suwaidi", "Al-Marri", "Al-Qasimi", "Al-Hashimi", "Al-Falasi", "Al-Mansoori", "Al-Naqbi", "Al-Dosari", "Al-Kuwari"],
        "country": "United Arab Emirates",
    },
    "Saudi": {
        "given_male": ["Sultan", "Faisal", "Turki", "Bandar", "Majed", "Talal", "Saud", "Abdulaziz", "Mansour", "Ziad"],
        "given_female": ["Lulwa", "Haya", "Munira", "Sara", "Nawal", "Ghada", "Wafa", "Lamia", "Rania", "Dalal"],
        "surname": ["Al-Saud", "Al-Ghamdi", "Al-Otaibi", "Al-Harbi", "Al-Zahrani", "Al-Qahtani", "Al-Shehri", "Al-Anazi", "Al-Mutairi", "Al-Dossari"],
        "country": "Saudi Arabia",
    },
    "Egyptian": {
        "given_male": ["Mahmoud", "Tarek", "Hassan", "Hossam", "Ashraf", "Karim", "Sameh", "Wael", "Ayman", "Sherif"],
        "given_female": ["Mona", "Hanan", "Dina", "Rasha", "Yasmin", "Nourhan", "Heba", "Salma", "Eman", "Mervat"],
        "surname": ["El-Sayed", "Abdel-Rahman", "Mostafa", "Ibrahim", "Hassan", "Fathy", "Gad", "Mansour", "Saleh", "Hamdy"],
        "country": "Egypt",
    },
    "Persian": {
        "given_male": ["Reza", "Hossein", "Mehdi", "Ali", "Babak", "Farhad", "Kamran", "Arman", "Bahman", "Cyrus"],
        "given_female": ["Fariba", "Shirin", "Negar", "Parvin", "Marjan", "Roya", "Mahsa", "Leila", "Niloofar", "Soheila"],
        "surname": ["Hosseini", "Rezaei", "Moradi", "Ahmadi", "Karimi", "Sadeghi", "Jafari", "Ebrahimi", "Ghorbani", "Bahrami"],
        "country": "Iran",
    },
    "Turkish": {
        "given_male": ["Mehmet", "Mustafa", "Emre", "Burak", "Kemal", "Ozan", "Serkan", "Tolga", "Volkan", "Hakan"],
        "given_female": ["Elif", "Zeynep", "Ayse", "Fatma", "Derya", "Selin", "Gulsen", "Pinar", "Burcu", "Ebru"],
        "surname": ["Yilmaz", "Demir", "Kaya", "Celik", "Sahin", "Yildiz", "Aydin", "Ozturk", "Arslan", "Dogan"],
        "country": "Turkey",
    },
    "Chinese": {
        "given_male": ["Wei", "Jun", "Hao", "Lei", "Feng", "Tao", "Ming", "Qiang", "Bo", "Yong"],
        "given_female": ["Mei", "Ling", "Xiu", "Yan", "Hua", "Jing", "Fang", "Na", "Li", "Xia"],
        "surname": ["Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou"],
        "country": "China",
    },
    "Russian": {
        "given_male": ["Ivan", "Sergei", "Dmitri", "Andrei", "Pavel", "Viktor", "Oleg", "Nikolai", "Vladimir", "Yuri"],
        "given_female": ["Olga", "Natasha", "Irina", "Svetlana", "Yelena", "Tatiana", "Anastasia", "Marina", "Galina", "Larisa"],
        "surname": ["Ivanov", "Petrov", "Smirnov", "Volkov", "Sokolov", "Popov", "Kuznetsov", "Fedorov", "Morozov", "Pavlov"],
        "country": "Russia",
    },
    "African_Nigerian": {
        "given_male": ["Chinedu", "Emeka", "Ifeanyi", "Tunde", "Obinna", "Kayode", "Chukwuma", "Segun", "Babatunde", "Adewale"],
        "given_female": ["Ngozi", "Amaka", "Chioma", "Funmilayo", "Adaeze", "Bisi", "Yetunde", "Ifeoma", "Folake", "Nneka"],
        "surname": ["Okafor", "Adeyemi", "Eze", "Okonkwo", "Balogun", "Nwosu", "Olawale", "Ibrahim", "Abubakar", "Chukwu"],
        "country": "Nigeria",
    },
    "African_South": {
        "given_male": ["Sipho", "Thabo", "Lwazi", "Mandla", "Bongani", "Themba", "Kagiso", "Sizwe", "Lerato", "Tshepo"],
        "given_female": ["Nomvula", "Zanele", "Thandiwe", "Precious", "Nokuthula", "Busisiwe", "Palesa", "Refilwe", "Ayanda", "Zinhle"],
        "surname": ["Nkosi", "Dlamini", "Mokoena", "Khumalo", "Mahlangu", "Sithole", "Ndlovu", "Mthembu", "Botha", "Van der Merwe"],
        "country": "South Africa",
    },
    "Western_US_UK": {
        "given_male": ["James", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Christopher"],
        "given_female": ["Mary", "Jennifer", "Linda", "Susan", "Karen", "Elizabeth", "Sarah", "Jessica", "Emily", "Margaret"],
        "surname": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson", "Anderson", "Taylor"],
        "country": "United States",
    },
    "Canadian": {
        "given_male": ["Liam", "Noah", "Ethan", "Jacob", "Benjamin", "Logan", "Mason", "Lucas", "Owen", "Carter"],
        "given_female": ["Olivia", "Emma", "Ava", "Sophia", "Chloe", "Charlotte", "Mia", "Amelia", "Abigail", "Madison"],
        "surname": ["Tremblay", "Gagnon", "Roy", "Cote", "Bouchard", "MacDonald", "Campbell", "Stewart", "Fraser", "Wilson"],
        "country": "Canada",
    },
    "German": {
        "given_male": ["Hans", "Klaus", "Stefan", "Wolfgang", "Jurgen", "Dieter", "Lukas", "Felix", "Matthias", "Florian"],
        "given_female": ["Hannah", "Greta", "Ingrid", "Petra", "Ursula", "Birgit", "Sabine", "Anja", "Claudia", "Monika"],
        "surname": ["Muller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Hoffmann", "Schulz"],
        "country": "Germany",
    },
    "French": {
        "given_male": ["Jean", "Pierre", "Michel", "Philippe", "Alain", "Nicolas", "Olivier", "Laurent", "Thierry", "Sebastien"],
        "given_female": ["Marie", "Nathalie", "Isabelle", "Sylvie", "Catherine", "Christine", "Veronique", "Sandrine", "Celine", "Aurelie"],
        "surname": ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Petit", "Durand", "Leroy", "Moreau", "Simon"],
        "country": "France",
    },
    "Italian": {
        "given_male": ["Giuseppe", "Antonio", "Marco", "Luca", "Francesco", "Alessandro", "Andrea", "Matteo", "Davide", "Roberto"],
        "given_female": ["Giulia", "Francesca", "Chiara", "Federica", "Valentina", "Sara", "Elena", "Martina", "Alessia", "Paola"],
        "surname": ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco"],
        "country": "Italy",
    },
    "Spanish": {
        "given_male": ["Antonio", "Manuel", "Francisco", "Jose", "Javier", "Carlos", "Miguel", "Rafael", "Pedro", "Alejandro"],
        "given_female": ["Maria", "Carmen", "Ana", "Isabel", "Laura", "Cristina", "Marta", "Lucia", "Elena", "Sofia"],
        "surname": ["Garcia", "Martinez", "Lopez", "Sanchez", "Perez", "Gomez", "Fernandez", "Diaz", "Moreno", "Alvarez"],
        "country": "Spain",
    },
    "Brazilian": {
        "given_male": ["Joao", "Pedro", "Lucas", "Gustavo", "Rafael", "Bruno", "Eduardo", "Felipe", "Ricardo", "Marcelo"],
        "given_female": ["Maria", "Ana", "Juliana", "Camila", "Fernanda", "Patricia", "Larissa", "Beatriz", "Carla", "Aline"],
        "surname": ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Almeida", "Pereira", "Lima", "Carvalho"],
        "country": "Brazil",
    },
    "Mexican": {
        "given_male": ["Jose", "Juan", "Luis", "Carlos", "Jesus", "Miguel", "Alejandro", "Francisco", "Ricardo", "Eduardo"],
        "given_female": ["Guadalupe", "Maria", "Rosa", "Veronica", "Alejandra", "Adriana", "Leticia", "Gabriela", "Monica", "Patricia"],
        "surname": ["Hernandez", "Gonzalez", "Ramirez", "Torres", "Flores", "Rivera", "Gomez", "Diaz", "Reyes", "Morales"],
        "country": "Mexico",
    },
    "Argentine": {
        "given_male": ["Mariano", "Sebastian", "Federico", "Martin", "Diego", "Gonzalo", "Nicolas", "Ezequiel", "Hernan", "Leandro"],
        "given_female": ["Florencia", "Valentina", "Agustina", "Lucia", "Romina", "Carolina", "Daniela", "Victoria", "Paula", "Mariana"],
        "surname": ["Fernandez", "Gonzalez", "Rodriguez", "Lopez", "Martinez", "Garcia", "Perez", "Sanchez", "Romero", "Alvarez"],
        "country": "Argentina",
    },
    "Malaysian": {
        "given_male": ["Azman", "Hafiz", "Faiz", "Rizal", "Zulkifli", "Hakim", "Shafiq", "Anwar", "Idris", "Nazri"],
        "given_female": ["Siti", "Noor", "Aishah", "Farah", "Nurul", "Zainab", "Aminah", "Rohana", "Hasnah", "Maimunah"],
        "surname": ["bin Abdullah", "bin Ismail", "bin Hassan", "bin Yusof", "bin Ahmad", "binti Rahman", "binti Othman", "binti Zainal", "bin Salleh", "binti Mahmud"],
        "country": "Malaysia",
    },
    "Indonesian": {
        "given_male": ["Budi", "Agus", "Joko", "Eko", "Hendra", "Bambang", "Wahyu", "Dedi", "Yusuf", "Anwar"],
        "given_female": ["Siti", "Dewi", "Ratna", "Wulan", "Indah", "Putri", "Sri", "Ayu", "Lestari", "Wati"],
        "surname": ["Santoso", "Wijaya", "Kusuma", "Permana", "Hidayat", "Setiawan", "Pratama", "Nugroho", "Suryanto", "Gunawan"],
        "country": "Indonesia",
    },
    "Singaporean": {
        "given_male": ["Wei Ming", "Jun Jie", "Kai Xuan", "Zhi Hao", "Wen Hao", "Yi Sheng", "Hao Ran", "Jia Le", "Kang Wei", "Boon Keng"],
        "given_female": ["Hui Ling", "Mei Yi", "Xin Yi", "Jia Hui", "Li Wen", "Yu Ting", "Shu Hui", "Wan Ting", "Pei Shan", "Si Ying"],
        "surname": ["Tan", "Lim", "Lee", "Ng", "Wong", "Goh", "Chua", "Teo", "Koh", "Ong"],
        "country": "Singapore",
    },
    "Nepali": {
        "given_male": ["Bikash", "Suresh", "Ramesh", "Dipak", "Prakash", "Anil", "Bishal", "Santosh", "Kiran", "Niraj"],
        "given_female": ["Sita", "Gita", "Anita", "Sunita", "Puja", "Sarita", "Kamala", "Laxmi", "Manisha", "Sushma"],
        "surname": ["Sharma", "Shrestha", "Gurung", "Thapa", "Tamang", "Rai", "Lama", "Adhikari", "Karki", "Bista"],
        "country": "Nepal",
    },
    "SriLankan": {
        "given_male": ["Sunil", "Nimal", "Kasun", "Pradeep", "Chamara", "Ruwan", "Dinesh", "Asanka", "Lakshan", "Saman"],
        "given_female": ["Nilmini", "Chamari", "Kumari", "Sandya", "Anusha", "Dilani", "Priyanka", "Malini", "Ishara", "Geetha"],
        "surname": ["Perera", "Fernando", "Silva", "Jayawardena", "Wickramasinghe", "Bandara", "Gunawardena", "Rajapaksa", "Dissanayake", "Senanayake"],
        "country": "Sri Lanka",
    },
    "Japanese": {
        "given_male": ["Hiroshi", "Takeshi", "Kenji", "Satoshi", "Yuto", "Daiki", "Haruto", "Sora", "Riku", "Kazuki"],
        "given_female": ["Yuki", "Sakura", "Hana", "Aoi", "Yui", "Mio", "Rina", "Akiko", "Naomi", "Emi"],
        "surname": ["Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto", "Nakamura", "Kobayashi", "Kato"],
        "country": "Japan",
    },
    "Qatari_Kuwaiti": {
        "given_male": ["Jassim", "Ahmad", "Tareq", "Sultan", "Waleed", "Adel", "Fawaz", "Anas", "Bader", "Hamad"],
        "given_female": ["Lulwa", "Mariam", "Shaikha", "Anoud", "Fajer", "Dalal", "Rawan", "Noora", "Hala", "Bashayer"],
        "surname": ["Al-Thani", "Al-Sabah", "Al-Kuwari", "Al-Mutawa", "Al-Ansari", "Al-Hajri", "Al-Rumaihi", "Al-Khalifa", "Al-Mannai", "Al-Awadhi"],
        "country": "Qatar",
    },
    "Australian": {
        "given_male": ["Jack", "Oliver", "William", "Lachlan", "Cooper", "Harrison", "Riley", "Ryan", "Connor", "Hunter"],
        "given_female": ["Charlotte", "Ruby", "Mia", "Grace", "Isla", "Zoe", "Chloe", "Lily", "Ella", "Sienna"],
        "surname": ["Smith", "Jones", "Williams", "Brown", "Wilson", "Taylor", "Johnson", "White", "Martin", "Anderson"],
        "country": "Australia",
    },
}

# All available cultures – used to pick a random background for each person.
CULTURE_KEYS = list(NAME_POOLS.keys())

# Master list of possible countries (nationality, country of risk).
COUNTRY_POOL = [
    "Pakistan", "India", "United States", "United Kingdom", "Canada",
    "United Arab Emirates", "Saudi Arabia", "China", "Russia", "Iran",
    "Turkey", "Germany", "France", "Brazil", "South Africa", "Nigeria",
    "Bangladesh", "Afghanistan", "Malaysia", "Indonesia", "Australia",
    "Japan", "Italy", "Spain", "Egypt", "Qatar", "Kuwait", "Singapore",
    "Nepal", "Sri Lanka", "Mexico", "Argentina",
]

# ── List type & risk configuration ───────────────────────────────────────────
LIST_TYPES = ["PEP", "Sanctions", "Adverse Media", "Watchlist", "High Risk Individual"]
LIST_TYPE_WEIGHTS = [25, 20, 25, 20, 10]                     # must sum to 100

# Risk level weights for each list type (Low, Medium, High, Critical).
# Weights represent relative frequencies within the list type.
RISK_WEIGHTS_BY_LIST_TYPE = {
    "Sanctions":            {"Low": 2,  "Medium": 8,  "High": 45, "Critical": 45},
    "PEP":                  {"Low": 5,  "Medium": 45, "High": 40, "Critical": 10},
    "Adverse Media":        {"Low": 5,  "Medium": 45, "High": 40, "Critical": 10},
    "Watchlist":            {"Low": 40, "Medium": 45, "High": 12, "Critical": 3},
    "High Risk Individual": {"Low": 2,  "Medium": 8,  "High": 45, "Critical": 45},
}

# Possible data sources for the watchlist entry.
SOURCES = [
    "OFAC", "UN", "EU", "Interpol",
    "WorldCheck", "News", "Internal", "CorporateRegistry",
]

# ── Date range for random date of birth ──────────────────────────────────────
START_DATE = date(1945, 1, 1)
END_DATE   = date(2005, 12, 31)
DATE_RANGE_DAYS = (END_DATE - START_DATE).days   # number of days in the range

# ──────────────────────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────────────────────

def random_dob() -> str:
    offset = random.randint(0, DATE_RANGE_DAYS)
    return (START_DATE + timedelta(days=offset)).isoformat()


def weighted_choice(options: list, weights: list) -> any:
    return random.choices(options, weights=weights, k=1)[0]


def pick_list_type() -> str:
    """Randomly select a watchlist type based on the predefined weights."""
    return weighted_choice(LIST_TYPES, LIST_TYPE_WEIGHTS)


def pick_risk_level(list_type: str) -> str:
 
    weights_map = RISK_WEIGHTS_BY_LIST_TYPE[list_type]
    levels = list(weights_map.keys())
    weights = list(weights_map.values())
    return weighted_choice(levels, weights)


# ── Name variant helpers (used for alias generation) ─────────────────────────

def make_initial(name_part: str) -> str:
    """Return the first-letter initial followed by a period (e.g., 'A.')."""
    return name_part[0].upper() + "."


def shorten_name(name_part: str) -> str:
    if len(name_part) <= 4:
        return name_part
    # Cut somewhere between the 3rd character and the penultimate character.
    cut = random.randint(3, max(3, len(name_part) - 1))
    return name_part[:cut]


def introduce_typo(name_part: str) -> str:
    if len(name_part) < 4:
        return name_part
    chars = list(name_part)
    idx = random.randint(1, len(chars) - 2)      # avoid first/last char
    swap_type = random.choice(["double", "drop", "swap_vowel"])

    if swap_type == "double" and chars[idx].isalpha():
        chars.insert(idx, chars[idx])
    elif swap_type == "drop":
        del chars[idx]
    elif swap_type == "swap_vowel":
        vowels = "aeiou"
        if chars[idx].lower() in vowels:
            chars[idx] = random.choice(vowels)
    return "".join(chars)


def generate_aliases(given: str, surname: str, full_name: str) -> str:
    candidates = set()

    # Initial + surname
    candidates.add(f"{make_initial(given)} {surname}")
    # Surname-first order
    candidates.add(f"{surname} {given}")
    # Shortened given name
    short_given = shorten_name(given)
    if short_given.lower() != given.lower():
        candidates.add(f"{short_given} {surname}")
    # Typo variant of full name
    typo_given = introduce_typo(given)
    candidates.add(f"{typo_given} {surname}")
    # Given name + surname initial
    candidates.add(f"{given} {make_initial(surname)}")

    # Remove the exact original name and any empty strings
    candidates.discard(full_name)
    candidates = {c for c in candidates if c.strip()}

    # Shuffle and pick 1–3 aliases
    chosen = list(candidates)
    random.shuffle(chosen)
    n = random.randint(1, min(3, len(chosen)))
    selected = chosen[:n]

    # Fallback – should never be needed but guarantees a non‑empty result
    if not selected:
        selected = [f"{make_initial(given)} {surname}"]

    return "|".join(selected)


# ──────────────────────────────────────────────────────────────────────────────
# Core data‑generation functions
# ──────────────────────────────────────────────────────────────────────────────

def generate_person(used_combos: set) -> dict:
    # 1. Pick a cultural background
    culture = random.choice(CULTURE_KEYS)
    pool = NAME_POOLS[culture]

    # 2. Random gender and name
    gender = random.choice(["given_male", "given_female"])
    given = random.choice(pool[gender])
    surname = random.choice(pool["surname"])
    full_name = f"{given} {surname}"

    # 3. Date of birth (unique combo enforced later)
    dob = random_dob()

    # 4. Country – 70% of the time it matches the cultural background,
    #    otherwise a random country from the global pool.
    if random.random() < 0.7:
        country = pool["country"]          # e.g. "Pakistan", "United States"
    else:
        country = random.choice(COUNTRY_POOL)

    # 5. Nationality – usually same as country, occasionally different (20%).
    if random.random() < 0.8:
        nationality = country
    else:
        nationality = random.choice(COUNTRY_POOL)

    # 6. Enforce uniqueness of (full_name, dob, country).
    #    With ~22,000 possible dates and a large variety of names, collisions
    #    are rare, but we guard against them anyway.
    combo_key = (full_name, dob, country)
    max_attempts = 10_000                  # safety ceiling to prevent infinite loop
    attempts = 0
    while combo_key in used_combos:
        dob = random_dob()
        combo_key = (full_name, dob, country)
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError(
                f"Unable to find a unique DOB for {full_name} in {country}. "
                "Consider expanding the date range or adding more name variety."
            )
    used_combos.add(combo_key)

    # 7. Aliases
    aliases = generate_aliases(given, surname, full_name)

    # 8. List type, source, entity type, risk level
    list_type = pick_list_type()
    source = random.choice(SOURCES)
    entity_type = "Individual"         # all records are individuals
    risk_level = pick_risk_level(list_type)

    return {
        "full_name": full_name,
        "aliases": aliases,
        "dob": dob,
        "country": country,
        "nationality": nationality,
        "list_type": list_type,
        "source": source,
        "entity_type": entity_type,
        "risk_level": risk_level,
    }


def generate_dataset(num_rows: int = 100_000) -> list:
    rows = []
    used_combos = set()          # ensures (name, dob, country) uniqueness

    for i in range(1, num_rows + 1):
        # Zero‑padded ID with a fixed width of 6 digits (supports up to 999,999 entries)
        record_id = f"WL{i:06d}"

        person = generate_person(used_combos)
        row = {"id": record_id, **person}
        rows.append(row)

    return rows


# ──────────────────────────────────────────────────────────────────────────────
# CSV output
# ──────────────────────────────────────────────────────────────────────────────

def write_csv(rows: list, filename: str = "watchlist_dummy.csv") -> None:
    fieldnames = [
        "id", "full_name", "aliases", "dob", "country",
        "nationality", "list_type", "source", "entity_type", "risk_level",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            # Ensure every field is present and non‑empty
            for field in fieldnames:
                value = row.get(field, "")
                if value is None or str(value).strip() == "":
                    raise ValueError(
                        f"Missing value in field '{field}' for row id {row.get('id')}"
                    )
            # Aliases must contain at least one alias; pipe delimiter is not mandatory
            # (a single alias without '|' is perfectly valid).
            assert isinstance(row["aliases"], str) and len(row["aliases"]) > 0, \
                f"Invalid aliases for id {row.get('id')}"

            writer.writerow(row)
# ──────────────────────────────────────────────────────────────────────────────
# Main entry point
# ──────────────────────────────────────────────────────────────────────────────
def main():
    """Generate the full 100k dataset and write it to disk."""
    print("Generating 100,000 watchlist entries ...")
    rows = generate_dataset(100_000)
    # Integrity checks
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "Duplicate IDs detected!"
    assert len(rows) == 100_000, f"Row count mismatch: expected 100000, got {len(rows)}"
    combos = [(r["full_name"], r["dob"], r["country"]) for r in rows]
    assert len(combos) == len(set(combos)), "Duplicate (name, DOB, country) combo found!"
    output_filename = "Dummy_data_100000_persons.csv"
    write_csv(rows, output_filename)
    print(f"Successfully wrote {len(rows)} rows to '{output_filename}'.")
if __name__ == "__main__":
    main()