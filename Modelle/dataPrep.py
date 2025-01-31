import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt

imputer = KNNImputer(n_neighbors=5, weights='uniform', metric='nan_euclidean')

#df = pd.read_csv('data_raw.csv')
#df = pd.read_csv('data_2.csv')
df = pd.read_csv('data_leipzig_all.csv')

df = df.replace(r'9999|Unbenannt|Unbekannt|9999.99', np.nan, regex=True)
df["width"] = df["width"].replace(9999.99, np.nan)

df["highway"] = df["highway"].replace("unclassified", np.nan)


df["lanes"] = df["lanes"].replace(9999, np.nan)
df["surface"] = df["surface"].replace("cobblestone:flattened", "cobblestone")
df["surface"] = df["surface"].replace("unhewn_cobblestone", "cobblestone")
df["surface"] = df["surface"].replace("pebblestone;", "cobblestone")
df["surface"] = df["surface"].replace("sett", "cobblestone")
df["surface"] = df["surface"].replace("paving_stones", "cobblestone")
df["surface"] = df["surface"].replace("paving_stones:lanes", "cobblestone")
df["surface"] = df["surface"].replace("paving_stones:20", "cobblestone")

#vlt concrete replace
df["surface"] = df["surface"].replace("concrete:lanes", "concrete")
df["surface"] = df["surface"].replace("concrete:plates", "concrete")
df["surface"] = df["surface"].replace("concrete:slabs", "concrete")
df["surface"] = df["surface"].replace("concrete:tiles", "concrete")
df["surface"] = df["surface"].replace("concrete_slabs", "concrete")

df["smoothness"] = df["smoothness"].replace("^g", np.nan)

df["sidewalk"] = df["sidewalk"].replace("none", "no")

df["maxspeed"] = df["maxspeed"].replace("DE:urban", "50")
df["maxspeed"] = df["maxspeed"].replace(9999, np.nan)

df["cycleway"] = df["cycleway"].replace("y", "yes")

df["bicycle"] = df["bicycle"].replace("unknown", np.nan)

df["width"].replace(to_replace=" m", value="", regex=True, inplace=True)
df["width"] = df["width"].replace("about 2m", "2")
df["width"].replace(to_replace="m", value="", regex=True, inplace=True)
df["width"].replace(to_replace=",", value=".", regex=True, inplace=True)
df["width"].replace(to_replace=">", value="", regex=True, inplace=True)

print("id", df['id'].unique())
print("name", df['name'].unique())
print("ref", df['ref'].unique())
print("highway", df['highway'].unique())
print("surface", df['surface'].unique())
print("maxspeed", df['maxspeed'].unique())
print("lanes", df['lanes'].unique())
print("sidewalk", df['sidewalk'].unique())
print("cycleway", df['cycleway'].unique())
print("bicycle", df['bicycle'].unique())
print("hazard", df['hazard'].unique())
print("width", df['width'].unique())
print("smoothness", df['smoothness'].unique())

df = df.drop(["name", "ref", "hazard"], axis=1)

"""""
#Correlation
corrdf = df[["width", "lanes"]].dropna()
print(corrdf)
corrdf.width = corrdf.width.astype(float)
corrdf.lanes = corrdf.lanes.astype(float)
matrix = corrdf.corr()
print(matrix)
plt.imshow(matrix, cmap='Blues')
plt.colorbar()
variables = []
for i in matrix.columns:
    variables.append(i)
plt.xticks(range(len(matrix)), variables, rotation=45, ha='right')
plt.yticks(range(len(matrix)), variables)
plt.show()

#Scatter Plot
plt.scatter(corrdf["lanes"], corrdf["width"])
b, a = np.polyfit(corrdf["lanes"], corrdf["width"], deg=1)

# Create sequence of 100 numbers from 0 to 100
xseq = np.linspace(0, 10, num=100)
plt.plot(xseq, a + b * xseq, color="k", lw=2.5)
plt.show()
"""

