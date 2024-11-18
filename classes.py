""" Event would be created on a menu where the user enters the name and people. This information is stored
in the event class but there are transactions that can also be added after the event has been made.
Transactions would be created in a menu where the user enters the payer, the debtors, the total amount of the
transaction, the individual amounts owed by the debtors and a description of the transaction to identify it.
The account will have to hold information about the amounts owed to and by the user.
The ne  friend class will contain the amounts owed to and by friends that the user adds to the app. """

import pickle
import os


class Event:

    def __init__(self, name):
        self.name = name
        self.transactions = {}
        self.people = []
        self.num_transactions = 0
        self.num_people = 0
        self.is_complete = False

    def __str__(self):
        return f'Event name: {self.name}'

    def add_people(self, people):
        self.people.append(people)
        self.num_people = len(self.people)
        # this is basic but needs to be changed to make sure people areent duplicated, etc

    def add_transaction(self, transaction):
        self.transactions[transaction.name] = transaction
        self.num_transactions = len(self.transactions)

    def remove_transaction(self, transaction):
        del self.transactions[transaction.name]
        self.num_transactions = len(self.transactions)
    # need to look into adding iterator mechanics __iter__() and __next__()


class Transaction:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        #self.total_paid = 0
        self.payers = {}
        self.num_payers = 0
        self.debtors = {}
        self.num_debtors = 0

    def add_payer(self, payer, amount):
        self.payers[payer] = amount
        self.num_payers = len(self.payers)

    def remove_payer(self, payer):
        del self.payers[payer]
        self.num_payers = len(self.payers)

    def add_debtor(self, debtor, amount):
        self.debtors[debtor] = amount
        self.num_debtors = len(self.debtors)

    def remove_debtor(self, debtor):
        del self.debtors[debtor]
        self.num_debtors = len(self.debtors)

    def mark_as_paid(self):
        self.isPaid = True

    def __str__(self):
        return f"Transaction: {self.name}\nPayers: {self.payers}\nDebtors: {self.debtors}"

    # need to look into adding iterator mechanics __iter__() and __next__()


class Account:

    def __init__(self, username, password):
        self.username = username
        # In a real app it would not be stored like this
        self.password = password
        self.displayName = " "
        self.events = {}
        self.friends = {}
        self.num_events = 0
        self.num_friends = 0
        self.amt_owed_to_acc = 0
        self.amt_owed_by_acc = 0
        self.amt_owed_total = 0

    def set_display_name(self, name):
        self.displayName = name
        self.save()

    def add_friend(self, friend):
        self.friends[friend.name] = friend
        self.num_friends = len(self.friends)
        self.save()

    def remove_friend(self, name):
        del self.friends[name]
        self.num_friends = len(self.friends)
        self.save()

    def remove_event(self, name):
        del self.events[name]
        self.num_events = len(self.events)
        self.save()

    def add_event(self, event):
        self.events[event.name] = event
        self.num_events = len(self.events)
        self.save()

    def save(self):
        with open('account.pkl', 'wb') as accfile:
            pickle.dump(self, accfile)

    @staticmethod
    def load():
        with open('account.pkl', 'rb') as accfile:
            return pickle.load(accfile)

    def deleteAcc(self):
        os.remove('account.pkl')
        os.remove('account.txt')

    # need to look into adding iterator mechanics __iter__() and __next__()


class Friend:

    def __init__(self, name):
        self.name = name
        self.amount_owed_to_user = 0.0
        self.amount_owed_by_user = 0.0


