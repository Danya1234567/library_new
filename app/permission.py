from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsSameBranchOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        employee = getattr(request.user, 'employee_profile', None)
        if not employee or not employee.library:
            return False

        library_field = getattr(view, 'library_field', 'library')
        obj_library = obj
        for part in library_field.split('__'):
            obj_library = getattr(obj_library, part)

        return obj_library == employee.library


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class CanIssueBooks(BasePermission):
    """
    - Суперюзер НЕ оформляет аренду/покупку книг вообще — это не его роль,
      этим занимается персонал (Librarians/Controllers) или читатель сам
      себе. Обычно Django даёт суперюзеру все permissions автоматически
      (has_perm всегда True) — здесь это намеренно переопределено явной
      проверкой is_superuser в начале.
    - Читатель (is_staff=False) оформляет аренду сам себе — Django-permission
      тут ни при чём, у читателя их в принципе нет и не должно быть.
    - Сотрудник (is_staff=True) действует по группе: Cleaners — ничего,
      Librarians — только add, Controllers — add/change/delete.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return False
        if request.method == 'POST':
            if not user.is_staff:
                return True
            return user.has_perm('app.add_borrowabooks')
        if request.method in ('PUT', 'PATCH'):
            if not user.is_staff:
                return False
            return user.has_perm('app.change_borrowabooks')
        if request.method == 'DELETE':
            return user.has_perm('app.delete_borrowabooks')
        return True