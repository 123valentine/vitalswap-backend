from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Vitalswap API",
    description="Endpoints providing fee structures for Customer and Business accounts.",
    version="1.0.0"
)

fees_data = {
    "Customer": {
        "US Virtual Bank Account": [
            {"Service": "Individual Account Issue", "Fee": "FREE", "Description": ""},
            {"Service": "ACH Deposit Fee", "Fee": "FREE", "Description": ""},
            {"Service": "Wire Deposit Fee", "Fee": "$15", "Description": ""},
            {"Service": "Fraud Reversal", "Fee": "$100", "Description": ""},
            {"Service": "3rd Party Requiring Extra Diligence", "Fee": "3%", "Description": ""}
        ],
        "NG Virtual Bank Account": [
            {"Service": "NGN Wallet Funding", "Fee": "₦200", "Description": ""},
            {"Service": "Fraud Reversal", "Fee": "₦1,000", "Description": ""},
            {"Service": "3rd Party Requiring Extra Diligence", "Fee": "3%", "Description": ""}
        ],
        "Payout": [
            {"Service": "NGN Payout - Instant", "Fee": "FREE", "Description": ""},
            {"Service": "USD Payout - 2-5 days", "Fee": "FREE", "Description": ""},
            {"Service": "USD Payout - 24hours", "Fee": "$10", "Description": ""}
        ],
        "Wallet to Wallet Transfer": [
            {"Service": "NGN Individual → Individual", "Fee": "FREE", "Description": ""},
            {"Service": "NGN Individual → Business", "Fee": "3%", "Description": ""}
        ],
        "Freedom Virtual Card": [
            {"Service": "Create Card", "Fee": "$1", "Description": ""},
            {"Service": "Fund Card", "Fee": "$0.50", "Description": ""},
            {"Service": "Transaction Fee", "Fee": "1.5% ($1 – $5)", "Description": ""},
            {"Service": "FX Fee (outside US)", "Fee": "1.5%", "Description": ""},
            {"Service": "Monthly Maintenance Fee", "Fee": "$1", "Description": ""},
            {"Service": "Defund Card", "Fee": "FREE", "Description": ""},
            {"Service": "Close Card", "Fee": "FREE", "Description": ""}
        ],
        "FX": [
            {"Service": "Create NGN Offer", "Fee": "FREE", "Description": ""},
            {"Service": "Buy NGN Offer", "Fee": "FREE", "Description": "We always put 10–15 points on all offers in the market"},
            {"Service": "Create USD Offer", "Fee": "FREE", "Description": ""},
            {"Service": "Buy USD Offer", "Fee": "FREE", "Description": "We always put 10–15 points on all offers in the market"}
        ]
    },
    "Business": {
        "US Virtual Bank Account": [
            {"Service": "Business Account Issue", "Fee": "FREE", "Description": ""},
            {"Service": "ACH Deposit Fee", "Fee": "FREE", "Description": ""},
            {"Service": "Wire Deposit Fee", "Fee": "$15", "Description": ""},
            {"Service": "Fraud Reversal", "Fee": "$100", "Description": ""},
            {"Service": "3rd Party Requiring Extra Diligence", "Fee": "3%", "Description": ""}
        ],
        "NG Virtual Bank Account": [
            {"Service": "NGN Wallet Funding", "Fee": "₦200", "Description": ""},
            {"Service": "Fraud Reversal", "Fee": "₦1,000", "Description": ""},
            {"Service": "3rd Party Requiring Extra Diligence", "Fee": "3%", "Description": ""}
        ],
        "Business Collections": [
            {"Service": "NGN Settlement", "Fee": "₦200", "Description": "Per transaction"},
            {"Service": "USD Settlement", "Fee": "2% ($1–$2)", "Description": "2% capped at $2, Min $1"}
        ],
        "Business Payout": [
            {"Service": "NGN Payout - Instant", "Fee": "FREE", "Description": ""},
            {"Service": "USD Payout - 2-5 days", "Fee": "FREE", "Description": ""},
            {"Service": "USD Payout - 24hours", "Fee": "$10", "Description": ""}
        ],
        "Wallet to Wallet Transfer": [
            {"Service": "NGN Individual → Business", "Fee": "2%", "Description": ""}
        ],
        "FX": [
            {"Service": "Create NGN Offer", "Fee": "FREE", "Description": ""},
            {"Service": "Buy NGN Offer", "Fee": "FREE", "Description": "We always put 10 points on all offers in the market"},
            {"Service": "Create USD Offer", "Fee": "FREE", "Description": ""},
            {"Service": "Buy USD Offer", "Fee": "FREE", "Description": "We always put 10 points on all offers in the market"}
        ]
    }
}

@app.get("/")
async def home():
    return {"message": "Vitalswap API is live! Visit /fees to view endpoints."}

@app.get("/fees")
async def get_all_fees():
    return JSONResponse(content=fees_data)

@app.get("/fees/customer")
async def get_customer_fees():
    return JSONResponse(content=fees_data["Customer"])

@app.get("/fees/business")
async def get_business_fees():
    return JSONResponse(content=fees_data["Business"])

@app.get("/fees/customer/{category}")
async def get_customer_category(category: str):
    data = fees_data["Customer"].get(category)
    if not data:
        return JSONResponse(content={"error": "Category not found"}, status_code=404)
    return JSONResponse(content={category: data})

@app.get("/fees/business/{category}")
async def get_business_category(category: str):
    data = fees_data["Business"].get(category)
    if not data:
        return JSONResponse(content={"error": "Category not found"}, status_code=404)
    return JSONResponse(content={category: data})