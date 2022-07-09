#### Clean Script begins here
import time
import sys
import pandas as pd
import random
import fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def similarity_function(key):
    return (lambda comp : fuzz.ratio(key, comp))

def find_best_match(df, key, k, delta):
    df_filter = df[(df.length > len(key)*(1 - delta))&(df.length < len(key)*(1+ delta))].copy()
    df_filter['fuzzy_similarity'] = df_filter['sequence'].apply(similarity_function(key))
    return df_filter.sort_values(by='fuzzy_similarity', ascending = False)[:k]


args = sys.argv[1:]
start = time.time()
key = args[0]
best_match = find_best_match(pd.read_csv('protein_base.csv'), key, int(args[1]), .1)
end = time.time()
similarity = list(best_match['fuzzy_similarity'])[0]

print( f"Match found! Confidence (similarity score): {similarity}")

for k, v in dict(best_match).items():
    if (k == 'pdb_id') or (list(v)[0] == 1):
        print(f'{k} : {list(v)[0]}')

print(f'found match in {end - start} seconds.')
