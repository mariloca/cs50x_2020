SELECT people.name
FROM people, stars, movies
WHERE people.id=stars.person_id and movies.id=stars.movie_id
AND movies.title='Toy Story';
