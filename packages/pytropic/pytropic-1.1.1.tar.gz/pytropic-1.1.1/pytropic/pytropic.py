# -*- coding: utf-8 -*-
import collections
import json
import math
import warnings

"""Main module."""


def sliding(string, n):
    for i in range(len(string) - n + 1):
        yield string[i : i + n]


class Model(object):
    """A counter for ngrams"""

    def __init__(self, size=2.0, name=None):
        self.size = size
        self.default_count = 0.5  # make a parameter?
        self.counter = collections.Counter()
        self.total = 0
        self.name = name

    def __repr__(self):
        return "<Model {}>".format(self.name)

    def update(self, string, muliplier=1):
        """
        Public: update a counter with a string, and a multiplier

        Examples

        counter = NGramCounter(2)
        counter.update_with_multiplier('01234', 1)

        string: The String to update with
        multiplier: The Integer describing how much weight (will often be 1)
        """
        for substr in sliding(string, self.size):
            self.counter[substr] += muliplier
            self.total += muliplier

    def count(self, ngram):
        """
        Public: get count for string, with default

         Examples

         counter = NGramCounter.new(2)
         counter.update('01234')
         counter.count('01')
         #=> 1
         counter.count('bob')
         #=> 0.5

         ngram: The String to check

        """
        return self.counter.get(ngram, self.default_count)

    def log_prob(self, key):
        if self.total == 0 or not key:
            return -math.inf
        count = self.count(key)
        return math.log(count, 2.0) - math.log(self.total, 2.0)

    def dump(self, io):
        for key, value in self.counter.items():
            io.write("{}\t{}\t{}\n".format(self.size, key, value))

    def dump_json(self, io):
        for key, value in self.counter.items():
            io.write(
                json.dumps(
                    {
                        "model_name": self.name,
                        "ngram_size": self.size,
                        "ngram": key,
                        "count": value,
                        "log_prob": self.log_prob(key),
                        "entropy": -self.log_prob(key),
                        "total": self.total,
                    }
                )
                + "\n"
            )

    def predict(self, string):
        n_ngrams = 0
        log_prob_total = 0.0
        for ngram in sliding(string, self.size):
            n_ngrams += 1
            log_prob_total += self.log_prob(ngram)
        log_prob_average = log_prob_total / n_ngrams
        return {
            "log_prob_total": log_prob_total,
            "log_prob_average": log_prob_average,
            "size": int(n_ngrams),
        }

    def entropy(self, string):
        return -self.predict(string)["log_prob_average"]

    def read(self, io):
        n = 0
        for line in io:
            n += 1
            try:
                _, ngram, count = line.strip().split("\t")
                count = float(count)
                self.counter[ngram] += count
                self.total += count
            except ValueError as err:
                warnings.warn("Invalid line at {}. Error: {}".format(n, err))

    def read_json(self, io, count_key="count", ngram_key="ngram"):
        n = 0
        for line in io:
            n += 1
            data = json.loads(line.strip())
            count = data[count_key]
            ngram = data[ngram_key]
            self.counter[ngram] += count
            self.total += count

    def read_from_string(self, string):
        n = 0
        for line in string.split("\n"):
            n += 1
            _, ngram, count = line.strip().split("\t")
            count = float(count)
            self.counter[ngram] += count
            self.total += count

    def train(self, io):
        for line in io:
            self.update(line.strip())

    def train_with_multiplier(self, io):
        n = 0
        for line in io:
            n += 1
            try:
                text, count = line.strip().split("\t")
                count = float(count)
                self.update(text, count)
            except ValueError as err:
                warnings.warn("Invalid line at {}. Error: {}".format(n, err))


class MultiModel(object):
    """A collection of models"""

    def __init__(self, models={}):
        self.models = models

    def __repr__(self):
        return "<MultiModel({} models)>".format(len(self.models))

    def read_json(
        self,
        io,
        count_key="count",
        ngram_key="ngram",
        model_name_key="model_name",
        ngram_size_key="ngram_size",
        ngram_size=None,
    ):
        """
        Public: read a json file into a MultiModel

        The file should be a jsonl file, with each line containing a json object with the following
        keys:
            count: the count of the ngram
            ngram: the ngram
            model_name: the name of the model
            ngram_size: the size of the ngram

        This will create a model for each model_name found in the file, and add the ngram data for that model.

        io: The IO object to read from
        count_key: The String key for the count
        ngram_key: The String key for the ngram
        model_name_key: The String key for the model name
        ngram_size_key: The String key for the ngram size
        ngram_size: The Integer size of the ngrams. If not provided, will be inferred from the data

        Returns: A MultiModel object

        Notes: This is additive,it will not overwrite, but will change, existing data in the MultiModel


        """
        models = {}
        for line in io:
            data = json.loads(line.strip())
            ngram = data[ngram_key]
            count = data[count_key]
            model_name = data[model_name_key]
            ngram_size = data[ngram_size_key]
            if model_name not in models:
                models[model_name] = Model(size=ngram_size, name=model_name)
            model = models[model_name]
            model.update(ngram, count)
        self.models = models

    def predict(self, string):
        """
        Public: Returns a sorted list of predictions for the string

        string: The String to predict

        Returns: A list of tuples of the form (model_name, prediction), sorted by the prediction's log_prob_average

        Example:

        >>> m = pytropic.MultiModel({"model1": pytropic.Model(size=3), "model2": pytropic.Model(size=3)})
        >>> m.models["model1"].update("abc", 1000)
        >>> m.models["model2"].update("abc", 1)
        >>> m.models["model1"].update("def", 1)
        >>> m.models["model2"].update("def", 1000)
        >>> m.predict("abc")[0][0] # should return 'model1' first
        'model1'
        >>> m.predict("def")[0][0] # should return 'model2' first
        'model2'

        """
        predicts = [
            (model_name, m.predict(string)) for model_name, m in self.models.items()
        ]
        # do a non-destructive sort
        sorted_predicts = sorted(predicts, key=lambda x: -x[1]["log_prob_average"])
        return sorted_predicts

    def entropy(self, string):
        """
        Public: Returns a sorted list of (model_name, entropy) for the string, sorted by entropy ascending

        string: The String to predict

        Returns: A list of tuples of the form (model_name, entropy), sorted by the entropy

        """
        predictions = self.predict(string)
        return [
            (model_name, -prediction["log_prob_average"])
            for model_name, prediction in predictions
        ]

    def lowest_entropy_model(self, string):
        """
        Public: Returns the model name with the lowest entropy for the string

        string: The String to predict

        Returns: The String model name with the lowest entropy
        """
        entropies = self.entropy(string)
        return entropies[0]

    def differences(self, string):
        """
        Public: Returns a list of (difference, model_name_1, model_name_2) for the string for each pair of models
        in a sorted entropy list

        string: The String to predict

        Returns: A list of tuples of the form (difference, model_name_1, model_name_2) for each pair of models
        """
        entropies = self.entropy(string)
        pairs = zip(entropies, entropies[1:])
        return [
            (prev_entropy - entropy, model_name_1, model_name_2)
            for (model_name_1, entropy), (model_name_2, prev_entropy) in pairs
        ]

    def difference(self, string):
        """
        Public: Returns the difference between the first two models in the sorted entropy list

        string: The String to predict

        Returns: The Float difference between the first two models in the sorted entropy list

        """
        return self.differences(string)[0]
