from .base import BaseScaler
import torch


class HeterogeneousScaler(BaseScaler):

    def __init__(self, scalers, splits):

        self.scalers = scalers
        self.splits = splits

    def _get_x_list(self, x):
        x_list = torch.split(x,
                             split_size_or_sections=self.splits,
                             dim=1)
        return x_list

    def fit(self, x, dims=None):
        x_list = self._get_x_list(x)

        for x_i, scaler in zip(x_list, self.scalers):
            scaler.fit(x_i, dims=dims)

    def fit_manual(self):
        for scaler in self.scalers:
            scaler.fit_manual()

    def fit_with_loader(self, loader, dims=None):
        i = 0
        x_list = []
        for batch in iter(loader):
            i += 1
            x_list.append(batch[0])
            if i == 60:
                print('Stopping fitting at batch 60')
                break

        x = torch.cat(x_list)
        self.fit(x, dims)

    def transform(self, x):
        x_list = self._get_x_list(x)
        x_norm_list = []
        for x_i, scaler in zip(x_list, self.scalers):
            x_norm_i = scaler.transform(x_i)
            x_norm_list.append(x_norm_i)

        x_norm = torch.cat(x_norm_list, dim=-1)

        return x_norm

    def inverse_transform(self, x_norm):
        x_norm_list = self._get_x_list(x_norm)
        x_list = []
        for x_norm_i, scaler in zip(x_norm_list, self.scalers):
            x_i = scaler.inverse_transform(x_norm_i)
            x_list.append(x_i)

        x = torch.cat(x_list, dim=-1)

        return x
