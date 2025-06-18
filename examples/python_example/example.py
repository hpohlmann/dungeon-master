# track_lore("payments.md")
# track_lore("api/payments.md")
"""
Example Python file with track_lore decorators.

This file demonstrates how to use track_lore decorators to associate
source files with documentation.
"""

def process_payment(amount, currency="USD"):
    """Process a payment with the given amount and currency."""
    # track_lore("payments-processing.md")
    print(f"Processing payment of {amount} {currency}")
    return {"status": "success", "amount": amount, "currency": currency}


class PaymentProcessor:
    """Main payment processing class."""
    
    def __init__(self):
        # track_lore("payment-processor-config.md")
        self.config = {"timeout": 30, "retries": 3}
    
    def validate_payment(self, payment_data):
        """Validate payment data before processing."""
        # This function doesn't have a decorator
        return True
