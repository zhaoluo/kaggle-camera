import numpy as np
from torch.utils.data.sampler import Sampler
from sklearn.model_selection import StratifiedShuffleSplit

from rng import RNG


class StratifiedSampler(Sampler):
    """Stratified Sampling
    Provides equal representation of target classes in each batch

    Reference
    ---------
    https://github.com/ncullen93/torchsample/blob/master/torchsample/samplers.py#L22
    """
    def __init__(self, class_vector, batch_size):
        """
        Arguments
        ---------
        class_vector : torch tensor
            a vector of class labels
        batch_size : integer
            batch_size
        """
        super(StratifiedSampler, self).__init__(class_vector)
        self.n_splits = int(class_vector.shape[0] / batch_size)
        self.class_vector = class_vector

    def gen_sample_array(self):
        rng = RNG()
        s = StratifiedShuffleSplit(n_splits=self.n_splits, test_size=0.5)
        X = rng.randn(self.class_vector.shape[0], 2)
        y = self.class_vector
        s.get_n_splits(X, y)

        train_index, test_index = next(s.split(X, y))
        return np.hstack([train_index, test_index])

    def __iter__(self):
        return iter(self.gen_sample_array())

    def __len__(self):
        return len(self.class_vector)
