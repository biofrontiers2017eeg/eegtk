from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


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
        if "n_components" in kwargs:
            self.n_components = kwargs["n_components"]
        if "label_data" in kwargs:
            self.label_data = kwargs["label_data"]

    def train(self, train_data, label_data=False):
        """
        trains an embedding based on passed training data
        :param train_data: training data with which to calculate the embedding
        :type train_data: ndarray
        """
        if self.type == "pca":
            pca = PCA(n_components=self.n_components)
            pca.fit(train_data)
            self.pca = pca
        if self.type == "lda":
            """
            label_data : 1xn_sample, labels the data
            train_data : n_samplexn_features
            """
            if label_data:
                lda = LinearDiscriminantAnalysis(n_components=self.n_components)
                lda.fit(train_data, label_data)
                self.lda = lda

    def embed(self, data):
        """
        embeds data according to a trained embedding
        data: n_Samplesxn_features
        return: n_SamplesxNewfeatures
        :param data: data to embed
        :type data: ndarray
        :return: embedding of the data
        :rtype: ndarray
        """
        if self.type == "pca":
            return self.pca.transform(data)
        if self.type == "lda":
            return self.lda.transform(data)
