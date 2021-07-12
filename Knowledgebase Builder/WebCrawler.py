# Homework 5 (Web crawler)
# Alec Dosier (ald170830)

import sys
from bs4 import BeautifulSoup
import requests
import urllib
from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError
import re
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
import pickle
import random
from random import seed
import math

def create_knowledge_base(num_files, filename, top_terms_fname):
    knowledge_base = {}

    targets = []
    # load the target terms in as a list
    with open(top_terms_fname, 'r', encoding='utf-8') as f:
        targets = f.read().splitlines()

    # initalize dict keys with empty lists
    for target in targets:
        knowledge_base[target] = []

    # load each data file one at a time
    for u in range(1, num_urls+1):
        # load all sentences into a list
        sentences = []
        with open((filename + str(u) + '.pickle'), 'rb') as handle:
            sentences = pickle.load(handle)

        # search each sentence for the existence of each term
            # if a term exists in the sentence, insert as an element in the list referred to by the dictionary[target] key
        for s in sentences:
            for t in targets:
                knowledge_base[t].append(s)

    # after all sentences have been scanned, the knowledge base is saved as a pickle file
    print("Knowledge base by term:")
    for i in knowledge_base:
        print(i, ' |', knowledge_base[i])
        print("number of sentences for the term ", i, ' = ', len(knowledge_base[i]))

    pickle.dump(knowledge_base, open('knowledge_base.pickle', 'wb'))




def preprocess(text):
    # removes all digits
    text = re.sub(r'\d', '', text)

    # turns all punctuation into spaces. I could have replaced the first step with this but it would add a few more spaces
    text = re.sub(r'[.,?!;:()|/{}`\"\-\[\]%&\\\'/><@$+*^#=]', ' ', text)

    # tokenize into words (also removes all whitespaces)
    return word_tokenize(text)

def create_termf_dict(tokens, normalize=0):
    termf_dict = {}
    # update the tf dict to contain a word associated with its count
    for t in tokens:
        if t in termf_dict:
            termf_dict[t] += 1
        else:
            termf_dict[t] = 1

    # normalize
    if normalize == 0:
        for t in termf_dict.keys():
            termf_dict[t] = termf_dict[t]/len(tokens)

    return termf_dict

def create_tfidf_dict(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]
    return tf_idf

def create_tf_idfs(num_urls, raw_text_file_name):
    # Calculate term frequency of each doc and update vocab along the way
    tf_list_dict = []
    vocab = set()
    for u in range(1, num_urls+1):
        # load all tokenized sentences from pickle files
        sentences = []
        with open((raw_text_file_name + 'clean_' + str(u) + '.pickle' ), 'rb') as handle:
            sentences = pickle.load(handle)

        # preprocess each sentence and append the list of words to the back of the words list
        words = []
        for sent in sentences:
            tmp_words = preprocess(sent)
            # only append words that aren't stopwords
            for w in tmp_words:
                if w not in stopwords.words('english'):
                    words.append(w)

        # extract important terms from all the words in the web page
        tf = create_termf_dict(words)
        tf_list_dict.append(tf)
        # if you union an empty set and a new set, it returns nothing this initializes the set
        if u == 1:
            vocab = set(tf.keys())
        else:
            vocab = vocab.union(set(tf.keys()))

    # print('Number of Unique words:', len(vocab))
    # print('tf for "esports" in first page: ', tf_list_dict[0].get('esports'))

    # Calculate inverse document frequency ==========================
    idf_dict = {}
    doc_vocab = []

    # make a list containing an element for each document.
    # each element contains the dict.keys to check if a word shows up in a document
    for i in range(0, len(tf_list_dict)):
        doc_vocab.append(tf_list_dict[i].keys())

    # for each doc_vocab, create an element in the list and put an x for the number of documents this term is found
    # from this, we can calculate the inverse document frequency
    for term in vocab:
        temp = ['x' for voc in doc_vocab if term in voc]
        # make dict element key=term value=log(1 + num_docs / 1 + number of docs with the term present)
        idf_dict[term] = math.log((1+num_urls)/(1+len(temp)))

    # create tfidf dictionaries for each document using their own term frequency dict and the overall idf_dict
    tf_idf_list = []
    for i in tf_list_dict:
        tf_idf_list.append(create_tfidf_dict(i, idf_dict))

    return tf_idf_list

