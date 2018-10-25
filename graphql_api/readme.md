# About this code

This explanation assumes a passing familiarity with GraphQL.

## `ObjectTypes` and resolvers

A key point to note is that Graphene does not require resolvers to return actual instances of the `ObjectType`. In keeping with Python's philosophy, Graphene accepts objects that only resemble the object type (or, duck-typing). This code-base takes advantage of this and directly returns the corresponding Django model instances from resolvers.

In the simplified example below, `pk` (primary key) and `region_id` are attributes from the `Location` model that the object type uses to resolve the `names` and `region` fields. Since they have not been assigned a Graphene type, they are [private fields](https://github.com/graphql-python/graphene/issues/554#issuecomment-344500839) and will not appear in queries.

```
class Location(graphene.ObjectType):
    pk = None
    names = g.List(LocationName)
    region_id = None
    region = Field(Region)

    def resolve_names(self, info):
        return models.LocationName.objects.filter(location_id=self.pk)

    def resolve_region(self, info):
        return models.Region.objects.get(pk=self.region_id)
```

In some cases, the model attribute names do not match the `ObjectType` field names; in these cases, a custom name can easily be set using the `name` argument to over-ride thefield name, as shown here:

```
class Language(g.ObjectType):
    official = g.Boolean(name="isOfficial")
    iso3166 = g.String(name="languageCode")
```

Note that Graphene automatically converts `snake_case` field names to `camelCase`, except when over-ridden with the `name` argument.

## Data Loader

## `where` and `orderBy` arguments

## Tests
