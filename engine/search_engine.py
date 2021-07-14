from math import log
from collections import defaultdict
from components.print_log import print_log, print_progress
from tokenize.tokenizer import tokenizer


class SearchEngine:
    def __init__(self, product_data: dict):
        self.product_data = product_data
        self.tokenized_data = self._generate_tokenized_data()
        self.inverted_index = self._generate_inverted_index()
        self.tf, self.df = self._generate_tf_df()

    def _generate_tokenized_data(self):
        print_log('Tokenizing the text data...\n')
        tokenized_data: dict = defaultdict(list)
        length = len(self.product_data)
        i = 0
        for pid, name in self.product_data.items():
            print_progress(100, length, i)
            tokenized_data[pid] = tokenizer(name)
            i += 1

        print_log('Successfully tokenized the text data!\n')

        return tokenized_data

    def _generate_inverted_index(self):
        print_log('Building a dictionary of inverted index...')

        inverted_index: dict = defaultdict(list)
        length = len(self.tokenized_data)
        i = 0
        for pid, tokens in self.tokenized_data.items():
            print_progress(100, length, i)
            for token in tokens:
                inverted_index[token].append(pid)
            i += 1

        print_log('Successfully built the dictionary of inverted index!\n')

        return inverted_index

    def _generate_tf_df(self):
        print_log('Generating dictionaries of term_frequency and document_frequency...')

        tf: dict = defaultdict(dict)
        df: dict = defaultdict(int)
        length = len(self.tokenized_data)
        i = 0
        for pid, tokens in self.tokenized_data.items():
            print_progress(100, length, i)
            for token in tokens:
                if tf[pid].get(token) is None:
                    tf[pid][token] = 1
                else:
                    tf[pid][token] += 1

            for token in set(tokens):
                df[token] += 1
            i += 1

        print_log('Successfully generated the dictionaries of term_frequency and document_frequency!\n')

        return tf, df

    def _get_tf_idf(self, pid: int, tokens: list):
        tf_idf: float = 0

        for token in tokens:
            tf_idf += (self.tf[pid][token] * (log(len(self.tf) / (1 + self.df[token])) + 1))

        return tf_idf

    def _get_intersection(self, tokens: list):
        intersection: list = self.inverted_index[tokens[0]]

        if len(tokens) >= 1:
            for i in range(1, len(tokens)):
                intersection = list(set(intersection) & set(self.inverted_index[tokens[i]]))

        return intersection

    def _get_matched_pid(self, query: str):
        tokens: list = list(set(tokenizer(query)))
        products: list = self._get_intersection(tokens)
        tf_idf: dict = {}
        total_tf_idf: float = 0

        for pid in products:
            tf_idf[pid] = self._get_tf_idf(pid, tokens)
            total_tf_idf += tf_idf[pid]

        for pid, tf_idf_value in tf_idf.items():
            tf_idf[pid] = tf_idf_value / total_tf_idf

        if len(tf_idf) > 20:
            return sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)[:20]
        else:
            return sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)

    def get_search_result(self, query: str):
        matched_pid = self._get_matched_pid(query)

        search_result: dict = {'data': []}

        for pid, score in matched_pid:
            data = {'pid': str(pid),
                    'name': self.product_data[pid],
                    'score': round(score, 5)}
            search_result['data'].append(data)

        return search_result
