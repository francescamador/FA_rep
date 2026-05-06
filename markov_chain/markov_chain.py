import requests
import re

def get_random_string(paragraphs):
    url="https://lorem-api.com"
    params = {
        "paragraphs": paragraphs,
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return(response.text)

    else:
        return(response.status_code)

def filter_random_string(string):
    filtered = re.sub(r'[^a-zA-Z]', '', string)
    return(filtered)

def transition_matrix(text):
    vowels = set("aeiouAEIOU")

    counts = {
        "VV": 0,
        "VC": 0,
        "CV": 0,
        "CC": 0
    }

    v_total = 0
    C_total = 0

    # count transitions
    for i in range(len(text) - 1):
        a = text[i]
        b = text[i + 1]

        if a in vowels:
            if b in vowels:
                counts["VV"] += 1
            else:
                counts["VC"] += 1
        else:
            if b in vowels:
                counts["CV"] += 1
            else:
                counts["CC"] += 1
    
    # compute probabilities
    v_total = counts["VV"] + counts["VC"]
    c_total = counts["CV"] + counts["CC"]

    matrix = {
        "V": {
            "V": counts["VV"] / v_total if v_total else 0,
            "C": counts["VC"] / v_total if v_total else 0
        },
        "C": {
            "V": counts["CV"] / c_total if c_total else 0,
            "C": counts["CC"] / c_total if c_total else 0
        }
    }

    return counts, matrix


def main():
    try:
        random_text = get_random_string(1)
        filtered_text = filter_random_string(random_text)
        result = transition_matrix(filtered_text)
        print(result)

    except Exception as e:
        print(f"Excelption: {e}")
        return
if __name__ == "__main__":
    main()
