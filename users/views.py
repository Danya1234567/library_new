from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from app.pagination import Pagination
from users.models import Employee, User
from users.serializer.employee import (
    EmployeeWriteSerializer, EmployeeStaffSerializer, EmployeeClientSerializer, EmployeeUpdateSerializer,
)
from users.serializer.login import LoginSerializer
from users.serializer.register import RegisterSerializer
from users.serializer.user import UserSerializer


# Create your views here.

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'phone_number': user.phone_number,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'groups': list(user.groups.values_list('name', flat=True)),
                'permissions': list(user.get_all_permissions()),
            },
        })

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='codename')
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.prefetch_related('permissions').order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.select_related('user', 'position', 'library').prefetch_related('shift')
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeWriteSerializer
        # Правка существующего сотрудника не требует логина и пароля,
        # поэтомуотдельный сериализатор — иначе смены не поменять.
        if self.request.method in ('PUT', 'PATCH'):
            return EmployeeUpdateSerializer
        if self.request.user.is_staff:
            return EmployeeStaffSerializer
        return EmployeeClientSerializer

    def get_permissions(self):
        if self.request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return [IsAdminUser()]
        return [IsAuthenticated()]

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            qs = User.objects.all().order_by('username')
            search = self.request.query_params.get('search')
            if search:
                from django.db.models import Q
                qs = qs.filter(
                    Q(username__icontains=search) |
                    Q(name__icontains=search) |
                    Q(surname__icontains=search) |
                    Q(phone_number__icontains=search)
                )
            return qs
        return User.objects.filter(pk=self.request.user.pk)