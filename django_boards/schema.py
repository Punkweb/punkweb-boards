import graphene
import apps.api.schema


class Query(apps.api.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
