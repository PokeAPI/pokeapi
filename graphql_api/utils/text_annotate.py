from django.db.models import OuterRef, Subquery
from graphql import GraphQLError


def text_annotate(query_set, lang, model, id_attr, text_resource, prefix):
    if not lang:
        raise GraphQLError(
            "Argument `lang` **must** be specified for sorts with text translations."
        )

    subquery = model.objects.filter(
        **{id_attr: OuterRef(id_attr if prefix else "pk")}, language__name=lang
    )
    field_name = prefix + "_" + text_resource + "_annotation"
    return (
        query_set.annotate(
            **{field_name: Subquery(subquery.values(text_resource)[:1])}
        ),
        field_name,
    )
