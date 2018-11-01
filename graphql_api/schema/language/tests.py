from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class LanguageTests(GraphQLTest):
    def setUp(self):
        self.languages = [
            A.setup_language_data(name=f"base lang {n}") for n in range(4)
        ]
        self.language_names = [
            A.setup_language_name_data(
                language, local_language=language, name=f"{language.name} name"
            )
            for language in self.languages
        ]

    def test_languages(self):
        executed = self.execute_query(
            """
            query {
                languages {
                    name
                    isOfficial
                    languageCode
                    names {
                        text
                        language {name}
                    }
                }
            }
            """
        )
        expected = {
            "data": {
                "languages": [
                    {
                        "name": l.name,
                        "isOfficial": l.official,
                        "languageCode": l.iso3166,
                        "names": [
                            {
                                "text": self.language_names[i].name,
                                "language": {
                                    "name": self.language_names[i].local_language.name
                                },
                            }
                        ],
                    }
                    for i, l in enumerate(self.languages)
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_language(self):
        l = self.languages[1]
        l_nm = self.language_names[1]
        executed = self.execute_query(
            """
            query {
                language(name: "%s") {
                    name
                    isOfficial
                    languageCode
                    names {
                        text
                        language {name}
                    }
                }
            }
            """
            % l.name
        )
        expected = {
            "data": {
                "language": {
                    "name": l.name,
                    "isOfficial": l.official,
                    "languageCode": l.iso3166,
                    "names": [
                        {
                            "text": l_nm.name,
                            "language": {"name": l_nm.local_language.name},
                        }
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
