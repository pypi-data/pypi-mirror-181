from .base import BaseScaler


class IdentityScaler(BaseScaler):
    def __init__(self):
        return

    def fit(self, x, dims=None):
        return

    def fit_manual(self):
        return

    def fit_with_loader(self, loader):
        return

    def transform(self, x):
        return x

    def inverse_transform(self, x_norm):
        return x_norm
