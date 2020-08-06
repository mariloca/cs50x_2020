SELECT DISTINCT people.name
FROM people, directors, movies, ratings
WHERE people.id=directors.person_id
AND directors.movie_id=movies.id
AND ratings.movie_id=movies.id
AND ratings.rating >= 9.0;
