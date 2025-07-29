from finkeith.core.common.banks import SupportedBank

bank_mapping = {
    "MB Bank": SupportedBank.MBBANK,
    "MBBANK": SupportedBank.MBBANK,
    "Military Commercial Joint Stock Bank": SupportedBank.MBBANK,
    # Add more banks here as you support them
}

class BankMapping:
    @staticmethod
    def map_bank_name(sepay_bank_name: str) -> SupportedBank:
        """Map SePay bank name to domain SupportedBank enum."""
        map_res = bank_mapping.get(sepay_bank_name, None)

        if map_res is None:
            raise ValueError(f"Unsupported bank name: {sepay_bank_name}")
        
        return map_res