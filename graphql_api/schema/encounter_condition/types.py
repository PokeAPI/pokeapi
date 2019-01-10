import graphene as g
from graphql_api.utils import load, load_with_args
from .. import interfaces as i  # pylint: disable=unused-import
from .. import base


class EncounterCondition(g.ObjectType):
    """
    Conditions which affect what pokemon might appear in the wild, e.g., day or night.
    """

    pk = None
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: EncounterConditionName,
        description="The name of this resource listed in different languages.",
        resolver=load_with_args("encountercondition_names", using="pk"),
    )
    values = g.List(
        lambda: EncounterConditionValue,
        description="A list of possible values for this encounter condition.",
        resolver=load("encountercondition_values", using="pk"),
    )


class EncounterConditionValue(g.ObjectType):
    """
    Encounter condition values are the various states that an encounter condition can have, i.e., time of day can be either day or night.
    """

    encounter_condition_id = None
    condition = g.Field(
        EncounterCondition,
        description="The condition this encounter condition value pertains to.",
        resolver=load("encountercondition", using="encounter_condition_id"),
    )
    is_default = g.Boolean(
        description="Whether or not this is the default condition value."
    )
    name = g.ID(name="idName", description="The name of this resource.")
    names = base.TranslationList(
        lambda: EncounterConditionValueName,
        description="The name of this encounter condition value listed in different languages.",
        resolver=load_with_args("encounterconditionvalue_names", using="pk"),
    )


class EncounterConditionName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )


class EncounterConditionValueName(base.BaseTranslation, interfaces=[i.Translation]):
    name = g.String(
        name="text", description="The localized resource name in a specific language."
    )
