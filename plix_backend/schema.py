import graphene

from graphql_auth.schema import UserQuery, MeQuery


# QUERY SECTION
class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


# class Mutation(graphene.ObjectType):
#     pass


SCHEMA = graphene.Schema(query=Query)

"""
===========================================================================
    PLIXA SCHEMA
===========================================================================
"""
