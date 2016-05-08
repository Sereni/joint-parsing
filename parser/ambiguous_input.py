from conllz import read_conllz
from sdp import read_sentences, load_model, parse, s2conll, c2s, parse_with_feats
from metrics import las


def run_experiment(gold_path, corpus_path, model, vector, output_path):

    gold_sentences = read_conllz(gold_path)
    # gold_sentences = read_sentences(gold_path)  # use with unambiguous gold corpora
    ambiguous_sentences = read_conllz(corpus_path, signals=True)

    feats = ["b0.pos", "s0.pos", "b1.pos", "s1.pos", "ld(b0).pos",  # no form no deprel
            "s0.pos b0.pos", "s0.form b0.pos", "b2.pos", "b3.pos",
            "s0.lemma", "b0.lemma", "morph"]

    print('Loading model...', end='')
    guide = load_model(model, vector)
    print('done')

    output = open(output_path, 'w')

    counter = 1
    for gold in gold_sentences:

        if counter % 1 == 0:
            print('Parsing sentence %d' % counter)

        output.write('# Gold parse:\n' + s2conll(gold[1:]))  # write the gold sentence

        scored_sentences = []
        # work with alternatives generated from one gold sentence
        current_sentence = next(ambiguous_sentences)
        while current_sentence is not None:
            parsed = c2s(parse_with_feats(current_sentence, guide, feats))  # parse the sentence
            score = las(parsed, gold[1:])
            scored_sentences.append((score, parsed))
            current_sentence = next(ambiguous_sentences)

        # write sentences in descending order of score
        for s in sorted(scored_sentences, key=lambda x: x[0], reverse=True):
            output.write('\n# LAS: ' + str(s[0]) + '\n' + s2conll(s[1]))

        output.write('\n')
        counter += 1

    output.close()

# todo parameters please
if __name__ == '__main__':
    run_experiment(

        # # crimean
        gold_path='/Users/Sereni/PycharmProjects/Joint Parsing/parser/data/crimean/puupankki.crh.conllu',
        corpus_path='/Users/Sereni/PycharmProjects/Joint Parsing/parser/data/crimean/puupankki.crh.x-best.conllz',

        # tuvan
        # gold_path='/Users/Sereni/PycharmProjects/Joint Parsing/parser/data/tuvan/puupankki.tyv.conllu',
        # corpus_path='/Users/Sereni/PycharmProjects/Joint Parsing/parser/data/tuvan/puupankki.tyv.x-best.conllz',

        # # kazakh
        # gold_path='/Users/Sereni/PycharmProjects/Joint Parsing/parser/data/kazakh/puupankki.conllx_test',
        # corpus_path='/Users/Sereni/PycharmProjects/Joint Parsing/parser/data/kazakh/xbest.conllz_test',

        model='/Users/Sereni/PycharmProjects/Joint Parsing/parser/models/kazakh_DT/model_for_puupankki.conllx_train.pkl',
        vector='/Users/Sereni/PycharmProjects/Joint Parsing/parser/models/kazakh_DT/vectorizer_for_puupankki.conllx_train.pkl',

        output_path='/Users/Sereni/PycharmProjects/Joint Parsing/parser/data/results/DT_experiments/crh_xbest_DT'


    )