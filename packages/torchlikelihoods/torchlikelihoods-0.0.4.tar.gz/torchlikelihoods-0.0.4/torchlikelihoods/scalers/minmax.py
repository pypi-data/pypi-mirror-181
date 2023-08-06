from .base import BaseScaler
import torch
class MinMaxScaler(BaseScaler):
    def __init__(self, feature_range):
        assert feature_range[0] == 0
        assert feature_range[1] == 1
        self.min_ = feature_range[0]
        self.max_ = feature_range[1]
        self.min_data = None
        self.max_data = None

    def reset(self):
        self.min_data = None
        self.max_data = None

    def fit(self, x, dims):
        assert isinstance(x, torch.Tensor)

        if isinstance(dims, tuple):
            min_data = x.min(dims[0],keepdim=True)[0]
            max_data = x.max(dims[0],keepdim=True)[0]
            for dim in dims[1:]:
                min_data = min_data.min(dim,keepdim=True)[0]
                max_data = max_data.max(dim,keepdim=True)[0]
        else:
            min_data = x.min()
            max_data = x.max()

        if self.min_data is None:
            self.min_data = min_data
            self.max_data = max_data

        else:
            idx_new = torch.where(min_data < self.min_data)
            print(idx_new)
            print(self.min_data)
            print(min_data)
            self.min_data[idx_new] = min_data[idx_new]

            idx_new = torch.where(max_data > self.max_data)
            self.max_data[idx_new] = max_data[idx_new]
    def fit_manual(self):
        self.min_data = 0.0
        self.max_data = 1.0
    def fit_with_loader(self, loader):
        i = 0
        for batch in iter(loader):
            i += 1
            self.fit(batch[0])

            if i == 60: break

    def transform(self, x):
        diff = self.max_data - self.min_data
        x_norm = (x - self.min_data) / diff  # [0,1]
        return x_norm

    def inverse_transform(self, x_norm):
        diff = self.max_data - self.min_data
        x = x_norm * diff + self.min_data
        return x
