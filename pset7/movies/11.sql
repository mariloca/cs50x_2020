SELECT movies.title
FROM ratings, people, stars, movies
WHERE ratings.movie_id=movies.id
AND people.id=stars.person_id
AND stars.movie_id=movies.id
AND people.name='Chadwick Boseman'
ORDER BY ratings.rating DESC LIMIT 5;
