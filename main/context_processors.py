def user_roles(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        is_editor_user = (
            user.groups.filter(name='Editor').exists()
            or user.has_perm('main.change_experience')
            or user.has_perm('main.change_project')
        )
        return {
            'is_editor': is_editor_user,
        }
    return {'is_editor': False}