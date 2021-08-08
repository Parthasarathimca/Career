'''
    Account config file
'''

class UserRole(object):
    '''
    Choices for user role: Admin, Franchise
    '''
    ADMIN = 1
    FRANCHISE = 2

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (FRANCHISE, 'Franchise')
    )