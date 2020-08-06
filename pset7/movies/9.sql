/*some stars may share the same name but different birth year, but they all have a unique id
so to use DISTINCT people.id instead of DISTINCT people.name would actually filter out same name with diff birth year*/

SELECT people.name
FROM people,
(
SELECT DISTINCT people.id
FROM movies, people, stars
WHERE movies.id=stars.movie_id AND people.id=stars.person_id
AND movies.year=2004
ORDER BY people.birth)AS x
WHERE people.id=x.id;
