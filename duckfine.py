class DuckFine:
    """Late fees for the QuackLoan rubber-duck lending library."""
    DAILY_FEE  = 0.50  # dollars per chargeable day
    GRACE_DAYS = 2     # the first two days late are forgiven
    MAX_FEE    = 5.00  # a single fine never exceeds this

    def __init__(self, member_id):
        self.member_id  = member_id
        self.total_owed = 0.0

 
