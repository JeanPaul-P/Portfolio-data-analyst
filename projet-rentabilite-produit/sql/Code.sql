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
	-- Total de la ligne (quantit� * prix unitaire)
    sod.LineTotal,
	-- Co�t standard unitaire du produit (0 si absent)
    ISNULL(pch.StandardCost, 0) AS StandardCost,
	-- Marge unitaire (prix de vente - co�t)
    (sod.UnitPrice - ISNULL(pch.StandardCost, 0)) AS UnitMargin,
	-- Marge totale (unitaire * quantit�)
    ((sod.UnitPrice - ISNULL(pch.StandardCost, 0)) * sod.OrderQty) AS TotalMargin
FROM Sales.SalesOrderDetail sod
-- Jointure avec l�en-t�te de la commande pour r�cup�rer la date et d�autres infos g�n�rales
JOIN Sales.SalesOrderHeader soh ON soh.SalesOrderID = sod.SalesOrderID
-- Jointure avec la table Produit pour r�cup�rer les d�tails du produit vendu
JOIN Production.Product p ON p.ProductID = sod.ProductID
-- Jointure gauche pour r�cup�rer la sous-cat�gorie du produit
LEFT JOIN Production.ProductSubcategory psc ON psc.ProductSubcategoryID = p.ProductSubcategoryID
-- Jointure gauche pour r�cup�rer la cat�gorie du produit
LEFT JOIN Production.ProductCategory pc ON pc.ProductCategoryID = psc.ProductCategoryID

-- Sous-requ�te inline pour r�cup�rer la date la plus r�cente du co�t par produit
LEFT JOIN (
    SELECT ProductID, MAX(ModifiedDate) AS LatestDate
    FROM Production.ProductCostHistory
    GROUP BY ProductID
) latestCost ON latestCost.ProductID = p.ProductID
-- Jointure avec la table de co�t r�el pour r�cup�rer le co�t standard correspondant � la derni�re date modifi�e
LEFT JOIN Production.ProductCostHistory pch 
	ON pch.ProductID = latestCost.ProductID 
	AND pch.ModifiedDate = latestCost.LatestDate

