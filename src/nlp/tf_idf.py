from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE

def tfidf_tsne(X, max_dim=50, map_dim=2):
    vectoring = TfidfVectorizer(analyzer='char_wb', max_features=max_dim)
    vectoring.fit(X)
    X = vectoring.transform(X)
    tsne = TSNE(n_components=map_dim)
    X = tsne.fit_transform(X)
    return X


if __name__ == '__main__':
    corpus = ['red', 'red', 'red', 'blue', 'green']

    X = tfidf_tsne(corpus, map_dim=1)
    print(X)