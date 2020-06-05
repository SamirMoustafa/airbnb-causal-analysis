import pandas as pd
from sklearn.preprocessing import LabelEncoder

from src.nlp.tf_idf import tfidf_tsne

numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']


def airbnb_data_clean(df):
    """
    Clean the airbnb dataset and make some encoding on the text

    :param df: airbnb data-frame that contains decried features
    :return: clean and numerical version of the data-frame
    """

    # skip cleaning if the provided data-frame contains numeric values
    df_types = df.select_dtypes(include=numerics)
    if df_types.shape[1] == df.shape[1]:
        return df

    # Encode target labels with value between 0 and n_classes-1 for unique text
    le = LabelEncoder()

    # drop all columns that have nan's at all of it's row
    df = df.dropna(axis=1, how='all')

    # drop unnecessary and unique values form data
    df = df.drop(['id', 'host_id', 'host_name'], axis=1)

    # use term frequency–inverse document frequency
    # then use t-distributed stochastic neighbor embedding
    # for embedding the text to single number
    df['name'] = tfidf_tsne(df['name'].astype('U'), map_dim=1)

    # to check that there exit a few values to the feature use
    # `df['room_type'].unique()`
    df['room_type'] = le.fit_transform(df['room_type'].values)
    df['neighbourhood'] = le.fit_transform(df['neighbourhood'].values)

    # subtract the current day from the mention day
    df['last_review'] = pd.to_datetime(df['last_review'])
    df['last_review'] = (pd.Timestamp.now().normalize() - df['last_review']).dt.days

    return df
