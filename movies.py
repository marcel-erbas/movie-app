import statistics
import sys
import random
import matplotlib.pyplot as plt
from thefuzz import fuzz
import movie_storage_sql as storage
import omdb_api
import generate_website


def print_menu():
    """Displays the main menu options for the movie database application."""
    print("\nMenu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Generate Website")
    print("10. Create rating histogram")
    print()


def exit_app():
    """Terminates the application."""
    print("Bye!")
    sys.exit(0)


def list_movies():
    """Displays all movies in the database."""
    print(f"\n{len(storage.list_movies())} movies in database:")
    for movie, info in storage.list_movies().items():
        print(f"{movie} ({info['year']}): {info['rating']}")


def add_movie():
    """Adds a new movie to the database."""
    movie = input("\nEnter new movie name: ")
    if not movie:
        print("Movie name is empty")
        return
    if movie in storage.list_movies():
        print(f"Movie '{movie}' already exists!")
        return

    try:
        movie, year, rating, poster = omdb_api.fetch_movie(movie)
    except ValueError as e:
        print(f"Error {e}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    storage.add_movie(movie, year, rating, poster)
    print(f"Movie '{movie}' added successfully!")


def delete_movie():
    """Deletes a movie by name."""
    movie = input("\nEnter movie name to delete: ")
    if not movie:
        print("Movie name is empty")
        return
    if movie in storage.list_movies():
        storage.delete_movie(movie)
        print(f"Movie '{movie}' deleted successfully!")
    else:
        print(f"Movie '{movie}' not found!")


def update_movie():
    """Updates the rating of an existing movie."""
    movie = input("\nEnter movie name to update: ")
    if not movie:
        print("Movie name is empty")
        return
    if movie not in storage.list_movies():
        print(f"Movie '{movie}' not found!")
        return

    try:
        rating = float(input("Enter new rating (0-10): "))
        if not 0 <= rating <= 10:
            print("Invalid rating! Must be between 0 and 10.")
            return
    except ValueError:
        print("Invalid input!")
        return

    storage.update_movie(movie, rating)
    print(f"Movie '{movie}' successfully updated!")


def get_stats():
    """Calculates and displays average, median, best, and worst ratings."""
    ratings = [info["rating"] for info in storage.list_movies().values()]
    avg_rating = round(sum(ratings) / len(ratings), 1)
    median_rating = round(statistics.median(ratings), 1)

    print(f"\nAverage rating: {avg_rating}")
    print(f"Median rating: {median_rating}")

    max_rating = max(ratings)
    min_rating = min(ratings)

    print("\nBest movie(s):")
    for movie, info in storage.list_movies().items():
        if info["rating"] == max_rating:
            print(f"{movie}, {info['rating']}")

    print("\nWorst movie(s):")
    for movie, info in storage.list_movies().items():
        if info["rating"] == min_rating:
            print(f"{movie}, {info['rating']}")


def get_random_movie():
    """Selects and displays a random movie."""
    movie = random.choice(list(storage.list_movies().keys()))
    info = storage.list_movies()[movie]
    print(f"\nYour movie for tonight: {movie} ({info['year']}), rating {info['rating']}")


def search_movie():
    """Searches for movies by name with fuzzy matching."""
    search_query = input("\nEnter part of movie name: ").strip().lower()
    if not search_query:
        print("Movie name is empty")
        return
    print()

    found_movies = [movie for movie in storage.list_movies() if search_query in movie.lower()]
    if found_movies:
        for movie in found_movies:
            info = storage.list_movies()[movie]
            print(f"{movie} ({info['year']}): {info['rating']}")
        return

    similar = []
    for movie in storage.list_movies():
        similarity = fuzz.ratio(search_query, movie.lower())
        if similarity > 50:
            similar.append((movie, similarity))

    if similar:
        print("Did you mean:")
        for movie, sim in sorted(similar, key=lambda x: x[1], reverse=True):
            print(f"- {movie} ({storage.list_movies()[movie]['rating']}) [{sim:.0f}%]")
    else:
        print(f"No results for '{search_query}'.")


def list_movies_sorted_by_rating():
    """Displays all movies sorted by rating."""
    sorted_movies = sorted(storage.list_movies().items(), key=lambda x: x[1]["rating"], reverse=True)
    print(f"\n{len(sorted_movies)} movies in database (sorted by rating):")
    for movie, info in sorted_movies:
        print(f"{movie}: {info['rating']}")


def create_website():
    if generate_website.build_website():
        print("Website was generated successfully.")


def create_rating_histogram():
    """Creates and shows a histogram of ratings."""
    ratings = [info["rating"] for info in storage.list_movies().values()]
    filename = input("Enter filename to save histogram (e.g., histogram.png): ")

    plt.hist(ratings, bins=20, range=(0, 10), edgecolor='black')
    plt.title("Movie Ratings Histogram")
    plt.xlabel("Rating")
    plt.ylabel("Number of Movies")
    plt.savefig(filename)
    plt.show()


def main():
    """
    Main entry point of the movie database application.

    Displays a menu of available actions and continuously prompts the user
    to choose an option (0–9). Based on the user’s input, the corresponding
    function is executed. The loop runs until the user selects '0' to exit.
    """
    print("*" * 10 + " My Movies Database " + "*" * 10)

    func_dict = {
        "0": exit_app,
        "1": list_movies,
        "2": add_movie,
        "3": delete_movie,
        "4": update_movie,
        "5": get_stats,
        "6": get_random_movie,
        "7": search_movie,
        "8": list_movies_sorted_by_rating,
        "9": create_website,
        "10": create_rating_histogram
    }

    while True:
        print_menu()
        user_choice = input("Enter choice (0-9): ")

        func = func_dict.get(user_choice)
        if func:
            func()
        else:
            print("Invalid choice!")

        input("\nPress enter to continue")


if __name__ == "__main__":
    main()