n_miss = df["highway"].isnull().sum()
print('> Highway Missing: %d (%.1f%%)' % (n_miss, (n_miss / df.shape[0] * 100)))
#df["highway"] = df["highway"].astype('category').cat.codes
one_hot = pd.get_dummies(df["highway"], prefix="highway")
df = df.drop("highway", axis = 1)
df = df.join(one_hot)

n_miss = df["surface"].isnull().sum()
print('> Surface Missing: %d (%.1f%%)' % (n_miss, (n_miss / df.shape[0] * 100)))
#df["surface"] = df["surface"].astype('category').cat.codes
one_hot = pd.get_dummies(df["surface"], prefix="surface")
#print(one_hot)
df = df.drop("surface", axis = 1)
df = df.join(one_hot)
print(df)

n_miss = df["smoothness"].isnull().sum()
print('> Smoothness Missing: %d (%.1f%%)' % (n_miss, (n_miss / df.shape[0] * 100)))
#df["smoothness"] = df["smoothness"].astype('category').cat.codes
one_hot = pd.get_dummies(df["smoothness"], prefix="smoothness")
df = df.drop("smoothness", axis = 1)
df = df.join(one_hot)

n_miss = df["maxspeed"].isnull().sum()
print('> Maxspeed Missing: %d (%.1f%%)' % (n_miss, (n_miss / df.shape[0] * 100)))
df["maxspeed"] =  pd.to_numeric(df['maxspeed'], errors='coerce')

n_miss = df["lanes"].isnull().sum()
print('> Lanes Missing: %d (%.1f%%)' % (n_miss, (n_miss / df.shape[0] * 100)))
df["lanes"] =  pd.to_numeric(df['lanes'], errors='coerce')

n_miss = df["sidewalk"].isnull().sum()
print('> Sidewalk Missing: %d (%.1f%%)' % (n_miss, (n_miss / df.shape[0] * 100)))
one_hot = pd.get_dummies(df["sidewalk"], prefix="sidewalk")
df = df.drop("sidewalk", axis = 1)
df = df.join(one_hot)


n_miss = df["cycleway"].isnull().sum()
print('> cycleway Missing: %d (%.1f%%)' % (n_miss, (n_miss / df.shape[0] * 100)))
#df["cycleway"] = df["cycleway"].astype('category').cat.codes
one_hot = pd.get_dummies(df["cycleway"], prefix="cycleway")
df = df.drop("cycleway", axis = 1)
df = df.join(one_hot)

n_miss = df["bicycle"].isnull().sum()
print('> Bicycle Missing: %d (%.1f%%)' % (n_miss, (n_miss / df.shape[0] * 100)))
#df["bicycle"] = df["bicycle"].astype('category').cat.codes
one_hot = pd.get_dummies(df["bicycle"], prefix="bicycle")
df = df.drop("bicycle", axis = 1)
df = df.join(one_hot)

n_miss = df["width"].isnull().sum()
print('> Width Missing: %d (%.1f%%)' % (n_miss, (n_miss / df.shape[0] * 100)))
df["width"] =  pd.to_numeric(df['width'], errors='coerce')

df["unfall"] = df["unfall"].astype('category').cat.codes

df = df.replace(-1, np.nan)

df_y = df["unfall"]
df_x = df.drop(["unfall"], axis=1)

#Correlation of all features
corrdf = df_x.dropna()
print(corrdf)
matrix = corrdf.corr()
matrix = matrix.dropna(axis=1, how='all')
matrix = matrix.dropna(axis=0, how='all')
print(matrix)
plt.imshow(matrix, cmap='Blues')
plt.colorbar()
variables = []
for i in matrix.columns:
    variables.append(i)
plt.xticks(range(len(matrix)), variables, rotation=45, ha='right')
plt.yticks(range(len(matrix)), variables)
#plt.show()


df_with_empty = df_x
df_with_empty["y"] = df_y

df_with_empty.to_csv('data_with_empty_latest_with_id.csv', index=False)
print(df.columns)


imputer.fit(df_x)
df_x_knn = pd.DataFrame(imputer.transform(df_x), columns=df_x.columns, index=df_x.index)

df_x_knn["y"] = df_y

print(df_x_knn)

df_x_knn.to_csv('data_knn_latest_with_id.csv', index=False)  