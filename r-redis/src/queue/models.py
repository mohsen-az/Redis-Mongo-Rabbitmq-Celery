class User:

    def __init__(self, pk, username, phone_number):
        self.pk = pk
        self.username = username
        self.phone_number = phone_number


class Alert:

    def __init__(self, pk, user_id):
        self.pk = pk
        self.user_id = user_id


class Advertisement:

    def __init__(self, pk):
        self.pk = pk