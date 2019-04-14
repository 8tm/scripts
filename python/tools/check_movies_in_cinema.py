#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------

""" Check movies in cinema (HELIOS) """

__author__ = "Tadeusz Miszczyk"
__version__ = "1.2.0"

# ----------------------------------------------------------------------------------------------------------------------

import os
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + '/../library/')
import mylib.email
import mylib.network
import mylib.templates
import mylib.variables_sensitive

# ----------------------------------------------------------------------------------------------------------------------


def get_movie_info(source):

    trailer = source.find('div', {'class': 'movie-trailer'})
    if trailer:
        *_, trailer, _ = str(trailer.find("a")).split('"')
        trailer = mylib.network.get_website_source_code("{0}{1}".format("https://www.helios.pl", trailer))
        trailer = str(trailer.find('figure', {'class': 'slide-media'}).find('iframe')).split('"')[-4]
    else:
        trailer = ""

    category = source.find('div', {'class': 'movie-category'})
    category = str(category.find("p")).replace('<p>', '').replace('</p>', '') if category else None

    movie_info = str(source.find('figure', {'class': 'movie-media'}).find("img"))

    movie_data = {'title': movie_info.split('"')[1],
                  'url': "https://www.helios.pl{0}".format(str(source.find("a")).split('"')[1]),
                  'poster': movie_info.split('"')[3].replace("/mvpstrmin/", "/mvpstr/"),
                  'trailer': trailer,
                  'category': category}
    return movie_data


# ----------------------------------------------------------------------------------------------------------------------


def get_movies(url_address):
    source = mylib.network.get_website_source_code(url_address)
    movies = source.find('ul', {'class': 'seances-list'}).findAll('div', {'class': 'movie'})

    links, titles = [], []
    movie_template = """<a href="{trailer}"><img width="100%" style="display:block" src="{poster}"></a>{category}
[<a href="{url}">&nbsp;\"{title}\" w HELIOS&nbsp;</a>]<br>""".replace('\n', '')

    for movie in movies:
        movie_data = get_movie_info(movie)
        if movie_data['title'] not in titles:
            category = "<br>{category}".format(
                category="Kategoria: {0}<br>".format(movie_data['category']) if movie_data['category'] else "")
            links.append(movie_template.format(title=movie_data['title'],
                                               poster=movie_data['poster'],
                                               url=movie_data['url'],
                                               trailer=movie_data['trailer'],
                                               category=category))
            titles.append(movie_data['title'])
    return links

# ----------------------------------------------------------------------------------------------------------------------


def save_movies(lista, file_name):
    with open(file_name, 'w+') as f:
        [f.write("{0}\n".format(movie)) for movie in lista]

# ----------------------------------------------------------------------------------------------------------------------


def load_movies(file_name):
    with open(file_name, 'r+') as f:
        return [movie.rstrip('\n') for movie in f.readlines()]

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    file_name = 'movies.txt'

    new_movies = get_movies('https://www.helios.pl/3,Wroclaw/Repertuar/')
    old_movies = load_movies(file_name) if os.path.exists(file_name) else []
    added_movies = [movie for movie in new_movies if movie not in old_movies]
    save_movies(new_movies, file_name)

    email_title = "{0} new movie(s)".format(len(added_movies))
    print("Found {0}".format(email_title))

    if added_movies:
        zm = {'title': email_title,
              'movies': "<center>{0}</center><br><br>".format(
                  "</center><br><br><center>".join([movie for movie in added_movies]))}
        mylib.email.send([mylib.variables_sensitive.EMAIL_LOGIN, mylib.variables_sensitive.EMAIL_BACKUP],
                         "HELIOS - {0}".format(email_title),
                         "",
                         mylib.templates.Email("new_movies_in_cinema").report(**zm),
                         [])

# ----------------------------------------------------------------------------------------------------------------------
