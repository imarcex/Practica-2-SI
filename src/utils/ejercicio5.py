import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,accuracy_score
from sklearn.impute import SimpleImputer
from matplotlib import pyplot as plt
from utils.internal_interfaces import connector
'''
datos = pd.read_json('data/users_data_online_clasificado.json')
usuarios_dict = {nombre: {
    "telefono": detalles["telefono"],
    "provincia": detalles["provincia"],
    "permisos": detalles["permisos"],
    "total_emails": detalles["emails"]["total"],
    "total_phishing": detalles["emails"]["phishing"],
    "total_cliclados": detalles["emails"]["cliclados"],
    "critico": detalles["critico"]
} for usuario in datos["usuarios"] for nombre, detalles in usuario.items()}
df = pd.DataFrame.from_dict(usuarios_dict, orient='index')
'''
df = pd.read_sql_query("SELECT total, phishing, cliclados, esCritico FROM emails INNER JOIN usuarios ON emails.usuario = usuarios.username", connector)

def linearRegression():
    LR = LinearRegression()

    X_df = df[["total", "phishing"]]
    X_df["ratio"] = df["cliclados"] / df["phishing"]
    imputer = SimpleImputer(strategy="mean")
    X_df["ratio"] = imputer.fit_transform(X_df["ratio"].values.reshape(-1, 1))
    X = np.array(X_df["ratio"]).reshape(-1, 1)
    y = df["esCritico"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    # Entrenamiento de modelo
    LR.fit(X_train, y_train)

    # Estadisticas de la predicción
    #critical_y_pred = LR.predict(X_test)
    #print(f"Mean squared error: {mean_squared_error(y_test, critical_y_pred)}")
    #plt.scatter(X_test, y_test, color="black")
    #plt.plot(X_test, critical_y_pred, color="blue", linewidth=3)
    #plt.xticks(())
    #plt.yticks(())
    #plt.show()
    return LR



def decisionTree():

    X = np.array(df[["total","phishing", "cliclados"]])
    y = np.array(df["esCritico"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    DT = tree.DecisionTreeClassifier()
    DT.fit(X_train, y_train)

    predY = DT.predict(X_test)
    accuracy = accuracy_score(y_test, predY)
    print("Decision Tree Results")
    print(f"Mean squared error: {mean_squared_error(y_test, predY)}")
    print("Accuracy: ", accuracy)
    return DT



def randomForest():

    X = np.array(df[["total","phishing", "cliclados"]])
    y = np.array(df["esCritico"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    RF = RandomForestRegressor(n_estimators=100)
    RF.fit(X_train, y_train)

    predY = RF.predict(X_test).round()
    accuracy = accuracy_score(y_test, predY)
    print("Random Forest Regressor Results")
    print(f"Mean squared error: {mean_squared_error(y_test, predY)}")
    print("Accuracy", accuracy)

    return RF

