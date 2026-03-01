import numpy as np
import matplotlib.pyplot as plt



class LCG:
    def __init__(self, seed, a=16807, c=2147483647, m=2 ** 32):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):

        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m



def poisson_lambda(lambda_param, n, lcg):
    result = []
    for _ in range(n):
        L = np.exp(-lambda_param)
        k = 0
        p = 1
        while p > L:
            k += 1
            u = lcg.next()
            p *= u
        result.append(k - 1)
    return result



def normal(mu, sigma, n, lcg):
    result = []
    for _ in range(n // 2):
        u1 = lcg.next()
        u2 = lcg.next()
        z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        z1 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)
        result.append(mu + z0 * sigma)
        result.append(mu + z1 * sigma)
    return result[:n]



def generate_distribution(distribution_type, n, param1, param2, use_seed=False, seed_value=None):

    if use_seed:
        lcg = LCG(seed_value)
    else:
        lcg = LCG(12345)

    if distribution_type == "poisson":
        return poisson_lambda(param1, n, lcg)
    elif distribution_type == "normal":
        return normal(param1, param2, n, lcg)
    else:
        raise ValueError("Nieobsługiwany typ rozkładu.")



def plot_histogram(data, distribution_name):
    plt.hist(data, bins=30, density=True, alpha=0.75)
    plt.title(f'Histogram rozkładu {distribution_name}')
    plt.xlabel('Wartość')
    plt.ylabel('Prawdopodobieństwo')
    plt.grid(True)
    plt.show()



def main():

    lambda_poisson = 5
    mu_normal = 0
    sigma_normal = 1
    n = 10000


    use_seed = True
    seed_value = 42

    poisson_data = generate_distribution("poisson", n, lambda_poisson, None, use_seed, seed_value)
    plot_histogram(poisson_data, "Poissona")


    normal_data = generate_distribution("normal", n, mu_normal, sigma_normal, use_seed, seed_value)
    plot_histogram(normal_data, "Normalnego (Gaussa)")


if __name__ == "__main__":
    main()