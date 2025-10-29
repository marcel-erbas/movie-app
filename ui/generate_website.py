from movie_storage import movie_storage_sql as storage


def serialize_movies():
    """Generate an HTML grid with all movies from the database."""
    output = ''
    for movie, info in storage.list_movies().items():
        title = movie
        year = info['year']
        poster = info['poster']

        output += f"""<li>
                <div class="movie">
                    <img class="movie-poster"
                         src="{poster}"/>
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">{year}</div>
                </div>
            </li>\n"""

    return output


def build_website():
    """Build the main index.templates page by replacing template placeholders with dynamic movie content from the database."""
    with open('./templates/index_template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    updated_html = template.replace('__TEMPLATE_TITLE__', 'Movie App')
    updated_html = updated_html.replace('__TEMPLATE_MOVIE_GRID__', serialize_movies())

    with open('./templates/index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)

    return True
