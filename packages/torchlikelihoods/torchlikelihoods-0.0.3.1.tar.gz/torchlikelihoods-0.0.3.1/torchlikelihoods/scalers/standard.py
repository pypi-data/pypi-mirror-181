from .base import BaseScaler
import torch

class StandardScaler(BaseScaler):

    def __init__(self):
        self.mu_ = None
        self.scale_ = None

    def fit(self, x, dims=None):
        if isinstance(dims, tuple):
            self.mu_ = x.mean(dims[0], keepdims=True)
            self.scale_ = x.std(dims, keepdims=True)
            for dim in dims[1:]:
                self.mu_ =  self.mu_.mean(dim, keepdims=True)
        elif isinstance(dims, list):
            raise Exception('dims should be None or a tuple!')
        else:
            self.mu_ = x.mean()
            self.scale_ = x.std()

    def fit_manual(self):
        self.mu_ = 0.0
        self.scale_ = 1.0

    def fit_with_loader(self, loader, dims=None):
        i = 0
        x_list = []
        for batch in iter(loader):
            # print(f"i: {i} {batch[0].mean()}")
            i += 1
            x_list.append(batch[0])
            if i == 60:
                print('Stopping fitting at batch 60')
                break

        x = torch.cat(x_list)

        self.fit(x, dims)

    def transform(self, x):
        return (x - self.mu_) / self.scale_

    def inverse_transform(self, x_norm):
        return x_norm * self.scale_ + self.mu_

