# Homework 5 (knowledge base builder)
# Alec Dosier (ald170830)

import pickle

def display_kb(knowledge_base):
    print("Knowledge base by term:")
    for i in knowledge_base:
        print(' ')
        print(i, ' with ', len(knowledge_base[i]), ' sentences ', '=======================================================================')
        for x in knowledge_base[i]:
                print(x)

if __name__ == '__main__':

    fname = 'url_text_clean_'
    top_terms_fname = 'top_10_terms.txt'
    num_files = 103

    knowledge_base = {}

    targets = []
    # load the target terms in as a list
    with open(top_terms_fname, 'r', encoding='utf-8') as f:
        targets = f.read().splitlines()

    # initalize dict keys with empty lists
    for target in targets:
        knowledge_base[target] = []

    # load each data file one at a time
    for u in range(1, num_files):
        # load all sentences into a list
        sentences = []
        sentences = pickle.load(open((fname + str(u) + '.pickle'), 'rb'))


        # search each sentence for the existence of each term
            # if a term exists in the sentence, insert as an element in the list referred to by the dictionary[target] key
        for s in sentences:
            for t in targets:
                if t in s:
                    knowledge_base[t].append(s)

    display_kb(knowledge_base)

    # after all sentences have been scanned, the knowledge base is saved as a pickle file
    pickle.dump(knowledge_base, open('knowledge_base.pickle', 'wb'))






