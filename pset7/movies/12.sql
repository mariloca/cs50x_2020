SELECT hbc.title
FROM
(
SELECT movies.title
FROM people, stars, movies
WHERE people.id=stars.person_id
AND stars.movie_id=movies.id
AND people.name='Helena Bonham Carter'
) AS hbc
INNER JOIN
(
SELECT movies.title
FROM people, stars, movies
WHERE people.id=stars.person_id
AND stars.movie_id=movies.id
AND people.name='Johnny Depp'
) AS jd ON hbc.title=jd.title;
