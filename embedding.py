from sklearn.decomposition import PCA


class Embedding(object):
    def __init__(self, type="pca", **kwargs):
        self.type = type
        self.n_components = kwargs["n_components"]

    def train(self, train_data):
        if self.type == "pca":
            pca = PCA(n_components=self.n_components)
            pca.fit(train_data)
            self.pca = pca

    def embed(self, train_data):
        if self.type == "pca":
            return self.pca.transform(train_data)
