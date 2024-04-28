from pydataset import data
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt


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
print(df.head())
LR = LinearRegression()

X = df["total_phishing"].values.reshape(-1, 1)
y = df["total_cliclados"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
LR.fit(X_train, y_train)
critical_y_pred = LR.predict(X_test)
print(f"Mean squared error: {mean_squared_error(y_test, critical_y_pred)}")
plt.scatter(X_test, y_test, color="black")
plt.plot(X_test, critical_y_pred, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()

