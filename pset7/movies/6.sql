SELECT AVG(ratings.rating) as 'Average Rating of 2012' FROM ratings,movies
WHERE movies.id=ratings.movie_id
AND movies.year=2012;
