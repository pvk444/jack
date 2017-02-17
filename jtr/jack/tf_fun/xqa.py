import tensorflow as tf


def xqa_min_crossentropy_loss(start_scores, end_scores, answer_span, answer_to_question):
    """
    very common XQA loss function
    """
    start, end = [tf.squeeze(t, 1) for t in tf.split(answer_span, 2, 1)]

    batch_size1 = tf.shape(start)[0]
    batch_size2 = tf.unstack(tf.shape(start_scores))[0]
    is_aligned = tf.equal(batch_size1, batch_size2)

    start_scores = tf.cond(is_aligned, lambda: start_scores, lambda: tf.gather(start_scores, answer_to_question))
    end_scores = tf.cond(is_aligned, lambda: end_scores, lambda: tf.gather(end_scores, answer_to_question))
    loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=start_scores,
            labels=start) + \
           tf.nn.sparse_softmax_cross_entropy_with_logits(logits=end_scores,
                   labels=end)
    loss = tf.segment_min(loss, answer_to_question)
    return [tf.reduce_mean(loss)]
