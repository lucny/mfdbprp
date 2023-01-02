import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Film, Genre
from django.contrib.auth.models import User
import graphql_jwt
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class FilmType(DjangoObjectType):
    class Meta:
        model = Film
        fields = ('id', 'title', 'plot', 'release_date', 'rate', 'runtime', 'poster', 'genres')


class Query(graphene.ObjectType):
    all_genres = graphene.List(GenreType)
    get_genre = graphene.Field(GenreType, id=graphene.Int())
    all_films = graphene.List(FilmType)
    get_film = graphene.Field(FilmType, id=graphene.Int())
    pokus = graphene.String()
    get_user = graphene.Field(UserType, token=graphene.String(required=True))

    @login_required
    def resolve_get_user(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
             raise Exception("Authentication credentials were not provided")
        return info.context.user

    def resolve_all_genres(root, info):
        return Genre.objects.all()

    def resolve_get_genre(root, info, id):
        return Genre.objects.get(pk=id)

    def resolve_all_films(root, info):
        return Film.objects.all()

    def resolve_get_film(root, info, id):
        return Film.objects.get(pk=id)

    def resolve_pokus(root, info):
        return f'To je můj pokus'


class CreateGenre(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    genre = graphene.Field(GenreType)

    @classmethod
    def mutate(cls, root, info, name):
        genre = Genre(name=name)
        ok = True
        genre.save()
        return CreateGenre(genre=genre, ok=ok)


class UpdateGenre(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    genre = graphene.Field(GenreType)

    @classmethod
    def mutate(cls, root, info, name, id):
        genre = Genre.objects.get(id=id)
        genre.name = name
        ok = True
        genre.save()
        return UpdateGenre(genre=genre, ok=ok)


class DeleteGenre(graphene.Mutation):

    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()
    genre = graphene.Field(GenreType)

    @classmethod
    def mutate(cls, root, info, id):
        genre = Genre.objects.get(id=id)
        ok = True
        genre.delete()
        return DeleteGenre(genre=genre, ok=ok)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    # Long running refresh tokens
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()

    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
