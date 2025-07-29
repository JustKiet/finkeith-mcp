from finkeith.core.common.banks import SupportedBank
from datetime import datetime
from typing import Optional

class Transaction:
    def __init__(
        self,
        id: str,
        transaction_date: datetime,
        account_number: str,
        bank_name: SupportedBank,
        sub_account: Optional[str] = None,
        amount_in: float = 0.0,
        amount_out: float = 0.0,
        accumulated: float = 0.0,
        code: Optional[str] = None,
        transaction_content: Optional[str] = None,
        reference_number: Optional[str] = None,
    ) -> None:
        self._id = id
        self._transaction_date = transaction_date
        self._account_number = account_number
        self._bank_name = bank_name
        self._sub_account = sub_account
        self._amount_in = amount_in
        self._amount_out = amount_out
        self._accumulated = accumulated
        self._code = code
        self._transaction_content = transaction_content
        self._reference_number = reference_number

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def transaction_date(self) -> datetime:
        return self._transaction_date
    
    @property
    def account_number(self) -> str:    
        return self._account_number
    
    @property
    def bank_name(self) -> SupportedBank:
        return self._bank_name
    
    @property
    def sub_account(self) -> Optional[str]:
        return self._sub_account
    
    @property
    def amount_in(self) -> float:
        return self._amount_in
    
    @property
    def amount_out(self) -> float:
        return self._amount_out
    
    @property
    def accumulated(self) -> float:
        return self._accumulated
    
    @property
    def code(self) -> Optional[str]:
        return self._code
    
    @property
    def transaction_content(self) -> Optional[str]:
        return self._transaction_content
    
    @property
    def reference_number(self) -> Optional[str]:
        return self._reference_number

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.id}, "
            f"transaction_date={self.transaction_date}, "
            f"account_number={self.account_number}, "
            f"bank_name={self.bank_name}, "
            f"sub_account={self.sub_account}, "
            f"amount_in={self.amount_in}, "
            f"amount_out={self.amount_out}, "
            f"accumulated={self.accumulated}, "
            f"code={self.code}, "
            f"transaction_content={self.transaction_content}, "
            f"reference_number={self.reference_number})"
        )