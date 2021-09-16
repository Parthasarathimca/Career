'''
    Account config file
'''

class UserRole(object):
    '''
    Choices for user role: Admin, Franchise
    '''
    ADMIN = 1
    FRANCHISE = 2
    EMPLOYEE=3
    PRODUCTION_CENTER=4
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (FRANCHISE, 'Franchise'),
        (EMPLOYEE,'Employee'),
        (PRODUCTION_CENTER,'Production Center')
    )