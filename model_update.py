import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import QuantileTransformer


# Import & Cleaning of the dataframe
df = pd.read_csv('db_tmdb.csv')
df = df[df['genre'] !='[]']
df['genre'] = df['genre'].apply(lambda x : pd.eval(x))
df = df[df['release_date'].notna()]
df['release_date'] = df['release_date'].apply(lambda x : int(str(x).split('-')[0]))


# Reset index to avoid problems
df = df.reset_index(drop=True)
df_num = df.select_dtypes('number')


# Quantile Transformer on numerical values
X = df_num.drop(columns = ['id'])
y = df_num['id']

quant_trans = QuantileTransformer(n_quantiles=100, output_distribution='uniform')
quant_trans.fit(X)

X_qt = quant_trans.transform(X)

df_num_std = pd.DataFrame(X_qt, columns= X.columns)
df_num_std['id'] = y


# Multi Binarizer on movies genres
modelMLB = MultiLabelBinarizer()

modelMLB.fit([df['genre'].explode().unique()])

df_genre = pd.DataFrame(modelMLB.transform(df['genre']))
df_genre.columns = modelMLB.classes_


# Concatenation of dataframes & parameter strong modification
df_num_std = pd.concat([df_num_std.drop(columns = 'id')/5 ,df_genre],axis=1)
df_num_std['Animation'] = df_num_std['Animation'] * 2
df_num_std['Comédie'] = df_num_std['Comédie'] * 2
df_num_std['id'] = y


# Model NearestNeighbors
id = df_num_std['id']
X = df_num_std.drop(columns='id')

model_nn = NearestNeighbors(n_neighbors= 3)
model_nn.fit(X)


# Redommandation df creation
list_reco = []
for i in range(len(df_num_std)) :
    liste_indice = model_nn.kneighbors([X.iloc[i]],4)[1][0][1:]
    list_reco.append([df_num_std.iloc[ind]['id'] for ind in liste_indice])

df_list_reco = pd.DataFrame(list_reco,columns=['reco_1','reco_2','reco_3'])

df_reco = pd.concat([df,df_list_reco], join = 'inner',axis=1)
df_reco = df_reco.drop(columns=['popularity','original_title','vote_count'])


# Save in CSV
df_reco.to_csv('db_reco.csv', index = False)