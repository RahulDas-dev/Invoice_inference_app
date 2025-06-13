from pydantic import BaseModel, Field, PositiveInt


class Item(BaseModel):
    """
    Structured model for summarizing item details in the invoice.
    """

    slno: PositiveInt
    description: str = Field(default="Not Available", description="Description of the item")
    quantity: str = Field(default="Not Available", description="Quantity of the item")
    price: str = Field(default="Not Available", description="Price of the item")
    currency: str = Field(default="INR", description="Currency of the price")


class CompanyDetails(BaseModel):
    """
    Structured model for summarizing company details.
    """

    name: str = Field(default="Not Available", description="Name of the company")
    gst_no: str = Field(default="Not Available", description="GST No of the company")
    pan_no: str = Field(default="Not Available", description="PAN No of the company")
    address: str = Field(default="Not Available", description="Address of the company")
    phone_number: str = Field(default="Not Available", description="Phone number of the company")
    email: str = Field(default="Not Available", description="Email of the company")


class TaxComponents(BaseModel):
    """
    Structured model for summarizing tax components.
    """

    CGST: float = Field(default=0.0, description="Central Goods and Services Tax")
    SGST: float = Field(default=0.0, description="State Goods and Services Tax")
    IGST: float = Field(default=0.0, description="Integrated Goods and Services Tax")


class Invoice(BaseModel):
    """
    Structured model for summarizing invoice details.
    """

    invoice_number: str = Field(description="Invoice number")
    invoice_date: str = Field(default="Not Available", description="Invoice date")
    seller_details: CompanyDetails = Field(
        default_factory=lambda: CompanyDetails(), description="Details of the seller Comapny"
    )
    buyer_details: CompanyDetails = Field(
        default_factory=lambda: CompanyDetails(), description="Details of the buyer Company"
    )
    items: list[Item] = Field(default_factory=list, description="List of items in the invoice")
    total_tax: TaxComponents = Field(default_factory=lambda: TaxComponents(), description="Total tax components")
    total_charge: float = Field(default=0.0, description="Total charges")
    total_discount: float = Field(default=0.0, description="Total discount applied")
    total_amount: float = Field(default=0.0, description="Total amount of the invoice")
    amount_paid: float = Field(default=0.0, description="Amount paid")
    amount_due: float = Field(default=0.0, description="Amount due")
    page_no: int = Field(default=0, description="Page no , Where the Information Available")


class InvoiceData(BaseModel):
    """Structured model for summarizing invoice details from List of pages."""

    details: list[Invoice] = Field(description="Deatils of invoice present per page", default_factory=list)
