SELECT DISTINCT people.name
FROM people, stars, movies, (SELECT movies.id, people.name
FROM movies, stars, people
WHERE movies.id=stars.movie_id
AND stars.person_id=people.id
AND people.name='Kevin Bacon'
AND people.birth=1958)AS kb

WHERE people.id=stars.person_id
AND movies.id=stars.movie_id
AND movies.id=kb.id
AND people.name != kb.name;