def clean_pages(num_files, input_name):
    for i in range(1, num_files+1):
        fname = input_name + str(i) + '.txt'
        raw_text = ''
        with open(fname, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        # remove tabs, spaces, and extra spaces that the removal introduces
        # I would have just removed the tabs and new lines, but that in turn stick two words together
        text = re.sub(r'\n', ' ', raw_text.lower())
        text = re.sub(r'\t', ' ', text)
        text = re.sub(r' +', ' ', text)

        # sent tokenize and pickle
        tokens = sent_tokenize(text)

        fname2 = input_name + 'clean_' + str(i) + '.pickle'
        pickle.dump(tokens, open(fname2, 'wb'))

    return

# finds if an element is visible so it knows what text will be more relevant
def is_visibile(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def scrape_pages(filename, input_name, URL_CAP = 0):
    # child function that scrapes an individual page given a url and a number to index
    # the files it creates
    def scrape_page(url, index):
        # open url and create Beautiful soup object
            # catches HTTP exceptions
        try:
            html = urllib.request.urlopen(url)
        except URLError as e:
            # will crash if its something other than an HTTP error
            # print("Error ", e.code, ' from url ', url)
            return -1

        soup = BeautifulSoup(html, features="html.parser")
        # find all data that is text on web page
        data = soup.findAll(text=True)
        # filter out data to only show visible elements and combine all text to a single large string
        result = filter(is_visibile, data)
        res_lst = list(result)
        res_string = ' '.join(res_lst)

        fname = input_name + str(index) + '.txt'
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(res_string)
        return 0

    # ============================ End of scrape_page =================================

    urls = []
    with open(filename, 'r') as f:
        urls = f.read().splitlines()

    # there is a URL cap (to minimize the number of files) it will randomize the list
        # and retrieve text from each page until either the URL cap is reached or the list is depleted
        # some of the links are forbidden, so it will check against the file index i
    seed(1841)
    random.shuffle(urls)

    # take the list of urls and retrieve text off each page and write to an indexed file
    i = 1
    e = 0
    for u in urls:
        if not scrape_page(u, i):
            # sometimes the web site forbids me from accessing it with this crawler
            # so I just skip over it to respect the web site
            i += 1

            # break out if cap exists and has been reached
            if URL_CAP != 0 and i-1 >= URL_CAP:
                break
        else:
            e += 1

    # return number of URL files created
    return i-1

def generate_url_file(start_url, topic, output_file_name):
    # pulls the text from the html and create a Beautiful Soup object
    r = requests.get(start_url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")

    # fetch all links within the start_url and write links to file
    url_file = 'relevant_urls.txt'
    count = 0

    tmp_links = []
    for link in soup.findAll('a'):
        link_s = str(link.get('href'))
        # ignore anything that doesn't have the topic in the link
        if topic in link_s or topic.capitalize() in link_s:
            # remove '/url?q=' sometimes found in the beginning of links
            if link_s.startswith('/url?q='):
                link_s = link_s[7:]
                print('MOD:', link_s)
            # ignore & and everything after
            if '&' in link_s:
                i = link_s.find('&')
                link_s = link_s[:i]
            # as long as this isn't a google link, add to list
            if link_s.startswith('http') and 'google' not in link_s:
                tmp_links.append(link_s)

    # remove duplicate links
    tmp_links = set(tmp_links)

    # write all unique links to file
    with open(output_file_name, 'w') as f:
        for t in tmp_links:
            f.write(t + '\n')
            count += 1

    return count

if __name__ == '__main__':

    # a few general strings that make this more readable and easy to change
    start_url = 'https://en.wikipedia.org/wiki/Pok%C3%A9mon'
    topic = 'pokemon'
    url_file_name = 'relevant_urls.txt'
    URL_CAP = 0

    # This generates the file containing relevant urls and returns the count of urls found. it is immediately checked.
        # (instruction 1)
    # I also introduced a URL cap to limit the number of URLs fetched

    print('Collecting URLs on web site and putting it in file name ', url_file_name)
    if generate_url_file(start_url, topic, url_file_name) < 15:
        print("Unable to find at least 15 related links given the URL:\n", start_url,
              "\neither adjust the url or the topic variable to find relevant links.")
        exit()

    # raw text file name is a common file name used for the next couple of functions
    # is used to create and locate the raw text scraped from web sites
    raw_text_file_name = 'url_text_'

    # scrape data off each page in the file url_file_name (instruction 2)
        # num_urls is the number of urls that didn't throw an error
    print('Scraping data from each URL and putting it in ', raw_text_file_name, '_#.txt')
    num_urls = scrape_pages(url_file_name, raw_text_file_name, URL_CAP)

    # num_urls is the number of files that have been created
    # clean the text in each file (instruction 3)
    print('Cleaning the data and making ', raw_text_file_name, '_clean_#.pickle files')
    clean_pages(num_urls, raw_text_file_name)

    # load each file and find tf-idf for each (instruction 4)
    # this function will return a list of tf_idf dictionaries
    print("Calculating term frequency - inverse document frequency for each file")
    tf_idf_list = create_tf_idfs(num_urls, raw_text_file_name)

    # create a term frequency dict based on the tf-idf found in the last step

    terms = []
    for i in tf_idf_list:
        d = sorted(i.items(), key=lambda x:x[1], reverse=True)
        tes = d[:20]
        for x in tes:
            terms.append(x[0])

    max_displayed = 40
    print("Top ", max_displayed, ' terms:')
    # the 1 in create_termf_dict prevents the frequency from being normalized
    common_terms = create_termf_dict(terms, 1)
    common_terms = sorted(common_terms.items(), key=lambda x: x[1], reverse=True)
    count = 0

    for i in common_terms:
        if count < max_displayed:
            print('\t', count+1, ': ', i[0], ' -> ', i[1])
            count += 1
        else:
            break

