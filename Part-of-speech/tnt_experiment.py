import sys
from itertools import izip
from collections import defaultdict

tags = ["ADJ", "NOUN", "PROPN", "VERB"]

def get_precision_and_recall(s_data, g_data, tag):
    """
    Precision and recall for a single POS tag.
    Expressed in terms of true|false positives|negatives.
    """
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0
    correct = 0
    for s_sent, g_sent in zip(s_data, g_data):
        for (_, s_tag), (_, g_tag) in zip(s_sent, g_sent):
            if tag == s_tag:  # system predicts tag...
                if s_tag == g_tag:  # ...and the prediction is correct
                    true_positives += 1
                else:  # ...and the prediction is incorrect
                    false_positives += 1
            else:  # system didn't predict tag...
                if tag == g_tag:  # ...and it should have
                    false_negatives += 1
                else:  # ...and it shouldn't have
                    true_negatives += 1
    precision = true_positives/float((true_positives + false_positives))
    recall = true_positives/float((true_positives + false_negatives))
    return precision, recall

def amt_unknowns(lexicon, test):
    """
    get the amt of unknowns in the set
    """
    unk = sum([int(word not in lexicon)
               for sentence in test
               for word, tag in sentence])
    total = sum([1 for sentence in test for word, tag in sentence])
    return unk/float(total)

def get_accuracy_known_vs_unknown(s_data, g_data, lexicon):
    """
    Separates the accuracy for known and unknown words.
    Known = exists in the training set.
    """
    correct_known = 0
    correct_unknown = 0
    total_known = 0
    total_unknown = 0
    for s_sent, g_sent in zip(s_data, g_data):
        for (word, s_tag), (_, g_tag) in zip(s_sent, g_sent):
            if word in lexicon:
                total_known += 1
                correct_known += int(s_tag == g_tag)
            else:
                total_unknown += 1
                correct_unknown += int(s_tag == g_tag)
    return correct_known/float(total_known), correct_unknown/float(total_unknown)

def get_accuracy(s_data, g_data):
    """
    Caluclates POS tagging accuracy with respect to gold data.
    """
    total = 0
    correct = 0
    for s_sent, g_sent in izip(s_data, g_data):
        for (_, s_tag), (_, g_tag) in izip(s_sent, g_sent):
            total += 1
            if s_tag == g_tag:
                correct += 1
    return correct/float(total)

def load_tagged_file(filename):
    """
    Reads the part-of-speech-tagged data in "word[\t]tag[\n]" format
    as a list of sentences, which are in turn lists of <word, tag> pairs.
    """
    unique_words = set()
    sentences = []
    current = []
    with open(filename) as file:
        for line in file:
            line = line. strip()
            if line:
                if line[:2] != "%%":
                    splitted = line.split()
                    word = splitted[0]
                    tag = splitted[-1]
                    current.append((word, tag))
                    unique_words.add(word)
            else:  # empty line is sentence delimiter
                sentences.append(current)
                current = []
    return sentences, unique_words


def print_stats():
    """
    Starts the program
    """
    langs = ["es", "et", "fi", "nl", "no"]
    data = {}
    for lang in langs:
        training, lexicon = load_tagged_file("data/{}.train".format(lang))
        test, _ = load_tagged_file("data/{}.test".format(lang))
        tagged, _ = load_tagged_file("data/{}.test.tagged".format(lang))
        data[lang] = (lexicon, training, test, tagged)

    # Basic stats
    format_string = "{:2}\t{}\t{}\t{}\t{}\t{}\t{:22}\t{}"
    print format_string.format(
        "lang",
        "#unique",
        "#train",
        "#test",
        "#tagged",
        "%accuracy",
        "%acc known / unknown",
        "%unknowns")
    for lang, datasets in data.items():
        unique_train = len(datasets[0])
        words_train = sum([len(sentence) for sentence in datasets[1]])
        words_test = sum([len(sentence) for sentence in datasets[2]])
        words_tagged = sum([len(sentence) for sentence in datasets[3]])
        accuracy = get_accuracy(datasets[2], datasets[3])
        accuracy_ku = get_accuracy_known_vs_unknown(datasets[2], datasets[3], datasets[0])
        unknowns = amt_unknowns(datasets[0], datasets[2])
        print format_string.format(
            lang,
            unique_train,
            words_train,
            words_test,
            words_tagged,
            accuracy,
            "{:.8f} / {:.8f}".format(accuracy_ku[0], accuracy_ku[1]),
            unknowns)

    precisions = defaultdict(lambda: defaultdict())
    recalls = defaultdict(lambda: defaultdict())

    print
    print "\t{}\t{}\t{}".format("tag", "precision", "recall")
    for lang in langs:
        print lang
        for tag in tags:
            precision, recall = get_precision_and_recall(data[lang][3], data[lang][2], tag)
            precisions[lang][tag] = round(precision * 100, 2)
            recalls[lang][tag] = round(recall * 100, 2)
            print "\t{}\t{}\t{}".format(tag, precision, recall)


def main():
    # partition training
    # create models
    # created the tagged files
    # print stats
    print_stats()

if __name__ == '__main__':
    main()