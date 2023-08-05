from .conf import BASE_URL
from .Session import session
from typing import Union, Any


class ApiMixIn:
    """An API MixIn for better mantainability"""

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    @property
    def endpoint(self):
        return f"{BASE_URL}/{self.__class__.__name__.lower()}"

    @classmethod
    def serialize(cls, json) -> Union[list[Any], Any]:
        """
        serializes a response into the appropriate object
        return a list of objects if multiple objects are present in the response
        """
        retval = []
        for item in json:
            try:
                item = cls(*item.values())
            except Exception:
                # NOTE: There's a weird edgecase where one or more characters don't have wikiUrl as a key value..
                # README: Also, towards the tail-end of development, I realized not everything is in a predictable order, which is surprising, since JSON preserves order..
                # This also means, that sometimes you'll get values in the wrong place with this implementation.
                item = cls(*item.values(), "")
            retval.append(item)

        return retval[0] if len(retval) == 1 else retval

    @classmethod
    def get(cls, id=None, limit=100, page=1, offset=0):
        """
        retrieves data from the API & returns the serialized result of the query

        :param id (str): the unique identifier to query
        :param limit (int): the maximum number of results to query
        :param page (int): which page to return results from
        :param offset (int): offset of the start of the query results by this amount
        """
        url = f"{BASE_URL}/{cls.__name__.lower()}"
        url = f"{url}/{id}" if id else url
        url = f"{url}?limit={limit}"
        url = f"{url}&page={page}"
        url = f"{url}&offset={offset}"
        resp = session.get(url)
        return cls.serialize(resp.json()["docs"])
