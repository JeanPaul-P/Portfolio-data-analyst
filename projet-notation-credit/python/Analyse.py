#%% 
#Synchronisation du fichier .ipnyb avec le fichier .py
# ---
# jupyter:
#   jupytext:
#     formats: py:percent,ipynb
# ---

#%%
#Importation des bibliothèques
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
  #CHARGEMENT DES DONNEES
# %%
#Chemin relatif 
data_path = os.path.join("data", "CorporateCreditRating.xlsx")
#Chargement des datas
df = pd.read_excel(data_path)

#Afficher les 1ères lignes
print(df.head())

#Vérifier la structure des données
print(df.info())

#%%
#Chemin relatif 
sector_path = os.path.join("data", "Sector_Table.xlsx")
#Chargement de la table détail des secteurs 
df_Sector = pd.read_excel(sector_path)

#Afficher les 1ères lignes
print(df_Sector.head())

#Vérifier la structure des données
print(df_Sector.info())


#%%
#PREPARATION DES DONNEES
#%%
#Valeurs manquantes et doublons
    #valeurs manquantes
print(df_Sector.isnull().sum())
    #doublons
doublons = df_Sector.duplicated().sum()
print("Nombre de doublons:", doublons)

#%%
#Ajout de la table détail des secteurs à df
df = pd.merge(df, df_Sector, on="SIC Code", how="left")

df.head()
#%%
#Valeurs manquantes
print(df.isnull().sum())
#%%
#Suppression des lignes où SubSector est vide
df = df.dropna(subset=["SubSector"])
print(df.isnull().sum())

#%%
#doublons
doublons = df.duplicated().sum()
print("Nombre de doublons:", doublons)

#%% 
#Renommage de "Binary Rating" = Investment Grade 
df.rename(columns={'Binary Rating': 'Investment Grade'}, inplace=True)

df.columns
#%%
#Filtre des données sur l'agence de notation "S&P"
df = df[df["Rating Agency"] == "Standard & Poor's Ratings Services"]

#Nombre de lignes après filtrage
print(f"Nombre de lignes après filtrage sur S&P : {df.shape[0]}")

#%%
#Type de données 
print(df.dtypes)

#%%
#Liste des secteurs uniques
df["Sector"].unique()

#%%
#Renommer les secteurs
sector_names = {
    "BusEq": "Business Equipment",
    "Chems": "Chemicals",
    "Durbl": "Durables",
    "Enrgy": "Energy",
    "Hlth": "Health",
    "Manuf": "Manufacturing",
    "Money": "Money",
    "NoDur": "Non-Durables",
    "Other": "Other",
    "Shops": "Shops",
    "Telcm": "Telecommunications",
    "Utils": "Utilities"}

df["Sector"] = df["Sector"].replace(sector_names)

#Vérification des changements
df["Sector"].unique()

#%%
#ANALYSE EXPLORATOIRE DES DONNEES
# %%
#Affichage de la répartition des notations de crédit
df["Rating"].value_counts().plot(kind="bar", figsize=(8, 4))
    #Ajouter des titres et labels
plt.title("Répartition des notations de crédit")
plt.xlabel("Notation")
plt.ylabel("Nombre d'entreprises")
    #Afficher le graphique
plt.show()

#Distribution des notations de crédit
df["Rating"].hist(figsize=(12, 8), bins=30)

plt.title("Distribution des notations de crédit")
plt.xlabel("Notation")
plt.ylabel("Nombre d'entreprises")
plt.show()

#%%
#Analyse des ratios financiers 
#%%
#Sélection des ratios 
ratios = ["Current Ratio", "Debt/Equity Ratio", "ROE - Return On Equity", "Net Profit Margin"]

#histogrammes
plt.figure(figsize=(10, 8))
for i, ratio in enumerate(ratios, 1):
    plt.subplot(2, 2, i)
    sns.histplot(df[ratio], bins=30, kde=True)
    plt.title(f"Distribution de {ratio}")
    plt.xlabel(ratio)
    plt.ylabel("Fréquence")
plt.tight_layout()
plt.show()

#Statistique descriptive
df[ratios].describe()

#%%
#Analyse écart interquartile
total_rows = df.shape[0]  

for i, ratio in enumerate(ratios, 1):
    Q1 = df[ratio].quantile(0.25) #1er quartile
    Q3 = df[ratio].quantile(0.75) #2ème quartile
    IQR = Q3 - Q1

    #Filtrage des valeurs aberrantes
    val_aberrantes = df[(df[ratio] < (Q1 - 1.5 * IQR)) | (df[ratio] > (Q3 + 1.5 * IQR))]
    
    print(f"Ratio : {ratio}")
    print(f" - Valeurs aberrantes : {val_aberrantes.shape[0]}")
    print(f" - Pourcentage du total : {round((val_aberrantes.shape[0]/total_rows)*100, 2)} %\n")

# %%
#Dispersion avec boxplot
plt.figure(figsize=(8, 6))
    #Afficher plusieurs graphs (subplot)
plt.subplot(4, 1, 1)
plt.boxplot(df["Current Ratio"], vert=False)
plt.title("Boxplot du Current Ratio")
plt.subplot(4, 1, 2)
plt.boxplot(df["Debt/Equity Ratio"], vert=False)
plt.title("Boxplot du Debt/Equity Ratio")
plt.subplot(4, 1, 3)
plt.boxplot(df["ROE - Return On Equity"], vert=False)
plt.title("Boxplot du ROE")
plt.subplot(4, 1, 4)
plt.boxplot(df["Net Profit Margin"], vert=False)
plt.title("Boxplot du NPM")
plt.figtext(0.5, -0.1, 
            "Les points hors des moustaches du boxplot correspondent aux valeurs extrêmes détectées par la méthode IQR. \n"
            "Cette méthode permet d'identifier les potentielles valeurs aberrantes", 
            wrap=True, horizontalalignment="center", fontsize=10)
plt.tight_layout() 


# %%
#Etude des relations entre variables (corrélations, tendances).
#Convertir la notation de crédit en score numérique 
rating_mapping = {"AAA": 23, "AA+": 22, "AA": 21, "AA-": 20,
                  "A+": 19, "A": 18, "A-": 17,
                  "BBB+": 16, "BBB": 15, "BBB-": 14,
                  "BB+": 13, "BB": 12, "BB-": 11,
                  "B+": 10, "B": 9, "B-": 8,
                  "CCC+": 7, "CCC": 6, "CCC-": 5,
                  "CC+": 4, "CC": 3,
                  "C": 2, "D": 1}
#Associe la notation au nouveau score numérique 
df["Rating_Score"] = df["Rating"].map(rating_mapping)

