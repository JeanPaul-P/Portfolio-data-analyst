CREATE VIEW vw_ProductProfitability AS
SELECT
    soh.SalesOrderID,
    soh.OrderDate,
    p.ProductID,
    p.Name AS ProductName,
    pc.Name AS Category,
    psc.Name AS SubCategory,
    sod.OrderQty,
    sod.UnitPrice,
	-- Total de la ligne (quantité * prix unitaire)
    sod.LineTotal,
	-- Coût standard unitaire du produit (0 si absent)
    ISNULL(pch.StandardCost, 0) AS StandardCost,
	-- Marge unitaire (prix de vente - coût)
    (sod.UnitPrice - ISNULL(pch.StandardCost, 0)) AS UnitMargin,
	-- Marge totale (unitaire * quantité)
    ((sod.UnitPrice - ISNULL(pch.StandardCost, 0)) * sod.OrderQty) AS TotalMargin
FROM Sales.SalesOrderDetail sod
-- Jointure avec l’en-tête de la commande pour récupérer la date et d’autres infos générales
JOIN Sales.SalesOrderHeader soh ON soh.SalesOrderID = sod.SalesOrderID
-- Jointure avec la table Produit pour récupérer les détails du produit vendu
JOIN Production.Product p ON p.ProductID = sod.ProductID
-- Jointure gauche pour récupérer la sous-catégorie du produit
LEFT JOIN Production.ProductSubcategory psc ON psc.ProductSubcategoryID = p.ProductSubcategoryID
-- Jointure gauche pour récupérer la catégorie du produit
LEFT JOIN Production.ProductCategory pc ON pc.ProductCategoryID = psc.ProductCategoryID

-- Sous-requête inline pour récupérer la date la plus récente du coût par produit
LEFT JOIN (
    SELECT ProductID, MAX(ModifiedDate) AS LatestDate
    FROM Production.ProductCostHistory
    GROUP BY ProductID
) latestCost ON latestCost.ProductID = p.ProductID
-- Jointure avec la table de coût réel pour récupérer le coût standard correspondant à la dernière date modifiée
LEFT JOIN Production.ProductCostHistory pch 
	ON pch.ProductID = latestCost.ProductID 
	AND pch.ModifiedDate = latestCost.LatestDate

