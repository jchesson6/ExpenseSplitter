""" Event would be created on a menu where the user enters the name and people. This information is stored
in the event class but there are transactions that can also be added after the event has been made.
Transactions would be created in a menu where the user enters the payer, the debtors, the total amount of the
transaction, the individual amounts owed by the debtors and a description of the transaction to identify it.
The account will have to hold information about the amounts owed to and by the user.
The new friend class will contain the amounts owed to and by friends that the user adds to the app. """


class Event:

    num_transactions = 0
    transactions = []
    people = []

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Event name: {self.name}'

    def add_people(self, people):
        self.people.append(people)
        # this is basic but needs to be changed to make sure people areent duplicated, etc

    def add_transaction(self, transaction):
        self.transactions.append(transaction)    

    # need to look into adding iterator mechanics __iter__() and __next__()


class Transaction:

    total = 0

    def __init__(self, description, payer, debtors):
        self.description = description
        self.payer = payer
        self.debtors = debtors

    def add_debtor(self, debtor):
        self.debtors.append(debtor)

    # need to look into adding iterator mechanics __iter__() and __next__()


class Account:

    num_friends = 0
    amt_owed_to_acc = 0
    amt_owed_by_acc = 0
    amt_owed_total = 0
    friends = []

    def __init__(self, name):
        self.name = name

    def add_friend(self, friend):
        self.friends.append(friend)

    # need to look into adding iterator mechanics __iter__() and __next__()


class Friend:
    
    amount_owed_to_user = 0
    amount_owed_by_user = 0

    def __init__(self, name):
        self.name = name


