from sklearn.decomposition import PCA


class Embedding(object):
    def __init__(self, type="pca", ):
        self.type = type

    def train(self, train_data):
        if self.type == "pca":
            pca = PCA()
            pca.fit(train_data)
            self.pca= pca

    def embed(self, train_data):
        if self.type == "pca":
            return self.pca.transform(train_data)
