from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtain
from rest_framework.decorators import action
from rest_framework.response import Response

from example_project.rest.permissions import IsTargetUser
from example_project.rest.serializers import UserCreateSerializer, UserSerializer


class UserCreateView(views.APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.order_by("username")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsTargetUser)

    @action(detail=False, methods=['get'])
    def from_token(self, request, *args, **kwargs):
        token_string = request.query_params.get("token")
        if not token_string:
            return Response("Token query param required", status=400)

        token = get_object_or_404(Token, key=token_string)
        self.kwargs["pk"] = token.user_id
        user = self.get_object()
        return Response(self.get_serializer(user).data)


class ObtainAuthToken(OriginalObtain):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "id": user.id})


obtain_auth_token = ObtainAuthToken.as_view()
