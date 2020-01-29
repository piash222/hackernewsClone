import graphene
from graphene_django import DjangoObjectType
from .models import Link


# each object type
class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


# define a mutation class. Right after, you define the output of the
# mutation, the data the server can send back to the client
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    # Defines the data you can send to the server
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # It creates a link in the database using the data send by the uesr through url and
    # description parameters. After the server returns the Createlink class
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description
        )


# creates a mutation class with a field to be resolved, which points to our mutation
# defined before
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
