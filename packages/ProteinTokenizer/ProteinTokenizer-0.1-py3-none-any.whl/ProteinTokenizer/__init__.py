def AA_tokenizer(AA, exclusive_tokens = None):
    """
    Tokenization of protein sequence at the Amino acid level. All of the 20 naturally occuring amino acids that can be found in the protein sequence will be tokenized.
    
    """
    import re
    pattern =  "(G|A|V|C|P|L|I|M|W|F|K|R|H|S|T|Y|N|Q|D|E)"
    regex = re.compile(pattern)
    tokens = [token for token in regex.findall(AA)]

    if exclusive_tokens:
        for i, tok in enumerate(tokens):
            if tok.startswith('['):
                if tok not in exclusive_tokens:
                    tokens[i] = '[UNK]'
    return tokens

#k-mer of AA tokenization
def kmer_tokenizer(proteins, ngram=4, stride=1, remove_last = False, exclusive_tokens = None):
    units = AA_tokenizer(proteins, exclusive_tokens = exclusive_tokens) #collect all the AA-wise tokens from the Protein Sequence
    if ngram == 1:
        tokens = units
    else:
        tokens = [tokens_to_mer(units[i:i+ngram]) for i in range(0, len(units), stride) if len(units[i:i+ngram]) == ngram]

    if remove_last:
        if len(tokens[-1]) < ngram: #truncate last whole k-mer if the length of the last k-mers is less than ngram.
            tokens = tokens[:-1]
    return tokens

def tokens_to_mer(toks):
    return ''.join(toks)

# define to_1D function
def to_1D(series):
  return pd.Series([x for _list in series for x in _list])