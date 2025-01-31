import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import shap
import xgboost
from catboost import CatBoostClassifier
from interpret.glassbox import ExplainableBoostingClassifier
from interpret import show_link
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score


#df = pd.read_csv('data_knn.csv')
#df = pd.read_csv('data_with_empty_2.csv')
df = pd.read_csv('data_with_empty_latest.csv')


df_all = pd.read_csv('data_with_empty_latest_with_id.csv')
id_col = df_all["id"]

df_all = df_all.drop(["id"], axis=1)

df_all = df_all.reindex(columns=df.columns, fill_value=0)
all_leipzig_x = df_all.loc[:, df_all.columns != 'y']
all_leipzig_y = df_all["y"]

X_train, X_test, y_train, y_test = train_test_split(
    df.loc[:, df.columns != 'y'], df["y"], test_size=0.33, random_state=42)


df_augsburg = pd.read_csv('data_with_empty_latest_augsburg.csv')
df_augsburg = df_augsburg.reindex(columns=df.columns, fill_value=0)
X = df_augsburg.loc[:, df_augsburg.columns != 'y']
Y = df_augsburg["y"]

#X_test = X
#y_test = Y

####### LinearRegression #######
#reg = LinearRegression().fit(X_train, y_train)
#print("LINEARE REGRESSION")
#print(reg.score(X_test, y_test))
#print(reg.coef_)

####### LogisticRegression #######
#clf = LogisticRegression(random_state=0, class_weight="balanced").fit(X_train, y_train)
#print("LOGISITC REGRESSION")
#print(clf.score(X_test, y_test))
#print(clf.coef_)

#y_pred_clf = clf.predict(X_test)

#cm_clf = confusion_matrix(y_test, y_pred_clf)

#cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = [0, 1])
#cm_display.plot()
#plt.show()

####### HistGradientBoosting Regressor #######

est = HistGradientBoostingRegressor(random_state=0, verbose=1).fit(X_train, y_train)
print("HistGradientBoosting REGRESSION")
print(est.score(X_test, y_test))
print("Augsburg")
print(est.score(X, Y))

y_pred_est = est.predict(X_test)


####### RandomForestClassifier #######
rfc = RandomForestClassifier(class_weight='balanced').fit(X_train, y_train)
y_pred_rfc = rfc.predict(X_test)

print("RANDOM FORREST")
print(rfc.score(X_test, y_test))
print("F1 Score")
print(f1_score(y_test, y_pred_rfc, average='weighted'))
print("Augsburg")
print(rfc.score(X, Y))
print("F1 Score")
print(f1_score(Y, rfc.predict(X), average='weighted'))

all_leipzig_pred_rfc = rfc.predict(all_leipzig_x)
all_leipzig_rfc = df = pd.DataFrame(columns = ['accident', 'id'])
all_leipzig_rfc["accident"] = all_leipzig_pred_rfc
all_leipzig_rfc["id"] = id_col
all_leipzig_rfc.to_csv('data_all_rfc.csv', index=False)

print(classification_report(y_pred_rfc, y_test))
cm_rfc = confusion_matrix(y_test, y_pred_rfc)


#for feature, importance in zip(X_test.columns, importances_rfc):
#    print(f"{feature}: {importance:.4f}")

importances_rfc = rfc.feature_importances_
indices_rfc = np.argsort(importances_rfc)
           
plt.figure(figsize=(20, 15))
plt.barh(range(20), importances_rfc[indices_rfc[-20:]], color='b', align='center')
plt.yticks(range(20), [X_train.columns[i] for i in indices_rfc[-20:]])

plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Feature Importance im Random Forest")
plt.show()


cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm_rfc, display_labels = [0, 1])
cm_display.plot()
plt.title("Confusion Matrix for Random Forest")
plt.show()

'''explainer = shap.TreeExplainer(rfc)
shap_values = np.array(explainer.shap_values(X_train))
shap_values_ = shap_values.transpose((1,0,2))
print(shap_values.shape)

np.allclose(
    rfc.predict_proba(X_train),
    shap_values_.sum(2) + explainer.expected_value
)

shap.summary_plot(shap_values[3],X_train)'''


####### XGBoost #######
xgb = xgboost.XGBClassifier().fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)

print("XGBOOST")
print(xgb.score(X_test, y_test))
print("F1 Score")
print(f1_score(y_test, y_pred_xgb, average='weighted'))
print("Augsburg")
print(xgb.score(X, Y))
print("F1 Score")
print(f1_score(Y, xgb.predict(X), average='weighted'))

all_leipzig_pred_xgb = xgb.predict(all_leipzig_x)
all_leipzig_xgb = df = pd.DataFrame(columns = ['accident', 'id'])
all_leipzig_xgb["accident"] = all_leipzig_pred_xgb
all_leipzig_xgb["id"] = id_col
all_leipzig_xgb.to_csv('data_all_xgb.csv', index=False)

