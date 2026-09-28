def filter_by_branch(qs, user, library_field='library'):
    if not user.is_authenticated:
        return qs
    if user.is_superuser or not user.is_staff:
        return qs
    employee = getattr(user, 'employee_profile', None)
    if not employee or not employee.library:
        return qs.none()

    return qs.filter(**{library_field: employee.library})
