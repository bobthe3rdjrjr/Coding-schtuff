import requests
import argparse

def get_arguments() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, required=True, choices=["playing", "popular", "top", "upcoming"])
    args = parser.parse_args()
    return args.type

def get_movies(type: str) -> requests.Response:
    if type == "playing":
        movies = requests.get("https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_release_type=2|3&release_date.gte={min_date}&release_date.lte={max_date}", headers={'Authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZTI1YmZiODA2YWUwMjAxMzJlOGQzZTQ4ODBiZGI4NSIsIm5iZiI6MTc3NTU5NTgxNi45LCJzdWIiOiI2OWQ1NzEyODFhZjU5MjFjZmEzMTQwNTMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.YRJbjuyP3LanalFyye_rSVGdFyMBtbYTbh13j2HLT1U"})
    elif type == "popular":
        movies = requests.get("https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc", headers={'Authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZTI1YmZiODA2YWUwMjAxMzJlOGQzZTQ4ODBiZGI4NSIsIm5iZiI6MTc3NTU5NTgxNi45LCJzdWIiOiI2OWQ1NzEyODFhZjU5MjFjZmEzMTQwNTMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.YRJbjuyP3LanalFyye_rSVGdFyMBtbYTbh13j2HLT1U"})
    elif type == "top":
        movies = requests.get("https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=vote_average.desc&without_genres=99,10755&vote_count.gte=200", headers={'Authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZTI1YmZiODA2YWUwMjAxMzJlOGQzZTQ4ODBiZGI4NSIsIm5iZiI6MTc3NTU5NTgxNi45LCJzdWIiOiI2OWQ1NzEyODFhZjU5MjFjZmEzMTQwNTMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.YRJbjuyP3LanalFyye_rSVGdFyMBtbYTbh13j2HLT1U"})
    elif type == "upcoming":
        movies = requests.get("https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_release_type=2|3&release_date.gte={min_date}&release_date.lte={max_date}", headers={'Authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZTI1YmZiODA2YWUwMjAxMzJlOGQzZTQ4ODBiZGI4NSIsIm5iZiI6MTc3NTU5NTgxNi45LCJzdWIiOiI2OWQ1NzEyODFhZjU5MjFjZmEzMTQwNTMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.YRJbjuyP3LanalFyye_rSVGdFyMBtbYTbh13j2HLT1U"})

    if not movies:
        raise RuntimeError("Something went wrong.", 2)
    return movies.json()
    
if __name__ == "__main__":
    type: str = get_arguments()
    print(get_movies(type))