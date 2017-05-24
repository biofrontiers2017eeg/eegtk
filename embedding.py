from sklearn.decomposition import PCA


class Embedding(object):
    """
    This class calculates a low dimensional embedding based on some training data
    """
    def __init__(self, type="pca", **kwargs):
        """
        initializes embedding options
        :param type: specifies type of embedding
        :type type: string
        :param kwargs: dictionary of optional keyword arguments
        :type kwargs: dict
        """
        self.type = type
        self.n_components = kwargs["n_components"]

    def train(self, train_data):
        """
        trains an embedding based on passed training data
        :param train_data: training data with which to calculate the embedding
        :type train_data: ndarray
        """
        if self.type == "pca":
            pca = PCA(n_components=self.n_components)
            pca.fit(train_data)
            self.pca = pca

    def embed(self, data):
        """
        embeds data according to a trained embedding
        :param data: data to embed
        :type data: ndarray
        :return: embedding of the data
        :rtype: ndarray
        """
        if self.type == "pca":
            return self.pca.transform(data)
