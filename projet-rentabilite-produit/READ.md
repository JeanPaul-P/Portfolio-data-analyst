# projet-rentabilite-produit

This project aims to analyse and visualise the **most profitable products and categories** by comparing costs and sales based on the ‘AdventureWorks’ database. 
It combines the use of **SQL** for data extraction, calculations and transformations, and **Power BI** for visualisation and business and strategic decision support.

---

## 🎯 Goals

- Identify the most and least profitable products and categories.
- Measure the impact of standard costs on overall profitability.
- Analyse margins by product, subcategory, and category.
- Provide a dynamic dashboard to support strategic decisions.

---

## 🛠️ Tools and Technologies

- **SQL Server**: Data extraction and calculation via views.
- **Power Query**: Data transformation within Power BI.
- **DAX (Power BI)**: Custom measures and KPIs.
- **Power BI**: Data visualisation, dynamic filters, and dashboards.

---

## 🧠 Methodology

### 1. Data extraction and transformation with SQL

- Creation of a SQL **view `vw_ProductProfitability`** joining several AdventureWorks tables:
  - `Sales.SalesOrderHeader` & `Sales.SalesOrderDetail` for order data.
  - `Production.Product`, `ProductSubcategory`, `ProductCategory` for product metadata.
  - `Production.ProductCostHistory` to extract the most recent **standard cost** per product.

- Calculated fields:
  - **Unit Margin** = Unit Price − Standard Cost  
  - **Total Margin** = Unit Margin × Quantity

> 🔎 See full SQL code in `/sql/Code.sql`.

---

### 2. Power BI - Data preparation with Power Query

- **Connection to the SQL View** using Power BI.
- Transformation steps:
  - Changed data types (e.g. OrderDate as date).
  - Extracted the **year** from the OrderDate using Power Query steps.


---

### 3. DAX Measures

- `Total Sales = SUM(ProductProfitability[LineTotal])`
- `Total Cost = SUM(ProductProfitability[StandardCost] * ProductProfitability[OrderQty])`
- `Total Margin = SUM(ProductProfitability[TotalMargin])`
- `Margin % = DIVIDE([Total Margin], [Total Sales])`

These KPIs allow dynamic calculation of performance across categories and time periods.

---

### 4. Power BI Dashboard

An interactive dashboard was created with the following features:

- **Filters**:
  - By product category, subcategory, and year.
- **Profitability KPIs**:
  - Total Sales, Total Margin, Margin %, and Total Cost.
- **Visualisations**:
  - Bar charts by product and category.
  - Trend analysis over time.
  - Matrix of products with profitability metrics.

---
