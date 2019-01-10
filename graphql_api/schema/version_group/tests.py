from pokemon_v2.tests import APIData as A
from graphql_api.graphql_test import GraphQLTest


class VersionGroupTests(GraphQLTest):
    def setUp(self):

        self.version_groups = []
        for n in range(4):
            generation = A.setup_generation_data(name=f"gen for ver grp {n}")
            self.version_groups.append(
                A.setup_version_group_data(
                    name=f"base ver grp {n}", generation=generation
                )
            )

        for vg in self.version_groups:
            move_learn_method = A.setup_move_learn_method_data(
                name=f"mv lrn mthd for {vg.name}"
            )
            region = A.setup_region_data(name=f"rgn for {vg.name}")
            pokedex = A.setup_pokedex_data(name=f"pkdx for {vg.name}")

            A.setup_version_group_move_learn_method_data(
                version_group=vg, move_learn_method=move_learn_method
            )
            A.setup_version_data(name=f"ver for {vg.name}", version_group=vg)
            A.setup_version_group_region_data(version_group=vg, region=region)
            A.setup_pokedex_version_group_data(pokedex=pokedex, version_group=vg)

    def test_version_groups(self):
        executed = self.execute_query(
            """
            query {
                versionGroups{
                    generation {idName}
                    idName
                    order
                    versions {idName}
                }
            }
            """
        )
        expected = {
            "data": {
                "versionGroups": [
                    {
                        "generation": {"idName": vg.generation.name},
                        "idName": vg.name,
                        "order": vg.order,
                        "versions": [{"idName": v.name} for v in vg.version.all()],
                    }
                    for vg in self.version_groups
                ]
            }
        }
        self.assertEqual(executed, expected)

    def test_version_group(self):
        vg = self.version_groups[1]
        executed = self.execute_query(
            """
            query {
                versionGroup(idName: "%s") {
                    idName
                }
            }
            """
            % vg.name
        )
        expected = {"data": {"versionGroup": {"idName": vg.name}}}
        self.assertEqual(executed, expected)
