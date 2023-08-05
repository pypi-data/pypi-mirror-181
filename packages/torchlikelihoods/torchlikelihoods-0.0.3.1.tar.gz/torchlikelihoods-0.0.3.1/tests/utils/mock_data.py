import torch

from torchlikelihoods import likelihood_dict
data_generator = {
    'normal': lambda n, d: torch.randn((n, d)),
    'cat': lambda n, d: torch.randint(0, d, (n, 1)),
    'cb': lambda n, d: torch.rand((n, d)),
    'ber': lambda n, d: torch.randint(0, 2, (n, d)),
}



def create_data(num_samples, lik_info):
    x_list = []
    x_one_hot_list = []
    for key, value in lik_info:
        x_i = data_generator[key](num_samples, value)
        x_list.append(x_i)
        if key == 'cat':
            x_one_hot = torch.nn.functional.one_hot(x_i.flatten(), num_classes=value)
            x_one_hot_list.append(x_one_hot)
        else:
            x_one_hot_list.append(x_i)

    x = torch.cat(x_list, dim=1)
    x_one_hot = torch.cat(x_one_hot_list, dim=1)


    return x, x_one_hot


def create_image_data( num_samples, width, height, channels):
    return torch.randint(0, 256, (num_samples, channels, width, height))



def get_likelihoods(lik_info):
    likelihoods = []
    for (lik_name_i, domain_size_i) in lik_info:
        assert isinstance(domain_size_i, int)
        lik = likelihood_dict[lik_name_i](domain_size_i)
        likelihoods.append(lik)
    return likelihoods