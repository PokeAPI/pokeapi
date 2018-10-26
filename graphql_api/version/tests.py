from pokemon_v2.tests import APIData as A
from ..graphql_test import GraphQLTest


class VersionTests(GraphQLTest):
    def setUp(self):
        self.versions = []
        for n in range(4):
            version_group = A.setup_version_group_data(name=f"ver grp for ver {n}")
            self.versions.append(
                A.setup_version_data(name=f"base ver {n}", version_group=version_group)
            )
        for v in self.versions:
            A.setup_version_name_data(v, name=f"{v.name} name")

    def test_versions(self):
        executed = self.execute_query(
            """
            query {
                versions {
                    name
                    names {
                        text
                        language {name}
                    }
                    versionGroup {name}
                }
            }
            """
        )
        expected = {
            "data": {
                "versions": [
                    {
                        "name": v.name,
                        "names": [
                            {"text": n.name, "language": {"name": n.language.name}}
                            for n in v.versionname.all()
                        ],
                        "versionGroup": {"name": v.version_group.name},
                    }
                    for v in self.versions
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_version(self):
        v = self.versions[1]
        executed = self.execute_query(
            """
            query {
                version(name: "%s") {
                    name
                    names {
                        text
                        language {name}
                    }
                }
            }
            """
            % v.name
        )
        expected = {
            "data": {
                "version": {
                    "name": v.name,
                    "names": [
                        {"text": n.name, "language": {"name": n.language.name}}
                        for n in v.versionname.all()
                    ],
                }
            }
        }
        self.assertEqual(executed, expected)
