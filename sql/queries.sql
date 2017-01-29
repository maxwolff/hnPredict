SELECT 
	stories.title AS stories_title,
	stories.score AS stories_score,
	stories.text AS stories_text,
	stories.descendants AS stories_descendants,
  stories.url AS stories_url,
	//COUNT(DISTINCT stories.url, 1000) AS stories_count_url
FROM [fh-bigquery:hackernews.stories]
 AS stories

WHERE 
	(stories.score > 10)
GROUP EACH BY 1,2,3,4,5
ORDER BY 1 
LIMIT 50


# grab URLS
SELECT 
	REGEXP_EXTRACT((REGEXP_EXTRACT(stories.url,'http://([^/]+)/')),'([^\\.]+\\.[^\\.]+(?:\\.[a-zA-Z].)?)$') AS stories_url_domain,
	COUNT(stories.id) AS stories_count,
	COUNT(CASE WHEN stories.score >= 7 THEN 1 ELSE NULL END) AS storiescountscore_7_plus,
	100.0 * (COUNT(CASE WHEN stories.score >= 7 THEN 1 ELSE NULL END)) / (COUNT(stories.id)) AS stories_percent_7_plus
FROM [fh-bigquery:hackernews.stories]
 AS stories

WHERE 
	(((REGEXP_EXTRACT((REGEXP_EXTRACT(stories.url,'http://([^/]+)/')),'([^\\.]+\\.[^\\.]+(?:\\.[a-zA-Z].)?)$')) IS NOT NULL))
GROUP EACH BY 1
HAVING 
	(COUNT(CASE WHEN stories.score >= 7 THEN 1 ELSE NULL END) >= 6)
ORDER BY 3 DESC
LIMIT 500


# https://looker.com/publicdata/hackernews/explore/15?