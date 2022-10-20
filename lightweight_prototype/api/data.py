import pandas as pd
import gzip
from pathlib import Path


class Data(object):

    def __init__(self):

        with gzip.open('data_sources/civicmine_collated.tsv.gz', 'r') as f:
            self.collated_pd = pd.read_csv(f, sep='\t')

        with gzip.open('data_sources/civicmine_sentences.tsv.gz', 'r') as f:
            self.sentences_pd = pd.read_csv(f, sep='\t')
            self.sentences_pd['upvotes'] = 0
            self.sentences_pd['downvotes'] = 0
            self.sentences_pd['id'] = range(0, len(self.sentences_pd))

        with gzip.open('data_sources/civicmine_unfiltered.tsv.gz', 'r') as f:
            self.unfiltered_pd = pd.read_csv(f, sep='\t')
