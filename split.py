"""
split.py

This file contains the algorithm for calculating splits
"""
import classes

def calculate_split(event, account):
    """
    Algorithm for reducing transactions to credits
    """

    credits = {}
    pos_credits = {}
    neg_credits = {}
    payments = {}

    # set default credits to 0
    credits[account.displayName.strip()] = 0.0
    for person in event.people:
        credits[person.name.strip()] = 0.0


    for transaction in event.transactions:
        transaction_total = 0.0
        transaction_obj = event.transactions[transaction]
        num_people = transaction_obj.num_payers + transaction_obj.num_debtors
        
           
        transaction_total = sum(list(transaction_obj.payers.values()))
        payer_total = 0.0

        # negatively credit users that were paid for
        for debtor in transaction_obj.debtors:
            amt = float(transaction_obj.debtors[debtor.strip()])
            credits[debtor.strip()] -= amt
            payer_total += amt


        # determine how much the payer(s) paid for themselves to remove from credit
        payer_amt = payer_total / transaction_obj.num_payers

        for payer in transaction_obj.payers:
            #transaction_total += transaction_obj.payers[payer]
            #amt = transaction_obj.payers[payer]
            credits[payer.strip()] += payer_amt
        

        # split credits by positive and negative
        for person in credits:
            if credits[person.strip()] > 0.0:
                pos_credits[person.strip()] = credits[person.strip()]
            elif credits[person] < 0.0:
                neg_credits[person.strip()] = credits[person.strip()]


    # first check for equal debts and amounts needed for simple transactions
    for person in list(pos_credits.keys()):
        amt = pos_credits[person.strip()]
        if -amt in neg_credits.values():
            payment = {person.strip(): amt}
            debtor = list(neg_credits.keys())[list(neg_credits.values()).index(-amt)]
            payments[debtor.strip()] = payment
            del pos_credits[person.strip()]
            del neg_credits[debtor.strip()]

    # loop until all payments are solved (removed from each dict)
    while pos_credits and neg_credits:
        reduce_transactions(pos_credits, neg_credits, payments)
    
    return payments


            
def reduce_transactions(pos_credits, neg_credits, payments):
    """
    Algorithm for reducing the amount of transactions
    """

    for person in list(pos_credits.keys()):

        for debtor in list(neg_credits.keys()):
            debt_amt = neg_credits[debtor.strip()]
            if abs(debt_amt) <= pos_credits[person.strip()]:
                payment = {person.strip(): -debt_amt}
                if debtor not in payments:
                    payments[debtor.strip()] = payment
                else:
                    payments[debtor.strip()][person.strip()] = debt_amt
                pos_credits[person.strip()] += debt_amt
                del neg_credits[debtor.strip()]

                if pos_credits[person.strip()] == 0.0:
                    del pos_credits[person.strip()]
    
    

    # check if there is a debt greater than all the remaining values and split
    debtgreater = False
    for debtor in list(neg_credits.keys()):
        
        if abs(neg_credits[debtor.strip()]) > max(pos_credits.values()):
            debtgreater = True
    
    # split process
    if debtgreater:
        for debtor, value in sorted(neg_credits.items(), key=lambda item: item[1]):
            
            for person in list(pos_credits.keys()):
                
                if abs(neg_credits[debtor.strip()]) >= pos_credits[person.strip()]:
                    payment = {person.strip(): pos_credits[person.strip()]}
                    if debtor not in payments:
                        payments[debtor.strip()] = payment
                    else:
                        payments[debtor.strip()][person.strip()] = pos_credits[person.strip()]
                    neg_credits[debtor.strip()] += pos_credits[person.strip()]
                    del pos_credits[person.strip()]

                    if neg_credits[debtor.strip()] == 0.0:
                        del neg_credits[debtor.strip()]

        # return calculations    



"""
#Testing Variables
# vacation event
event = classes.Event("Vacation Weekend")

# user account
account = classes.Account("jchesson", "password")
account.set_display_name("Jeff")

# friends on event
friend1 = classes.Friend("James")
friend2 = classes.Friend("John")
friend3 = classes.Friend("Lexi")
friend4 = classes.Friend("Steven")
friend5 = classes.Friend("Hannah")
account.add_friend(friend1)
account.add_friend(friend2)
account.add_friend(friend3)
account.add_friend(friend4)
account.add_friend(friend5)
event.add_people(friend1)
event.add_people(friend2)
event.add_people(friend3)
event.add_people(friend4)
event.add_people(friend5)



# transactions on event

# Jeff paid $180, everyone who ate owes $60 (user as payer)
dinner = classes.Transaction('Dinner', "KBBQ with three friends")
dinner.add_payer("Jeff", 180)
dinner.add_debtor("John", 60)
dinner.add_debtor("Lexi", 60)
event.add_transaction(dinner)

# Steven paid $75, 2 paid $10, 1 paid $15, and 2 paid $20 (user as debtor)
breakfast = classes.Transaction('Breakfast', "IHOP with 5 people") 
breakfast.add_payer("Steven", 75)
breakfast.add_debtor("Jeff", 10)
breakfast.add_debtor("John", 10)
breakfast.add_debtor("Lexi", 15)
breakfast.add_debtor("Hannah", 20)
event.add_transaction(breakfast)

# Lexi paid $30 for her and hannah, (user not in transaction)
coffee = classes.Transaction('Coffee', "Quick starbucks trip for lexi and hannah and Jeff")
coffee.add_payer("Lexi", 30)
coffee.add_debtor("Jeff", 10)
coffee.add_debtor("Hannah", 10)
event.add_transaction(coffee)

#situations with 2 payers could be someone paying tip in cash while someone pays the bill with a card
#in this situation either the amount paid by the second payer would be deducted from the amount they owe to the first
#or the amount paid can all be attributed to the largest payer who then would pay back the second

#add event to account and pass through function
account.add_event(event)
calculate_split(event, account)
"""