print(classification_report(y_pred_xgb, y_test))
cm_xgb = confusion_matrix(y_test, y_pred_xgb)

importances_xgb = xgb.feature_importances_
indices_xgb = np.argsort(importances_xgb)
plt.figure(figsize=(20, 15))
plt.barh(range(20), importances_xgb[indices_xgb[-20:]], color='b', align='center')
plt.yticks(range(20), [X_train.columns[i] for i in indices_xgb[-20:]])
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Feature Importance im XGBoost")
plt.show()

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm_xgb, display_labels = [0, 1])
cm_display.plot()
plt.title("Confusion Matrix for XGBoost")
plt.show()

X_samples = shap.utils.sample(X_test, 20)
explainer = shap.TreeExplainer(xgb)
expected_value = explainer.expected_value
shap_values = explainer.shap_values(X_samples)


#shap.decision_plot(expected_value, shap_values, features_display)
shap.decision_plot(expected_value, shap_values, X_samples.columns)

explainer = shap.Explainer(xgb, np.array(X_test,dtype='float64'))
shap_values = explainer(X_test)
shap.plots.beeswarm(shap_values, max_display=20)

####### SupportVectorMachine #######
#print("SVM")
#svm = SVC(class_weight='balanced').fit(X_train, y_train)
#print(svm.score(X_test, y_test))

#y_pred_svm = svm.predict(X_test)

#cm_svm = confusion_matrix(y_test, y_pred_svm)

#cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm_svm, display_labels = [0, 1])
#cm_display.plot()
#plt.show()

####### CatBoost #######
print("CatBoost")
catb = CatBoostClassifier(iterations=500,
                          early_stopping_rounds=50,
                           depth=6,
                           learning_rate=0.02,
                           l2_leaf_reg=6,
                           loss_function='Logloss',
                           verbose=False)
# train the model
catb.fit(X_train, y_train)
y_pred_catb = catb.predict(X_test)

print(catb.score(X_test, y_test))
print("F1 Score")
print(f1_score(y_test, y_pred_catb, average='weighted'))
print("Augsburg")
print(catb.score(X, Y))
print("F1 Score")
print(f1_score(Y, catb.predict(X), average='weighted'))

all_leipzig_pred_catb = catb.predict(all_leipzig_x)
all_leipzig_catb = df = pd.DataFrame(columns = ['accident', 'id'])
all_leipzig_catb["accident"] = all_leipzig_pred_catb
all_leipzig_catb["id"] = id_col
all_leipzig_catb.to_csv('data_all_catb.csv', index=False)

print(classification_report(y_pred_catb, y_test))
cm_catb = confusion_matrix(y_test, y_pred_catb)

importances_catb = catb.feature_importances_
indices_catb = np.argsort(importances_catb)
plt.figure(figsize=(20, 15))
plt.barh(range(20), importances_catb[indices_catb[-20:]], color='b', align='center')
plt.yticks(range(20), [X_train.columns[i] for i in indices_catb[-20:]])
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Feature Importance for CatBoost")
plt.show()

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm_catb, display_labels = [0, 1])
cm_display.plot()
plt.title("Confusion Matrix for CatBoost")
plt.show()



X_samples = shap.utils.sample(X_test, 20)
explainer = shap.TreeExplainer(catb)
expected_value = explainer.expected_value
shap_values = explainer.shap_values(X_samples)


#shap.decision_plot(expected_value, shap_values, features_display)
shap.decision_plot(expected_value, shap_values, X_samples.columns)

explainer = shap.Explainer(catb, np.array(X_test,dtype='float64'))
shap_values = explainer(X_test)
shap.plots.beeswarm(shap_values, max_display=20)


####### EBM #######
print("EBM")
ebm = ExplainableBoostingClassifier()
ebm.fit(X_train, y_train)
y_pred_ebm = ebm.predict(X_test)

print(roc_auc_score(y_test, ebm.predict_proba(X_test)[:, 1]))
print("F1 Score")
print(f1_score(y_test, y_pred_ebm, average='weighted'))
print("Augsburg")
print(roc_auc_score(Y, ebm.predict_proba(X)[:, 1]))
print("F1 Score")
print(f1_score(Y, ebm.predict(X), average='weighted'))

all_leipzig_pred_ebm = rfc.predict(all_leipzig_x)
all_leipzig_ebm = df = pd.DataFrame(columns = ['accident', 'id'])
all_leipzig_ebm["accident"] = all_leipzig_pred_ebm
all_leipzig_ebm["id"] = id_col
all_leipzig_ebm.to_csv('data_all_ebm.csv', index=False)

print(classification_report(y_pred_ebm, y_test))
cm_ebm = confusion_matrix(y_test, y_pred_ebm)

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = cm_ebm, display_labels = [0, 1])
cm_display.plot()
plt.title("Confusion Matrix for EBM")
plt.show()


import webbrowser
dashboard_url = show_link(ebm.explain_global())
webbrowser.open(dashboard_url)