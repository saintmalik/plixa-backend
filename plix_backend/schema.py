import graphene

from graphql_auth.schema import UserQuery, MeQuery


# QUERY SECTION
class Query(UserQuery, MeQuery, graphene.ObjectType):
    class Meta:
        exclude_fields = ("username",)


# class Mutation(graphene.ObjectType):
#     pass


SCHEMA = graphene.Schema(query=Query)

"""
===========================================================================
    PLIXA SCHEMA
===========================================================================
"""
