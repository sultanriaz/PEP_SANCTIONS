
# PEP + Sanctions Screening AI Agent

A Python-based **PEP and Sanctions Screening Module** for KYC/AML compliance workflows.  
This project uses **NLP-style name normalization**, **fuzzy matching**, and **risk scoring** to screen customers against a dummy watchlist dataset.

> This project uses synthetic/dummy data only. It does not contain real PEPs, sanctioned persons, criminals, or official watchlist records.

---

## Project Overview

The goal of this project is to build a compliance screening prototype that can:

- Screen customer names against a dummy watchlist
- Detect possible matches using fuzzy name matching
- Compare customer details such as name, date of birth, and country
- Calculate a risk score
- Return a structured screening decision
- Reduce false positives using scoring logic
- Provide explainable output for review

---

## Key Features

- Customer screening by name, DOB, and country
- Name normalization
- Alias handling
- Fuzzy matching using RapidFuzz
- Risk scoring engine
- Structured terminal report
- Top match detection
- Top possible matches listing
- Pytest-based unit testing support
- Dummy CSV watchlist support

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | CSV loading and data handling |
| RapidFuzz | Fuzzy name matching |
| Pytest | Unit testing |

---

## Project Structure

```txt
PEP_SANCTIONS/
│
├── data/
│   └── watchlist_dummy_1000.csv
│
├── src/
│   ├── __init__.py
│   ├── normalizer.py
│   ├── matcher.py
│   ├── scorer.py
│   ├── agent.py
│   └── main.py
│
├── tests/
│   └── test_matcher.py
│
├── requirements.txt
└── README.md
````

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pep-sanctions-screening-agent.git
cd pep-sanctions-screening-agent
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

For Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Dataset Format

The project expects a CSV file inside the `data/` folder.

Example file:

```txt
data/watchlist.csv
```

Expected columns:

```csv
id,full_name,aliases,dob,country,nationality,list_type,source,entity_type,risk_level
```

Example row:

```csv
WL0001,Ahmed Khan,A Khan|Ahmad Khan|Ahmed K,1975-03-22,Pakistan,Pakistani,PEP,Dummy-Internal,Individual,High
```

---

## How to Run

Run the project from the root directory:

```bash
python src/main.py
```

Example customer input inside `main.py`:

```python
customer = {
    "name": "Ahmad Khan",
    "dob": "1975-03-22",
    "country": "Pakistan"
}
```

---

## Example Output

```txt
========== PEP + SANCTIONS SCREENING REPORT ==========

Customer Information
--------------------
Name       : Ahmad Khan
DOB        : 1975-03-22
Country    : Pakistan

Screening Decision
------------------
Status     : Possible Match
Risk Score : 75.13

Top Match
---------
Watchlist ID : WL006848
Matched Name : Ahmed Khan
Name Score   : 90.27
Risk Score   : 75.13
Decision     : Possible Match
List Type    : Sanctions
Source       : CorporateRegistry

Top 5 Possible Matches
----------------------

Match #1
ID          : WL097073
Name        : Ahmed Khan
Name Score  : 94.89
Risk Score  : 72.44
Decision    : Possible Match
List Type   : PEP
Source      : UN

Explanation
-----------
Customer 'Ahmad Khan' matched with watchlist record 'Ahmed Khan'.

=====================================================
```

---

## Core Workflow

```txt
Customer Input
      ↓
Name Normalization
      ↓
Alias Extraction
      ↓
Fuzzy Matching
      ↓
Risk Scoring
      ↓
Top Match Selection
      ↓
Structured Screening Report
```

---

## Module Explanation

### `normalizer.py`

Handles text cleaning and name preparation.

Main responsibilities:

* Convert names to lowercase
* Remove symbols and extra spaces
* Remove accents
* Normalize aliases

---

### `matcher.py`

Handles fuzzy matching between customer names and watchlist records.

Main responsibilities:

* Compare customer name with full name
* Compare customer name with aliases
* Calculate name similarity score
* Return matches above threshold

---

### `scorer.py`

Calculates the final risk score.

Scoring factors may include:

* Name similarity
* Date of birth match
* Country match
* List type severity

Example decisions:

| Score Range | Decision          |
| ----------- | ----------------- |
| 85+         | High-Risk Match   |
| 65–84       | Possible Match    |
| Below 65    | Low-Risk / Review |

---

### `agent.py`

Combines all modules into a complete screening workflow.

Main responsibilities:

* Load watchlist CSV
* Screen customer
* Find possible matches
* Score matches
* Select top match
* Generate explanation

---

### `main.py`

Entry point of the project.

Main responsibilities:

* Define customer input
* Run screening agent
* Print structured result

---

## Running Tests

Run all tests:

```bash
pytest
```

Run tests with detailed output:

```bash
pytest -v
```

---

## Example Test Case

```python
def test_fuzzy_name_match():
    df = pd.read_csv("data/watchlist_dummy_1000.csv")
    matches = find_matches("Ahmad Khan", df)

    assert len(matches) > 0
```

---

## Future Improvements

* Add FastAPI backend
* Add `/screen-customer` API endpoint
* Add Streamlit or React frontend
* Add database support using PostgreSQL or SQLite
* Add adverse media article summarization
* Add corporate registry screening
* Add batch CSV customer screening
* Add PDF/JSON report generation
* Add LLM-based explanation generation
* Add audit logs for compliance review

---

## Compliance Disclaimer

This project is for educational and prototype purposes only.

It uses dummy data and should not be used as a production AML/KYC compliance system without:

* Official watchlist data integration
* Legal and compliance validation
* Proper audit logging
* Human review workflow
* Data privacy controls
* Security hardening
* Regulatory approval

---

## Author

**Sultan Riaz**
BS Computer Science Student
Project Category: AI Agent / KYC / AML Compliance / PEP + Sanctions Screening

---

## License

This project is open for educational use.

```
```
