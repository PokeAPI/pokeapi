import re
import logging
from django.db import connection

LOGGER = logging.getLogger(__name__)


class QueryCountDebugMiddleware:
    """
    Log the number of queries run and the total time taken for each request (with a status code of 200). It does not currently support multi-database setups.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 200:
            total_time = 0

            for query in connection.queries:
                query_time = query.get("time")
                if query_time is None:
                    # django-debug-toolbar monkeypatches the connection
                    # cursor wrapper and adds extra information in each
                    # item in connection.queries. The query time is stored
                    # under the key "duration" rather than "time" and is
                    # in milliseconds, not seconds.
                    query_time = query.get("duration", 0) / 1000
                total_time += float(query_time)

            LOGGER.debug("===================================================================")
            LOGGER.debug(
                "%i queries in %.3f seconds", len(connection.queries), total_time
            )

        return response


class QueryDebugMiddleware:
    """
    Log each query that is run for requests with a status code of 200.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 200:
            LOGGER.debug(
                "==================================================================="
            )

            for counter, query in enumerate(connection.queries):

                sql = re.split(
                    r"(SELECT|FROM|WHERE|GROUP BY|ORDER BY|INNER JOIN|LIMIT|ON|LEFT OUTER JOIN)",
                    query["sql"],
                )
                if not sql[0]:
                    sql = sql[1:]

                # Join every other line
                string = ""
                for i, line in enumerate(sql):
                    if i % 2:
                        string += "%s\n" % line
                    else:
                        string += line

                # Remove quotation marks
                string = string.replace('"', "")

                # Put each select clause on its own line
                regex = re.compile("(, )(?=.*\n*FROM)")
                string = regex.sub(",\n       ", string)

                # Put each AND clause on its own line
                regex = re.compile(" AND ")
                string = regex.sub(" \n  AND ", string)

                # Indent every other line
                # sql = [
                #     (" " if i % 2 else "") + x
                #     for i, x in enumerate(sql)
                # ]

                if counter != 0:
                    LOGGER.debug(
                        "-------------------------------------------------------------------"
                    )

                LOGGER.debug(
                    "%i (%.3f seconds)\n\n%s", counter + 1, float(query["time"]), string
                )
        return response
