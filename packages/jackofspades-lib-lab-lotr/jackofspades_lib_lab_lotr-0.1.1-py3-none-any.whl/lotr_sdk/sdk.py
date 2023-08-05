from .mixins import ApiMixIn
from .Session import session


class Book(ApiMixIn):
    """represents a Lord of the Rings book"""

    def __init__(self, id: str, name: str):
        """
        :param id: books unique identifier
        :param name: the name of the book
        """
        self.id = id
        self.name = name

    @property
    def chapters(self):
        """query all chapters for the current book object"""
        url = f"{self.endpoint}/{self.id}/chapter"
        resp = session.get(url)
        return Chapter.serialize(resp.json()["docs"])


class Movie(ApiMixIn):
    """represents a Lord of the Rings movie"""

    def __init__(
        self,
        id: str,
        name: str,
        run_time: int,
        budget: int,
        revenue: int,
        nominations: int,
        nomination_wins: int,
        score: int,
    ):
        """
        :param id: movies unique identifier
        :param name: name of movie
        :param run_time: the movies run_time in minutes
        :param budget: the movies budget in millions
        :param nominations: the number of nominations the movie was considered for
        :param nomination_wins: the number of nominations the movie won
        :param score: Rotten Tomatoes critic rating
        """
        self.id = id
        self.name = name
        self.run_time = run_time
        self.budget = budget
        self.revenue = revenue
        self.nominations = nominations
        self.nomination_wins = nomination_wins
        self.score = score

    @property
    def quotes(self):
        """returns all quotes for a given movie"""
        url = f"{self.endpoint}/{self.id}/quote"
        resp = session.get(url)
        return Quote.serialize(resp.json()["docs"])


class Character(ApiMixIn):
    """represents a character from Lord of the Rings"""

    def __init__(
        self,
        id: str,
        height: str,
        race: str,
        gender: str,
        birth: str,
        spouse: str,
        death: str,
        realm: str,
        hair: str,
        name: str,
        wiki_url: str,
    ):
        """
        :param id: characters unique identifier
        :param height: the characters height, either an exact height or a word describing their height
        :param race: the characters race IE: Hobbit/Dwarf
        :param gender: the characters gender
        :param birth: the characters birthday
        :param spouse: the name of the characters spouse
        :param death: prompt describing when the character has died
        :param realm: which realm the character is from
        :param hair: hair color for the character
        :param name: the characters name
        :param wiki_url: the wiki page url for the character
        """
        self.id = id
        self.height = height
        self.race = race
        self.gender = gender
        self.birth = birth
        self.spouse = spouse
        self.death = death
        self.realm = realm
        self.hair = hair
        self.name = name
        self.wiki_url = wiki_url

    @property
    def quotes(self):
        """
        returns all quotes spoken by a given character
        """
        # TODO: testme
        url = f"{self.endpoint}/{self.id}/quote"
        resp = session.get(url)
        return Quote.serialize(resp.json()["docs"])


class Quote(ApiMixIn):
    """represents a quote from a Lord of the rings character/movie"""

    def __init__(
        self, _id: str, dialog: str, movie_id: str, character_id: str, id: str
    ):
        """
        :param _id: quotes unique identifier
        :param dialog: the contents of the quote
        :param movie_id: identifier for the movie the quote is from
        :param character_id: identifier for which character says the quote
        :param id: redundant quote identifier
        """
        self._id = _id
        self.dialog = dialog
        self._movie_id = movie_id
        self._character_id = character_id
        self.id = id
        self.name = dialog  # Kind of redundant. Might be preferable to override the __repr__ method, but I see redundancy in the API with getting both `id` and `_id`

    @property
    def movie(self):
        '''gets the Movie object associated with this quote'''
        return Movie.get(self._movie_id)

    @property
    def character(self):
        '''get the Character object of the character who says the quote'''
        return Character.get(self._character_id)


class Chapter(ApiMixIn):
    """represents a chapter in a book"""

    def __init__(self, id: str, name: str, book_id: str):
        self.id = id
        self.name = name
        self._book_id = book_id

    @property
    def book(self):
        """
        retrieve the book that this chapter resides in
        """
        return Book.get(self._book_id)


if __name__ == "__main__":
    # Very simple test
    books = Book.get()
    print(books[0])
    print(books[0].chapters)
    print()

    movies = Movie.get()
    print(movies[5])
    print(movies[5].quotes)
    print()

    characters = Character.get()
    print(characters[0])
    print(characters[0].quotes)
    print()

    quotes = Quote.get()
    print(quotes[0])
    print()

    chapters = Chapter.get()
    print(chapters[0])
    print()
