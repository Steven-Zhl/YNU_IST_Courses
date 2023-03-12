-- 单表查询例子

-- 1. 简单的单表查询（使用DISTINCT关键字）：查询不同语言的使用情况

SELECT
    DISTINCT count(*),
    Language
FROM countrylanguage
GROUP BY(Language)
ORDER BY count(*) DESC
LIMIT 20;

-- 2. 带ORDER BY的单表查询：查询各个国家的人数，并降序排列

SELECT Name, Population
FROM country
ORDER BY Population DESC
LIMIT 20;

-- 3. 带GROUP BY+HAVING+ORDER BY的单表查询：查询在city中的个数大于等于5个的国家，按降序排列

SELECT
    CountryCode,
    COUNT(*) AS '城市数'
FROM city
GROUP BY(CountryCode)
HAVING COUNT(*) >= 5
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 4. 选择表中的若干元组（WHERE IN）：查询五常国家的城市

SELECT Name
FROM city
WHERE
    CountryCode IN (
        'CHN',
        'RUS',
        'USA',
        'GBR',
        'FRA'
    )
LIMIT 20;

-- 5. 选择表中的若干元组（WHERE =、>=、<=、BETWEEN AND）：查询人口在1亿到10亿的国家

SELECT Name, Population
FROM country
WHERE
    Population BETWEEN 100000000 AND 1000000000;

-- 6. 包含聚集函数的单表查询：查询各大洲的国家数

SELECT
    Continent,
    COUNT(*) AS '国家数'
FROM country
GROUP BY(Continent)
ORDER BY(COUNT(*)) DESC;

-- 连接查询例子

-- 1. 简单的连接查询：查询亚洲国家及其官方语言

SELECT
    country.Name AS '国家',
    countrylanguage.Language AS '官方语言'
FROM country, countrylanguage
WHERE
    country.Code = countrylanguage.CountryCode
    AND country.Continent = 'Asia'
    AND countrylanguage.IsOfficial = 'T'
LIMIT 20;

-- 2. 自身连接：查询使用中国使用的语言的国家

SELECT
    OTHER.CountryCode AS '国家',
    OTHER.Language AS '语言',
    CHN.Language AS '中国使用的语言'
FROM
    countrylanguage OTHER,
    countrylanguage CHN
WHERE
    OTHER.Language = CHN.Language
    AND OTHER.CountryCode != 'CHN'
    AND CHN.CountryCode = 'CHN'
LIMIT 20;

-- 3. 查询人数最多的城市所在的洲

SELECT
    city.Name,
    country.Continent
FROM city, country
WHERE
    city.CountryCode = country.Code
    AND city.Population = (
        SELECT
            MAX(Population)
        FROM city
    );

-- 4. 多表连接：查询各大洲的语言数

SELECT
    DISTINCT Continent,
    COUNT(Language)
FROM
    country,
    city,
    countrylanguage
WHERE
    country.Code = countrylanguage.CountryCode
    AND country.Code = city.CountryCode
GROUP BY(Continent);

-- 5. 多表连接：查询名字最长的城市及所在国家和大洲

SELECT
    city.Name AS '城市名',
    country.Name,
    country.Continent
FROM city, country
WHERE
    city.CountryCode = country.Code
    AND LENGTH(city.Name) = (
        SELECT
            MAX(LENGTH(Name))
        FROM city
    );