#%%
#Analyse avec la matrice de corrélation
list_corr = ["Rating_Score", "Current Ratio", "Debt/Equity Ratio", "Long-term Debt / Capital", 
          "ROE - Return On Equity", "Net Profit Margin", "EBITDA Margin", "ROI - Return On Investment", 
          "Return On Tangible Equity", "ROA - Return On Assets", "EBIT Margin", "Gross Margin",
          "Asset Turnover", "Operating Cash Flow Per Share", "Free Cash Flow Per Share",
          "Pre-Tax Profit Margin", "Operating Margin"]

df[list_corr].corr()

#Visualisation de la matrice de corrélation
plt.figure(figsize=(12, 8))
sns.heatmap(df[list_corr].corr(),
            annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Matrice de corrélation des ratios financiers et de la notation de crédit")
plt.figtext(0.5, -0.1,
            "La matrice de corrélation montre les relations entre les ratios financiers et la notation de crédit. \n"
            "Les valeurs proches de 1 ou -1 indiquent une forte corrélation, tandis que les valeurs proches de 0 indiquent une faible corrélation.", 
            wrap=True, horizontalalignment="center", fontsize=10)
plt.tight_layout()
plt.show()


#%%
#Visualisation
#%%
#Ratio de liquidité
#Nuage de point  avec une courbe de tendance
plt.figure(figsize=(10, 6))
sns.regplot(x=df["Current Ratio"], y=df["Rating_Score"], 
            scatter_kws={'alpha': 0.5}, line_kws={"color": "red"})

plt.title("Relation entre le Current Ratio et la Notation de Crédit")
plt.xlabel("Current Ratio")
plt.ylabel("Notation de Crédit (Score numérique)")
plt.grid(True)
plt.figtext(0.5, -0.1, 
            "Pour l'axe de la Notation de crédit : \n"
            "Plus le score est élevé, "
            "plus la notation est mauvaise (ex: AAA=1, CCC=18 ou plus) \n", 
            wrap=True, horizontalalignment="center", fontsize=10)

plt.show()


#%%
#Nombre d'entreprises par Rating_Score 
rating_counts = df["Rating_Score"].value_counts()

#Rating_count pour associer le nombre d'entreprise à la note de Rating score
df["Rating_Count"] = df["Rating_Score"].map(rating_counts)

#Définir la taille des points en fonction du nombre d’entreprises ayant la même note
#Racine carrée (sqrt) pour atténuer l'effet de la distribution hétérogène de Rating_score 
point_sizes = np.sqrt(df["Rating_Count"]) * 20  

#Nuage de point 
plt.figure(figsize=(10, 6))
plt.scatter(x=df["Current Ratio"], y=df["Rating_Score"], 
            s=point_sizes, c=df["Rating_Score"], alpha=0.7, cmap="coolwarm")

plt.title("Relation entre Current Ratio et la Notation de Crédit")
plt.xlabel("Current Ratio")
plt.ylabel("Notation de Crédit (Score numérique)")
plt.colorbar(label="Score de Notation (Format numérique)")
plt.grid(True)
plt.figtext(0.5, -0.05, 
            "Pour l'axe de la Notation de crédit : \n"
            "Plus le score est élevé, "
            "plus la notation est mauvaise (ex: AAA=1, CCC=18 ou plus) \n"
            "Plus une notation est fréquente, plus le point sera grand.", 
            wrap=True, horizontalalignment="center", fontsize=10)

plt.show()

#%%
#Ratio d'endettement 
#Debt/Equity Ratio
plt.figure(figsize=(10, 6))
sns.regplot(x=df["Debt/Equity Ratio"], y=df["Rating_Score"], 
            scatter_kws={'alpha': 0.5}, line_kws={"color": "red"})

plt.title("Relation entre Debt/Equity Ratio et la Notation de Crédit")
plt.xlabel("Debt/Equity Ratio")
plt.ylabel("Notation de Crédit (Score numérique)")
plt.grid(True)
plt.figtext(0.5, -0.1, 
            "Pour l'axe de la Notation de crédit : \n"
            "Plus le score est élevé, "
            "plus la notation est mauvaise (ex: AAA=1, CCC=18 ou plus) \n", 
            wrap=True, horizontalalignment="center", fontsize=10)

plt.show()

#Long-term Debt / Capital
plt.figure(figsize=(10, 6))
plt.scatter(x=df["Long-term Debt / Capital"], y=df["Rating_Score"], 
            s=point_sizes, c=df["Rating_Score"], alpha=0.7, cmap="coolwarm")

plt.title("Relation entre Long-term Debt / Capital et la Notation de Crédit")
plt.xlabel("Long-term Debt / Capital")
plt.ylabel("Notation de Crédit (Score numérique)")
plt.colorbar(label="Score de Notation (Format numérique)")
plt.grid(True)
plt.figtext(0.5, -0.05, 
            "Pour l'axe de la Notation de crédit : \n"
            "Plus le score est élevé, "
            "plus la notation est mauvaise (ex: AAA=1, CCC=18 ou plus) \n"
            "Plus une notation est fréquente, plus le point sera grand.", 
            wrap=True, horizontalalignment="center", fontsize=10)
plt.show()
#%%
#Ratio de rentabilité 
#Net Profit Margin
plt.figure(figsize=(10, 6))
sns.regplot(x=df["Net Profit Margin"], y=df["Rating_Score"], 
            scatter_kws={'alpha': 0.5}, line_kws={"color": "red"})

plt.title("Relation entre Net Profit Margin et la Notation de Crédit")
plt.xlabel("Net Profit Margin")
plt.ylabel("Notation de Crédit (Score numérique)")
plt.grid(True)
plt.figtext(0.5, -0.1, 
            "Pour l'axe de la Notation de crédit : \n"
            "Plus le score est élevé, "
            "plus la notation est mauvaise (ex: AAA=1, CCC=18 ou plus) \n", 
            wrap=True, horizontalalignment="center", fontsize=10)

plt.show()

#ROE - Return On Equity
plt.figure(figsize=(10, 6))
plt.scatter(x=df["ROE - Return On Equity"], y=df["Rating_Score"], 
            s=point_sizes, c=df["Rating_Score"], alpha=0.7, cmap="coolwarm")

plt.title("Relation entre ROE - Return On Equity et la Notation de Crédit")
plt.xlabel("ROE - Return On Equity")
plt.ylabel("Notation de Crédit (Score numérique)")
plt.colorbar(label="Score de Notation (Format numérique)")
plt.grid(True)
plt.figtext(0.5, -0.05, 
            "Pour l'axe de la Notation de crédit : \n"
            "Plus le score est élevé, "
            "plus la notation est mauvaise (ex: AAA=1, CCC=18 ou plus) \n"
            "Plus une notation est fréquente, plus le point sera grand.", 
            wrap=True, horizontalalignment="center", fontsize=10)

plt.show()

#%%
#Analyse sectorielle
#%%
#Regroupement rating par secteur
sector_rating = df.groupby(['Sector', 'Rating']).size().unstack().fillna(0)

#Visualisation
sector_rating.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title("Répartition des notations de crédit par secteur")
plt.ylabel("Nombre d'entreprises")
plt.xlabel("Secteur")
plt.legend(title='Notation')
plt.tight_layout()
plt.figtext(0.5, -0.05, 
            "Les secteurs sont regroupés par notation de crédit.",
            wrap=True, horizontalalignment="center", fontsize=10)
plt.show()

#%%
#Répartition des entreprise IG par secteur
sector_IG = df.groupby(['Sector', 'Investment Grade']).size().unstack().fillna(0)

#Visualisation
sector_IG.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title("Répartition des Investment Grade par secteur")
plt.ylabel("Nombre d'entreprises")
plt.xlabel("Secteur")
plt.legend(title='IG')
plt.tight_layout()
plt.figtext(0.5, -0.05, 
            "Les secteurs sont regroupés par Investment Grade. \n"
            "1 : Investment Grade et 0 : Non Investment Grade",
            wrap=True, horizontalalignment="center", fontsize=10)
plt.show()

#%%
#Analyse de la tendance globale et par secteur du Rating score
#Tendance globale
trend = df.groupby(df["Rating Date"].dt.to_period("Y"))["Rating_Score"].mean()

#Tendance par secteur
sector_trends = df.groupby([df["Rating Date"].dt.to_period("Y"), "Sector"])["Rating_Score"].mean().unstack()

#Visualisation
sector_trends.plot(figsize=(12, 8))
trend.plot(kind="line", figsize=(12, 8), marker="o",color="black", linewidth=3, label="Tendance globale")
plt.xlabel("Année")
plt.ylabel("Score moyen de notation")
plt.title("Tendances des scores de notation par secteur et tendance globale")
plt.legend(title="Légende", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.show()

#%%
#Matrice de corrélation par secteur
#Liste des secteurs uniques
sectors = df["Sector"].dropna().unique()
print(sectors)
#Calcul des corrélations par secteur
for sector in sectors:
    print(f"Corrélations pour le secteur : {sector}")
    sector_data = df[df["Sector"] == sector]
    correlation_matrix = sector_data[ratios].corr()
    print(correlation_matrix)
    print("\n")

#%%
#Nuage de points pour visualiser les relations entre les ratios financiers et la notation de crédit
#Visualiser les relations par secteur
for sector in sectors:
    print(f"Visualisation pour le secteur : {sector}")
    sector_data = df[df["Sector"] == sector]
    
    #Exemple : Relation entre Current Ratio et Rating_Score
    plt.figure(figsize=(10, 6))
    sns.regplot(x=sector_data["Current Ratio"], y=sector_data["Rating_Score"], 
                scatter_kws={'alpha': 0.5}, line_kws={"color": "red"})
    plt.title(f"Relation entre Current Ratio et Notation de Crédit ({sector})")
    plt.xlabel("Current Ratio")
    plt.ylabel("Notation de Crédit (Score numérique)")
    plt.grid(True)
    plt.show()

#%%
#Moyenne des ratios financiers par secteur
sector_ratios = df.groupby('Sector')[["Current Ratio", "Debt/Equity Ratio", "Net Profit Margin", 
        "ROE - Return On Equity"]].mean().sort_values(by='Current Ratio', ascending=True)

# Visualisation avec heatmap
sns.heatmap(sector_ratios, annot=True, cmap='coolwarm')
plt.title("Moyennes des ratios financiers par secteur :")
plt.show()

#%%
#Etude des outliers par secteur
outlier_summary = []

for sector in sectors:
    sector_data = df[df["Sector"] == sector]
    
    for ratio in ["Current Ratio", "Debt/Equity Ratio", "Net Profit Margin", "ROE - Return On Equity"]:
        Q1 = sector_data[ratio].quantile(0.25)
        Q3 = sector_data[ratio].quantile(0.75)
        IQR = Q3 - Q1
        outliers = sector_data[(sector_data[ratio] < (Q1 - 1.5 * IQR)) | 
                               (sector_data[ratio] > (Q3 + 1.5 * IQR))]
        count_outliers = outliers.shape[0]
        pourcentage = round((count_outliers / sector_data.shape[0]) * 100, 2)

        outlier_summary.append({
            "Sector": sector,
            "Ratio": ratio,
            "Nombre d'outliers": count_outliers,
            "% d'outliers": pourcentage})

#Tableau
outlier_df = pd.DataFrame(outlier_summary)
outlier_df

#%%
#Médiane des ratios financiers par secteur
sector_ratios_median = df.groupby('Sector')[["Current Ratio", "Debt/Equity Ratio", "Net Profit Margin", 
        "ROE - Return On Equity"]].median().sort_values(by='Current Ratio', ascending=True)

# Visualisation avec heatmap
sns.heatmap(sector_ratios_median, annot=True, cmap='coolwarm')
plt.title("Médianes des ratios financiers par secteur :")
plt.show()

#%% Distribution du ROE par secteur avec histogrammes
sectors = df["Sector"].unique()  
#Liste des secteurs uniques
plt.figure(figsize=(15, 12))

# Création d'un histogramme pour chaque secteur
for i, sector in enumerate(sectors, 1):
    plt.subplot((len(sectors) // 3) + 1, 3, i)  # Organisation en sous-graphiques
    sector_data = df[df["Sector"] == sector]  # Filtrer les données par secteur
    plt.hist(sector_data["ROE - Return On Equity"], bins=20, alpha=0.7, color="blue", edgecolor="black")
    plt.title(f"ROE - {sector}")
    plt.xlabel("ROE - Return On Equity")
    plt.ylabel("Fréquence")

plt.tight_layout()
plt.show()

#%%
#Winsorisation des ratios financiers pour réduire l'impact des valeurs extrêmes
#Importation de la fonction de winsorisation
from scipy.stats.mstats import winsorize

#Copie de df pour la winsorisation
df_winsorized = df.copy()

#Liste des ratios financiers à winsoriser
ratios = ["Current Ratio", "Debt/Equity Ratio", "Net Profit Margin", "ROE - Return On Equity"]

#Moyennes par secteur avant winsorisation
sector_means_before = df.groupby("Sector")[ratios].mean()

#Winsorisation (on limite les valeurs extrêmes aux 5ème et 95ème percentiles)
for ratio in ratios:
    lower = 0.05 
    upper = 0.05  
    df_winsorized[ratio] = winsorize(df[ratio], limits=(lower, upper))

#Moyennes par secteur après winsorisation
sector_means_after = df_winsorized.groupby("Sector")[ratios].mean()

#Visualisation des moyennes avant winsorisation
sns.heatmap(sector_means_before, annot=True, cmap="coolwarm")
plt.title("Moyennes des ratios financiers par secteur (Avant Winsorisation)")
plt.show()

#Visualisation des moyennes après winsorisation
sns.heatmap(sector_means_after, annot=True, cmap="coolwarm")
plt.title("Moyennes des ratios financiers par secteur (Après Winsorisation)")
plt.show()

#%%
#SCORE RISQUE 
#%%
#Création du score risque entreprise
#Calcul de la corrélation entre les ratios et la notation
correlations = df[["Rating_Score", "Current Ratio", "Debt/Equity Ratio", 
                   "Net Profit Margin", "ROE - Return On Equity"]].corr()

#Corrélations avec Rating_score 
correlation_rating = correlations["Rating_Score"].drop("Rating_Score")
print(correlation_rating)

#%%
#Poids du ratio sur le rating en valeur absolue pour éviter les effets de signe
weights = correlation_rating.abs() / correlation_rating.abs().sum()

print("Poids des ratios basés sur leur corrélation avec la notation :")
print(weights)

#%%
#Calcul du score de risque pondéré
df["Risk_Score"] = (
    df["Current Ratio"] * weights["Current Ratio"] +
    df["Debt/Equity Ratio"] * weights["Debt/Equity Ratio"] +
    df["Net Profit Margin"] * weights["Net Profit Margin"] +
    df["ROE - Return On Equity"] * weights["ROE - Return On Equity"]
)

print(df[["Corporation", "Risk_Score"]].head())

#%%
df["Risk_Score"].describe()

#%%
#Distribution des scores de risque 
plt.figure(figsize=(10, 6))
sns.histplot(df["Risk_Score"], bins=30, kde=True, color="blue")
plt.title("Distribution des scores de risque")
plt.xlabel("Score de risque")
plt.ylabel("Fréquence")
plt.grid(True)
plt.show()

#%%
#Classification du Risk_Score
q1 = df["Risk_Score"].quantile(0.25)
q3 = df["Risk_Score"].quantile(0.75)

def classify_risk(score):
    if score <= q1:
        return "Low"
    elif score <= q3:
        return "Moderate"
    else:
        return "High"

df["Risk_Category"] = df["Risk_Score"].apply(classify_risk)

print(df[["Corporation", "Risk_Score", "Risk_Category"]].head())

#%%
#Création du score risque secteur (Normalisé)
#%%
#Importation du Min-Max Scaler pour la normalisation
from sklearn.preprocessing import MinMaxScaler

#Création du scaler
scaler = MinMaxScaler()

#%%
#Calcul des médianes des ratios par secteur
sector_medians = df.groupby("Sector")[ratios].median()

print(sector_medians)

#Normalisation des médianes sectorielles
sector_medians_normalized = sector_medians.copy()
sector_medians_normalized[ratios] = scaler.fit_transform(sector_medians[ratios])

print(sector_medians_normalized)

#%%
#Création des colonnes médiane des ratios 
for ratio in ratios:
    df[f"{ratio}_Sector_Median"] = df["Sector"].map(sector_medians[ratio])

#Vérification des nouvelles colonnes
df[["Corporation", "Sector", "Current Ratio_Sector_Median", 
    "Debt/Equity Ratio_Sector_Median","Net Profit Margin_Sector_Median",
    "ROE - Return On Equity_Sector_Median"]].head(20)

#%%
#Calcul de la notation moyenne (médiane) par secteur
sector_medians_normalized["Rating_Score"] = df.groupby("Sector")["Rating_Score"].median()

print(sector_medians_normalized)

#%%
#Corrélations entre les ratios et la notation moyenne
sector_correlations = sector_medians_normalized.corr()["Rating_Score"].drop("Rating_Score")

print(sector_correlations)

# %%
#Poids du ratio sur le rating en valeur absolue
sector_weights = sector_correlations.abs() / sector_correlations.abs().sum()

print("Poids des ratios basés sur leur corrélation avec la notation :")
print(sector_weights)

#%%
#Calcul score de risque pour les secteurs
sector_medians_normalized["Sector_Risk_Score"] = (
    sector_medians_normalized["Current Ratio"] * sector_weights["Current Ratio"] +
    sector_medians_normalized["Debt/Equity Ratio"] * sector_weights["Debt/Equity Ratio"] +
    sector_medians_normalized["Net Profit Margin"] * sector_weights["Net Profit Margin"] +
    sector_medians_normalized["ROE - Return On Equity"] * sector_weights["ROE - Return On Equity"]
).round(3)

print(sector_medians_normalized[["Sector_Risk_Score"]])

# %%
# Visualisation des scores sectoriels
plt.figure(figsize=(12, 6))
sector_medians_normalized["Sector_Risk_Score"].sort_values().plot(kind="bar", color="skyblue")
plt.title("Scores de risque par secteur (basés sur les médianes normalisées)")
plt.xlabel("Secteur")
plt.ylabel("Score de risque")
plt.grid(True)
plt.show()

#%%
#Normalisation des ratios financiers des entreprises
df_normalized = df.copy()
df_normalized[ratios] = scaler.fit_transform(df[ratios])

#Calcul du score de risque pour les entreprises (normalisé)
df_normalized["Risk_Score"] = (
    df_normalized["Current Ratio"] * sector_weights["Current Ratio"] +
    df_normalized["Debt/Equity Ratio"] * sector_weights["Debt/Equity Ratio"] +
    df_normalized["Net Profit Margin"] * sector_weights["Net Profit Margin"] +
    df_normalized["ROE - Return On Equity"] * sector_weights["ROE - Return On Equity"]
).round(3)

print(df_normalized[["Corporation", "Risk_Score"]].head())

#%%
#Classification du Risk_Score
q1 = df_normalized["Risk_Score"].quantile(0.25)
q3 = df_normalized["Risk_Score"].quantile(0.75)

def classify_risk(score):
    if score <= q1:
        return "Low"
    elif score <= q3:
        return "Moderate"
    else:
        return "High"

df_normalized["Risk_Category"] = df_normalized["Risk_Score"].apply(classify_risk)

print(df_normalized[["Corporation", "Risk_Score", "Risk_Category"]].head())

#%%
#Comparaison des scores de risque
#Ajout des scores de risque sectoriels à df_normalized
df_normalized = pd.merge(df_normalized, sector_medians_normalized[["Sector_Risk_Score"]], 
                         left_on="Sector", right_index=True)

df_normalized["Risk_Comparaison"] = df_normalized["Risk_Score"] - df_normalized["Sector_Risk_Score"]

#%%
# Indicateur de performance par rapport au secteur
df_normalized["Performance_vs_Sector"] = df_normalized["Risk_Comparaison"].apply(lambda x: "Au-dessus" if x > 0 else "En-dessous")

#%%
#Ratios financiers normalisés 
print("Ratios normalisés :")
print(df_normalized[ratios].head())

#%%
#Calcul de la corrélation entre les ratios normalisés et le Rating_Score
correlations_norm = df_normalized[["Rating_Score"] + ratios].corr()
#Corrélations avec Rating_Score
correlation_rating_norm = correlations_norm["Rating_Score"].drop("Rating_Score")
print("Corrélations avec Rating_Score :")
print(correlation_rating_norm)

#Calcul des poids des ratios (en valeur absolue pour éviter les effets de signe)
weights2 = correlation_rating_norm.abs() / correlation_rating_norm.abs().sum()
print("Poids des ratios basés sur leur corrélation avec la notation :")
print(weights2)

#%%
#Poids ajusté avec Investment Grade (0.3 fixé pour l'importance de l'Investment Grade)
investment_grade_weight = 0.3  
weights_adjusted = weights2 * (1 - investment_grade_weight)  

print("Poids ajustés des ratios :")
print(weights_adjusted)

#%%
#Calcul du score de risque ajusté
df_normalized["Risk_Score_Improved"] = (
    df_normalized["Current Ratio"] * weights_adjusted["Current Ratio"] +
    df_normalized["Debt/Equity Ratio"] * weights_adjusted["Debt/Equity Ratio"] +
    df_normalized["Net Profit Margin"] * weights_adjusted["Net Profit Margin"] +
    df_normalized["ROE - Return On Equity"] * weights_adjusted["ROE - Return On Equity"] +
    df_normalized["Investment Grade"] * investment_grade_weight)

print("Nouveau score de risque calculé :")
print(df_normalized[["Corporation", "Risk_Score_Improved"]].head())

#%%
#Statistiques descriptives
print(df_normalized["Risk_Score_Improved"].describe())

#%%
#Calcul du score de risque pour les entreprises (normalisé)
df_normalized["Risk_Score"] = (
    df_normalized["Current Ratio"] * weights2["Current Ratio"] +
    df_normalized["Debt/Equity Ratio"] * weights2["Debt/Equity Ratio"] +
    df_normalized["Net Profit Margin"] * weights2["Net Profit Margin"] +
    df_normalized["ROE - Return On Equity"] * weights2["ROE - Return On Equity"]
).round(3)
print(df_normalized[["Corporation", "Risk_Score"]].head())

#%%
#Comparaison des distributions des scores
plt.figure(figsize=(12, 6))
sns.histplot(df_normalized["Risk_Score"], bins=30, kde=True, color="blue", label="Ancien Risk Score", alpha=0.6)
sns.histplot(df_normalized["Risk_Score_Improved"], bins=30, kde=True, color="green", label="Nouveau Risk Score", alpha=0.6)
plt.title("Comparaison des distributions des scores de risque")
plt.xlabel("Score de risque")
plt.ylabel("Fréquence")
plt.legend()
plt.grid(True)
plt.show()

#%%
#Visualisation de la distribution des deux scores
plt.figure(figsize=(12, 6))
sns.histplot(df_normalized["Risk_Score_Improved"], bins=30, kde=True, color="green", label="Nouveau Risk Score", alpha=0.6)
plt.title("Comparaison des distributions des scores de risque")
plt.xlabel("Score de risque")
plt.ylabel("Fréquence")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
sns.histplot(df["Risk_Score"], bins=30, kde=True, color="blue", label="Ancien Risk Score", alpha=0.6)
plt.title("Comparaison des distributions des scores de risque")
plt.xlabel("Score de risque")
plt.ylabel("Fréquence")
plt.legend()
plt.grid(True)
plt.show()

#%%
#Corrélation entre les deux scores
correlation = df["Risk_Score"].corr(df_normalized["Risk_Score_Improved"])
print(f"Corrélation entre l'ancien et le nouveau score : {correlation:.2f}")

correlation

#Écart moyen entre les deux scores
mean_difference = (df_normalized["Risk_Score_Improved"] - df["Risk_Score"]).mean()
print(f"Écart moyen entre les deux scores : {mean_difference:.2f}")

#%%
#Répartition des scores par catégorie de risk
plt.figure(figsize=(10, 6))
sns.boxplot(x="Risk_Category", y="Risk_Score_Improved", data=df_normalized, palette="coolwarm")
plt.title("Répartition des scores de risque par catégorie")
plt.xlabel("Catégorie de risque")
plt.ylabel("Score de risque")
plt.grid(True)
plt.show()

#%%
#MACHINE LEARNING 
#%% 
#Validation croisée pour évaluer la robustesse des pondérations
#Importation des bibliothèque 
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt

#%%
#X: ratios normalisés Y: Notation format numérique
X = df_normalized[ratios]
y = df["Rating_Score"]

X.columns

#%%
#Initialiser le modèle KFold pour la validation croisée avec 5 plis
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_errors = []
rmse_errors = []
r2_scores = []

for train_index, test_index in kf.split(X):
    #Séparer les données en ensembles d'entraînement et de test
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    #Modèle de régression linéaire
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    #Prédictions sur l'ensemble de test
    y_pred = model.predict(X_test)
    
    #Calcul des métriques de performance 
    mse = mean_squared_error(y_test, y_pred)
    rmse = sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    #Résultats
    mse_errors.append(mse)
    rmse_errors.append(rmse)
    r2_scores.append(r2)

#Résultats de la validation croisée
print("\nValidation croisée (Régression linéaire) :")
print(f"Erreur quadratique moyenne (MSE) moyenne : {np.mean(mse_errors):.4f}")
print(f"Écart-type du MSE : {np.std(mse_errors):.4f}")
print(f"Erreur quadratique moyenne racine (RMSE) moyenne : {np.mean(rmse_errors):.4f}")
print(f"Écart-type du RMSE : {np.std(rmse_errors):.4f}")
print(f"R² moyen : {np.mean(r2_scores):.4f}")
print(f"Écart-type du R² : {np.std(r2_scores):.4f}")

#%% 
#Importation de l'arbre de décision
from sklearn.tree import DecisionTreeRegressor

#Initialiser la validation croisée avec 5 plis
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_errors_tree = []
rmse_errors_tree = []
r2_scores_tree = []

#Modèle d'arbre de décision
tree_model = DecisionTreeRegressor(random_state=42, max_depth=5)  # Vous pouvez ajuster max_depth pour éviter l'overfitting

for train_index, test_index in kf.split(X):
    #Diviser les données en ensembles d'entraînement et de test
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    #Entraîner le modèle d'arbre de décision
    tree_model.fit(X_train, y_train)
    
    #Prédictions sur l'ensemble de test
    y_pred_tree = tree_model.predict(X_test)
    
    #Calcul des métriques
    mse_tree = mean_squared_error(y_test, y_pred_tree)
    rmse_tree = sqrt(mse_tree)
    r2_tree = r2_score(y_test, y_pred_tree)
    
    #Résultats
    mse_errors_tree.append(mse_tree)
    rmse_errors_tree.append(rmse_tree)
    r2_scores_tree.append(r2_tree)

#Résultats de la validation croisée pour l'arbre de décision
print("\nValidation croisée (Arbre de décision) :")
print(f"Erreur quadratique moyenne (MSE) moyenne : {np.mean(mse_errors_tree):.4f}")
print(f"Écart-type du MSE : {np.std(mse_errors_tree):.4f}")
print(f"Erreur quadratique moyenne racine (RMSE) moyenne : {np.mean(rmse_errors_tree):.4f}")
print(f"Écart-type du RMSE : {np.std(rmse_errors_tree):.4f}")
print(f"R² moyen : {np.mean(r2_scores_tree):.4f}")
print(f"Écart-type du R² : {np.std(r2_scores_tree):.4f}")

#%%
#DécisionTree plus performant mais légèrement moins stable 

#%%
#Importance des variables
importances = tree_model.feature_importances_

#Création d'une série pandas pour l'affichage
feature_importance = pd.Series(importances, index=X.columns)

#Trier les variables par importance décroissante
feature_importance = feature_importance.sort_values(ascending=True)

#Affichage avec un graphique horizontal
plt.figure(figsize=(10, 6))
feature_importance.plot(kind='barh', color='steelblue')
plt.title("Importance des variables (Arbre de décision)")
plt.xlabel("Score d'importance")
plt.tight_layout()
plt.show()
#%%
df.columns 

#%%
#Ajout de ratios
ratios_all = ["Current Ratio", "Debt/Equity Ratio", "Net Profit Margin",
              "ROE - Return On Equity", "EBITDA Margin", "Gross Margin",
                "Long-term Debt / Capital", "Asset Turnover", "ROA - Return On Assets",
                "Operating Margin"]
#Sélectionner les ratios normalisés
df_normalized[ratios_all] = scaler.fit_transform(df[ratios_all])

df_normalized[ratios_all].head()
#%% Ajouts de ratios combinés
#X: ratios normalisés Y: Notation format numérique
X = df_normalized[ratios_all]
y = df["Rating_Score"]

#Création ratios combinés
    #ROE pondérée par la marge nette 
X["ROE_x_NetProfitMargin"] = X["ROE - Return On Equity"] * X["Net Profit Margin"]
    #Endettement ajusté à la rentabilité
X["DebtEquity_x_ROA"] = X["Debt/Equity Ratio"] * X["ROA - Return On Assets"]
    #Rentabilité opérationnelle vs efficacité des actifs
X["EBITDAmargin_x_ROA"] = X["EBITDA Margin"] * X["ROA - Return On Assets"]

X.columns 

#%%
#Initialiser le modèle KFold pour la validation croisée avec 5 plis
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_errors = []
rmse_errors = []
r2_scores = []

for train_index, test_index in kf.split(X):
    #Séparer les données en ensembles d'entraînement et de test
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    #Modèle de régression linéaire
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    #Prédictions sur l'ensemble de test
    y_pred = model.predict(X_test)
    
    #Calcul des métriques de performance 
    mse = mean_squared_error(y_test, y_pred)
    rmse = sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    #Résultats
    mse_errors.append(mse)
    rmse_errors.append(rmse)
    r2_scores.append(r2)

#Résultats de la validation croisée
print("Validation croisée (Régression linéaire):")
print(f"Erreur quadratique moyenne (MSE) moyenne : {np.mean(mse_errors):.4f}")
print(f"Écart-type du MSE : {np.std(mse_errors):.4f}")
print(f"Erreur quadratique moyenne racine (RMSE) moyenne : {np.mean(rmse_errors):.4f}")
print(f"Écart-type du RMSE : {np.std(rmse_errors):.4f}")
print(f"R² moyen : {np.mean(r2_scores):.4f}")
print(f"Écart-type du R² : {np.std(r2_scores):.4f}")

#%% 
#Importation de l'arbre de décision
from sklearn.tree import DecisionTreeRegressor

#Initialiser la validation croisée avec 5 plis
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_errors_tree = []
rmse_errors_tree = []
r2_scores_tree = []

#Modèle d'arbre de décision
tree_model = DecisionTreeRegressor(random_state=42, max_depth=5)  # Vous pouvez ajuster max_depth pour éviter l'overfitting

for train_index, test_index in kf.split(X):
    #Diviser les données en ensembles d'entraînement et de test
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    #Entraîner le modèle d'arbre de décision
    tree_model.fit(X_train, y_train)
    
    #Prédictions sur l'ensemble de test
    y_pred_tree = tree_model.predict(X_test)
    
    #Calcul des métriques
    mse_tree = mean_squared_error(y_test, y_pred_tree)
    rmse_tree = sqrt(mse_tree)
    r2_tree = r2_score(y_test, y_pred_tree)
    
    #Résultats
    mse_errors_tree.append(mse_tree)
    rmse_errors_tree.append(rmse_tree)
    r2_scores_tree.append(r2_tree)

#Résultats de la validation croisée pour l'arbre de décision
print("\nValidation croisée (Arbre de décision) :")
print(f"Erreur quadratique moyenne (MSE) moyenne : {np.mean(mse_errors_tree):.4f}")
print(f"Écart-type du MSE : {np.std(mse_errors_tree):.4f}")
print(f"Erreur quadratique moyenne racine (RMSE) moyenne : {np.mean(rmse_errors_tree):.4f}")
print(f"Écart-type du RMSE : {np.std(rmse_errors_tree):.4f}")
print(f"R² moyen : {np.mean(r2_scores_tree):.4f}")
print(f"Écart-type du R² : {np.std(r2_scores_tree):.4f}")

#%%
#Meilleure performancce globale : baisse du MSE et RMSE, hausse du R²
#Modèle plus stable baisse des écarts-types
#%% 
#Features Importance

#Importance des variables
importances = tree_model.feature_importances_

#Création d'une série pandas pour l'affichage
feature_importance = pd.Series(importances, index=X.columns)

#Trier les variables par importance décroissante
feature_importance = feature_importance.sort_values(ascending=True)

#Affichage avec un graphique horizontal
plt.figure(figsize=(10, 6))
feature_importance.plot(kind='barh', color='steelblue')
plt.title("Importance des variables (Arbre de décision)")
plt.xlabel("Score d'importance")
plt.tight_layout()
plt.show()

#%% Ajout de variables à df avant normalisation
#Inverse le LTD car interprétation inverse 
df["Inverse_Long-term Debt/Capital"] = 1 / df["Long-term Debt / Capital"]
df["Inverse_Debt/Equity Ratio"] = 1 / df["Debt/Equity Ratio"]

#Ajout du ROE pondérée par la marge nette dans df
df["ROE_x_NetProfitMargin"] = df["ROE - Return On Equity"] * df["Net Profit Margin"]

df.columns

#%% Réadaptation des variables
ratios_all1 = ["Current Ratio", "Net Profit Margin", "ROE - Return On Equity", 
               "EBITDA Margin", "Gross Margin", "Inverse_Long-term Debt/Capital", 
               "Inverse_Debt/Equity Ratio", "ROA - Return On Assets", 
               "Operating Margin", "ROE_x_NetProfitMargin"]

#Sélectionner les ratios normalisés 
df_normalized[ratios_all1] = scaler.fit_transform(df[ratios_all1])

df_normalized[ratios_all1].head()

#%% 
#X: ratios normalisés Y: Notation format numérique
X = df_normalized[ratios_all1]
y = df["Rating_Score"]

X.columns

#%%
#Initialiser la validation croisée avec 5 plis
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_errors_tree = []
rmse_errors_tree = []
r2_scores_tree = []

#Modèle d'arbre de décision
tree_model = DecisionTreeRegressor(random_state=42, max_depth=5)  # Vous pouvez ajuster max_depth pour éviter l'overfitting

for train_index, test_index in kf.split(X):
    #Diviser les données en ensembles d'entraînement et de test
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    #Entraîner le modèle d'arbre de décision
    tree_model.fit(X_train, y_train)
    
    #Prédictions sur l'ensemble de test
    y_pred_tree = tree_model.predict(X_test)
    
    #Calcul des métriques
    mse_tree = mean_squared_error(y_test, y_pred_tree)
    rmse_tree = sqrt(mse_tree)
    r2_tree = r2_score(y_test, y_pred_tree)

    #Résultats
    mse_errors_tree.append(mse_tree)
    rmse_errors_tree.append(rmse_tree)
    r2_scores_tree.append(r2_tree)

#Résultats de la validation croisée pour l'arbre de décision
print("\nValidation croisée (Arbre de décision) :")
print(f"Erreur quadratique moyenne (MSE) moyenne : {np.mean(mse_errors_tree):.4f}")
print(f"Écart-type du MSE : {np.std(mse_errors_tree):.4f}")
print(f"Erreur quadratique moyenne racine (RMSE) moyenne : {np.mean(rmse_errors_tree):.4f}")
print(f"Écart-type du RMSE : {np.std(rmse_errors_tree):.4f}")
print(f"R² moyen : {np.mean(r2_scores_tree):.4f}")
print(f"Écart-type du R² : {np.std(r2_scores_tree):.4f}")

#%%
#L'ajout de nouvelles variables  dans X rend le modèle moins pertinent
#%% Modèle de Gradient Boosting
from sklearn.ensemble import GradientBoostingRegressor

X.columns
#%%
#Initialiser la validation croisée avec 5 plis
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_errors_gb = []
rmse_errors_gb = []
r2_scores_gb = []

#Modèle de Gradient Boosting
gb_model = GradientBoostingRegressor(random_state=42, n_estimators=100, learning_rate=0.1, max_depth=5)

for train_index, test_index in kf.split(X):
    #Diviser les données en ensembles d'entraînement et de test
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    #Entraîner le modèle de Gradient Boosting
    gb_model.fit(X_train, y_train)
    
    #Prédictions sur l'ensemble de test
    y_pred_gb = gb_model.predict(X_test)
    
    #Calcul des métriques
    mse_gb = mean_squared_error(y_test, y_pred_gb)
    rmse_gb = sqrt(mse_gb)
    r2_gb = r2_score(y_test, y_pred_gb)
    
    #Résultats
    mse_errors_gb.append(mse_gb)
    rmse_errors_gb.append(rmse_gb)
    r2_scores_gb.append(r2_gb)

#Résultats de la validation croisée pour le Gradient Boosting
print("\nValidation croisée (Gradient Boosting) :")
print(f"Erreur quadratique moyenne (MSE) moyenne : {np.mean(mse_errors_gb):.4f}")
print(f"Écart-type du MSE : {np.std(mse_errors_gb):.4f}")
print(f"Erreur quadratique moyenne racine (RMSE) moyenne : {np.mean(rmse_errors_gb):.4f}")
print(f"Écart-type du RMSE : {np.std(rmse_errors_gb):.4f}")
print(f"R² moyen : {np.mean(r2_scores_gb):.4f}")
print(f"Écart-type du R² : {np.std(r2_scores_gb):.4f}")

#%%
#GradientBoost : Meilleure performance globale du modèle : baisse du MSE et RMSE, hausse du R²

#%%
#Importance des variables
gb_importances = gb_model.feature_importances_

 #Création d'une série pandas pour l'affichage
gb_feature_importance = pd.Series(gb_importances, index=X.columns)

#Trier les variables par importance décroissante
gb_feature_importance = gb_feature_importance.sort_values(ascending=True)

#Affichage avec un graphique horizontal
plt.figure(figsize=(10, 6))
gb_feature_importance.plot(kind='barh', color='darkorange')
plt.title("Importance des variables (Gradient Boosting)")
plt.xlabel("Score d'importance")
plt.tight_layout()
plt.show()

#%% Modèle XGBoost
from xgboost import XGBRegressor

#Initialiser la validation croisée avec 5 plis
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_errors_xgb = []
rmse_errors_xgb = []
r2_scores_xgb = []

#Modèle XGBoost
xgb_model = XGBRegressor(random_state=42, n_estimators=100, learning_rate=0.1, max_depth=5)

for train_index, test_index in kf.split(X):
    #Diviser les données en ensembles d'entraînement et de test
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    #Entraîner le modèle XGBoost
    xgb_model.fit(X_train, y_train)
    
    #Prédictions sur l'ensemble de test
    y_pred_xgb = xgb_model.predict(X_test)
    
    #Calcul des métriques
    mse_xgb = mean_squared_error(y_test, y_pred_xgb)
    rmse_xgb = sqrt(mse_xgb)
    r2_xgb = r2_score(y_test, y_pred_xgb)
    
    #Stocker les résultats
    mse_errors_xgb.append(mse_xgb)
    rmse_errors_xgb.append(rmse_xgb)
    r2_scores_xgb.append(r2_xgb)

#Résultats de la validation croisée pour XGBoost
print("\nValidation croisée (XGBoost) :")
print(f"Erreur quadratique moyenne (MSE) moyenne : {np.mean(mse_errors_xgb):.4f}")
print(f"Écart-type du MSE : {np.std(mse_errors_xgb):.4f}")
print(f"Erreur quadratique moyenne racine (RMSE) moyenne : {np.mean(rmse_errors_xgb):.4f}")
print(f"Écart-type du RMSE : {np.std(rmse_errors_xgb):.4f}")
print(f"R² moyen : {np.mean(r2_scores_xgb):.4f}")
print(f"Écart-type du R² : {np.std(r2_scores_xgb):.4f}")

#%%
#GradientBoost légèrement plus performant que XGBoost
#%% SCORE RISQUE
#%% Extraction des pondérations pour SCORE RISQUE 
#Importance des variables à partir du modèle Gradient Boosting
gb_importances = gb_model.feature_importances_

#Création d'une série pandas pour associer les pondérations aux variables
weights_new = pd.Series(gb_importances, index=X.columns)
#Convertir les pondérations pour avoir une somme de 1
weights_new /= weights_new.sum() 

print("Pondérations des variables (Gradient Boosting) :")
print(weights_new)


#%%
#Score de risque ajusté avec les nouvelles pondérations
df_normalized["New_Risk_Score"] = (df_normalized[X.columns] * weights_new).sum(axis=1)
#Arrondis et multiplication pour un score [0;10]
df_normalized["New_Risk_Score"] = (df_normalized["New_Risk_Score"] * 10).round(2)

print(df_normalized[["Corporation", "New_Risk_Score"]].head())

#%%
#Classification du Risk_Score
def classify_risk(score):
    if score >= 6:
        return "Very Low"
    elif score >= 5:
        return "Low"
    elif score >= 4.5:
        return "Moderate"
    elif score >= 3.5:
        return "High"
    else:
        return "Very High"

df_normalized["Risk_level"] = df_normalized["New_Risk_Score"].apply(classify_risk)

print(df_normalized[["Corporation", "New_Risk_Score", "Risk_level"]].head())

#%% Sector risque 
#Moyennes des variables par secteur
sector_means = df_normalized.groupby("Sector")[X.columns].mean()

#Sector Risk Score
sector_means["SectorRisk_Score"] = (sector_means[X.columns] * weights_new).sum(axis=1)
#Arrondis et multiplication pour un score [0;10]
sector_means["SectorRisk_Score"] = (sector_means["SectorRisk_Score"] * 10).round(2)

print(sector_means[["SectorRisk_Score"]])

#%% 
#Ajouter le Sector Risk Score aux données des entreprises
df_normalized = pd.merge(df_normalized, sector_means[["SectorRisk_Score"]],
    left_on="Sector", right_index=True)

df_normalized.columns

#%%
#Comparaison entre le Risk Score et le Sector Risk Score
df_normalized["Risk_Comparaison1"] = df_normalized["New_Risk_Score"] - df_normalized["SectorRisk_Score"]

print(df_normalized[["Corporation", "New_Risk_Score", "SectorRisk_Score", "Risk_Comparaison1"]].head())

#%%
df_normalized[["New_Risk_Score"]].head(100)

#%%
#Distribution du Sector Risk Score
plt.figure(figsize=(12, 6))
sns.histplot(df_normalized["SectorRisk_Score"], bins=30, kde=True, color="green", label="New Risk Score", alpha=0.6)
plt.title("Distribution du Sector Risk Score")
plt.xlabel("Score de risque")
plt.ylabel("Fréquence")
plt.legend()
plt.grid(True)
plt.show()


#%%
df_normalized["SectorRisk_Score"].describe()

#%%
df_normalized[["Corporation", "Investment Grade", "New_Risk_Score", "SectorRisk_Score", "Risk_level"]].head(50)
#%%
#Conversion Rating Date en chaîne de caractères
df["Rating Date2"] = df["Rating Date"].astype(str)
df_normalized["Rating Date2"] = df_normalized["Rating Date"].astype(str)

#Clé composite dans les deux DataFrames
df["Composite_Key"] = df["CIK"].astype(str) + "_" + df["Corporation"] + "_" + df["Rating Date2"]
df_normalized["Composite_Key"] = df_normalized["CIK"].astype(str) + "_" + df_normalized["Corporation"] + "_" + df_normalized["Rating Date2"]

#Vérification de la clé composite
print(df["Composite_Key"].head())
print(df_normalized["Composite_Key"].head())

#%%
#Doublons de la clé composite dans df
print("Doublons dans la clé composite (table non normalisée) :", df["Composite_Key"].duplicated().sum())

#Doublons de la clé composite dans df_normalized
print("Doublons dans la clé composite (table normalisée) :", df_normalized["Composite_Key"].duplicated().sum())

#%%
#Vérifier les valeurs uniques dans les deux tables
unique_keys_df = set(df["Composite_Key"].unique())
unique_keys_df_normalized = set(df_normalized["Composite_Key"].unique())


print("Clés présentes dans df mais pas dans df_normalized :", unique_keys_df - unique_keys_df_normalized)
print("Clés présentes dans df_normalized mais pas dans df :", unique_keys_df_normalized - unique_keys_df)

# %%
#EXPORT DES DONNEES
#%%
print(df.columns)
print(df_normalized.columns)

#%%
print(df.info())
print(df_normalized.info())

#%%
#Sélection des colonnes à exporter
export_colonnes1 = ["CIK", "Corporation", "SIC Code", "Sector", "SubSector", "Industry", 
                   "Rating Agency", "Rating", "Rating Date", "Rating_Score","Investment Grade", 
                   "Current Ratio", "Debt/Equity Ratio", "Net Profit Margin", "ROE - Return On Equity", 
                   "Current Ratio_Sector_Median", "Debt/Equity Ratio_Sector_Median",
                   "Net Profit Margin_Sector_Median","ROE - Return On Equity_Sector_Median",
                   "Risk_Score", "Risk_Category", "Composite_Key"]

export_colonnes2 = export_colonnes1 + ["New_Risk_Score", "Sector_Risk_Score", "SectorRisk_Score", 
                                       "Risk_level", "Risk_Comparaison", "Performance_vs_Sector", "Risk_Comparaison1"]

#Export des données non normalisées
df[export_colonnes1].to_excel("CorporateCredit_NonNormalized.xlsx", index=False)

#Export des données normalisées
df_normalized[export_colonnes2].to_excel("CorporateCredit_Normalized.xlsx", index=False)

print("Export terminé : fichiers Excel générés.")
