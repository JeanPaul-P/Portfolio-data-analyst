# projet-notation-credit
The goal of this analysis project is to evaluate and monitor corporate credit risk by using the “Corporate Credit Rating with Financial Ratios” dataset available on Kaggle. 

#Goals
- Analyse the factors influencing a company's credit rating.
- Determine which financial ratios are the most relevant for evaluating risk.
- Build a personalised risk score based on financial ratios.
- Track changes in ratings and risk over time.
- Create an intuitive and interactive Power BI dashboard with useful insights for decision-making.

#Tools and Technologies
- Excel : Pivot tables, Power Query, Web scraping. 
- Python : Pandas, Numpy, Matplotlib, Seaborn, SciPy, Scikit-Learn et XGBoost.
- Power BI : Power Query, DAX.

#Methodology
1. Loading and exploring the data
   - Downloading the dataset and exploring it in Excel.
   - Check the structure.

2. Data extraction, preparation and cleaning
   - Extraction of company financial data from Excel files.
   - Loading of a supplementary table containing sectoral details, web scraping from the US government site (SIC Code). 
   - Handling missing values, removing duplicates, renaming columns and filtering data.
     
3. Exploratory data analysis (EDA)
   - Visualisation of the distribution of credit ratings.
   - Analysis of key financial ratio distributions (Current Ratio, Debt/Equity Ratio, Net Profit Margin, etc.).
   - Identification of outliers using the IQR (Interquartile Range) method.
   - Study of the relationships between financial ratios and credit ratings using correlation matrices and scatter plots.
     
4. Création of risk scores
   - Conversion of credit ratings into numerical scores.
   - Calculation of risk scores for companies by weighting financial ratios according to their correlation with ratings.
   - Classification of companies into risk categories (Low, Moderate, High).
     
5. Sector analysis 
   - Calculation of medians of financial ratios by sector.
   - Creation of sector risk scores based on normalised medians.
   - Comparison of company risk scores with sector scores.
     
6. Data normalisation
   - Application of Min-Max normalisation on financial ratios to reduce the impact of extreme values.
   - Winsorisation of ratios to limit outliers.
     
7. Cross-validation and machine learning models
   - Use of cross-validation (K-Fold) to evaluate the robustness of ratio weightings.
   - Implementation of several regression models: linear regression, decision tree, gradient boosting and XGBoost.
   - Comparison of model performance using MSE, RMSE and R² metrics.
   - Analysis of the importance of variables for the models and adjustment of ratio weights.
   - Calculation of the new risk score

8. Data export
   - Selection of relevant columns for the export.
   - Export of two Excel files: Non-normalised data and normalised data with adjusted risk scores.
     
9. Power BI dashboard
   - Filters by company, sector, year and risk level.
   - Dynamic gauges of financial ratios with sector and business objectives.
   - KPI map.
   - Summary table.

