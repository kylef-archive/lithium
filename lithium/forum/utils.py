
def user_permission_level(user):
    user_perm = int(not user.is_anonymous()) + 1
    
    if user.is_staff:
        user_perm = 3
    
    if user.is_superuser:
        user_perm = 4
    
    return user_perm
