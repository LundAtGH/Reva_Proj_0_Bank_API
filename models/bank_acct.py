class BankAcct:

    def __init__(self, bank_acct_id=0, holder_id=0, type="", funds=0, creation_date=0):
        self.bank_acct_id = bank_acct_id
        self.holder_id = holder_id
        self.type = type
        self.funds = funds
        self.creation_date = creation_date

    def json(self):
        return {
            'bankAcctId':   self.bank_acct_id,
            'holderId':     self.holder_id,
            'type':         self.type,
            'funds':        self.funds,
            'creationDate': self.creation_date
        }

    @staticmethod
    def json_parse(json):
        bank_acct = BankAcct()
        bank_acct.bank_acct_id = json["bankAcctId"] if "bankAcctId" in json else 0
        bank_acct.holder_id = json["holderId"]
        bank_acct.type = json["type"]
        bank_acct.funds = json["funds"]
        bank_acct.creation_date = json["creationDate"]
        return bank_acct

    def __repr__(self):
        return str(self.json())
