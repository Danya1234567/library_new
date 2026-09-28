from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import EmployeeViewSet, RegisterView, LoginView, UserViewSet, GroupViewSet

router = DefaultRouter()
router.register('employees', EmployeeViewSet)
router.register('users',UserViewSet)
router.register('groups', GroupViewSet, basename='groups')
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
] + router.urls