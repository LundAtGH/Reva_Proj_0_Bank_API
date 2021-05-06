from models.bank_acct import BankAcct


# Temporary code for functionality w/o database.

class TempDB:
    bank_accts = {
        1: BankAcct(1,  13, "savings",    1.00, 2001),
        2: BankAcct(2, 100, "savings",  123.45, 1776),
        3: BankAcct(3, 666, "checking",   3.14, 1900)
    }
