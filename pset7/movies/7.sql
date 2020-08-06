SELECT movies.title, ratings.rating
FROM movies,ratings
WHERE ratings.rating IS NOT NULL
AND movies.id=ratings.movie_id
AND year=2010
ORDER BY ratings.rating DESC, movies.title ASC;
