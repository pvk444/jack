# -*- coding: utf-8 -*-

from jtr.pipelines import pipeline


def preprocess_with_pipeline(data, vocab, target_vocab, test_time=False, negsamples=0,
                             tokenization=True, use_single_support=True, sepvocab=True):
    corpus = {"support": [], "question": [], "candidates": [], "ids": []}
    if not test_time:
        corpus["answers"] = []
    for i, xy in enumerate(data):
        x, y = (xy, None) if test_time else xy

        corpus["support"] += [x.support[0] if use_single_support else x.support]
        corpus['ids'].append(i)
        corpus["question"].append(x.question)
        corpus["candidates"].append(x.atomic_candidates)
        assert len(y) == 1
        if not test_time:
            corpus["answers"].append(y[0].text)

    corpus, train_vocab, answer_vocab, train_candidates_vocab =\
        pipeline(corpus, vocab, target_vocab, sepvocab=sepvocab, test_time=test_time,
                 tokenization=tokenization, cache_fun=True, map_to_target=False, normalize=True,
                 **({'negsamples': negsamples} if not test_time else {}))
    return corpus, train_vocab, answer_vocab, train_candidates_vocab
