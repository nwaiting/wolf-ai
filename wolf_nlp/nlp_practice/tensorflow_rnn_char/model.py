#coding=utf-8


class RNNChar(object):
    def __init__(self, num_classes,
                time_steps=28,
                time_inputs=28,
                hidden_size=128,
                num_layers=2,
                learning_rate=0.001
                grad_clip=5,
                sampling=False,
                training_keep_prob=0.5,
                using_embedding=False,
                embedding_size=300
                ):
    self.num_classes_ = num_classes
    self.time_steps_ = time_steps
    self.time_inputs_ = time_inputs
    self.hidden_size_ = hidden_size
    self.num_layers_ = num_layers
    self.learning_rate_ = learning_rate
    self.grad_clip_ = grad_clip
    self.sampling_ = sampling
    self.training_keep_prob_ = training_keep_prob
    self.using_embedding_ = using_embedding
    self.embedding_size_ = embedding_size
