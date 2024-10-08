ROLE_CHOICES = [
        ('admin', 'Admin'),           # Full access to all features
        ('manager', 'Manager'),       # Can manage users and devices, but limited admin features
        ('user', 'User'),             # Regular user with basic control over personal devices
        ('guest', 'Guest'),           # Guest user with limited access (view-only)
    ]