import streamlit as st
from PIL import Image
import requests
from requests.auth import HTTPBasicAuth
from io import BytesIO
import json

st.set_page_config(layout="wide", page_title="")

# API authentication
auth = HTTPBasicAuth('admin', '1234@BCD')

# Function to fetch documents from API
def fetch_documents(url):
    documents = []
    while url:
        response = requests.get(url, auth=auth)
        data = response.json()
        documents.extend(data['results'])
        url = data['next']
    return documents

# Fetch documents
api_url = "http://edms-demo.epik.live/api/v4/documents/"
documents = fetch_documents(api_url)

# Create a placeholder for the uploaded image
uploaded_image = None

# Create the two-column layout
col1, col2 = st.columns([4, 6])

# Extract document labels and image URLs
document_labels = [doc['label'] for doc in documents]
image_urls = {doc['label']: doc['file_latest']['pages_first']['image_url'] for doc in documents}

# Subcategory options
subcategory_options = {
    "Expenses": [
        
        "Food and Groceries", "Healthcare", "Insurance", "Marketing and Advertising", 
        "Meals and Entertainment", "Mortgage", "Office Supplies & Expenses", "Other expenses", 
        "Professional Services", "Rent", "Salaries and Wages", "Subscriptions", "Taxes", 
        "Tools & Hardware", "Training and Education", "Transportation and Travel", "Utilities", 
        "Vehicles and Gas","Other"
    ],
    "Income": [
        
        "Affiliate Marketing", "Business Sales", "Freelance Income", "Gifts and Donations", 
        "Investments", "Online Sales", "Other income", "Rental Income", "Royalties", 
        "Salary or Wages", "Other"
    ],
    "Bank statements": [
        
        "Annual Reports", "Balance Sheets", "Bank statements", "Business Licenses", 
        "Cash Flow Statements", "Contracts", "Employee Contracts", "Income Statements", 
        "Inventory Lists", "Lease Agreements", "Meeting Minutes", "Other documents", 
        "Purchase Orders", "Tax Statements", "Other"
    ],
    "Documents": [
       
        "Annual Reports", "Balance Sheets", "Bank statements", "Business Licenses", 
        "Cash Flow Statements", "Contracts", "Employee Contracts", "Income Statements", 
        "Inventory Lists", "Lease Agreements", "Meeting Minutes", "Other documents", 
        "Purchase Orders", "Tax Statements", "Other"
    ]
}

# Subcategory options
currency_options = [
    "SGD - Singapore dollar",
    "AFN - Afghan afghani",
    "ALL - Albanian lek",
    "DZD - Algerian dinar",
    "AOA - Angolan kwanza",
    "ARS - Argentine peso",
    "AMD - Armenian dram",
    "AWG - Aruban florin",
    "AUD - Australian dollar",
    "AZN - Azerbaijani manat",
    "BSD - Bahamian dollar",
    "BHD - Bahraini dinar",
    "BDT - Bangladeshi taka",
    "BBD - Barbadian dollar",
    "BYN - Belarusian ruble",
    "BZD - Belize dollar",
    "BMD - Bermudian dollar",
    "BTN - Bhutanese ngultrum",
    "BOB - Bolivian boliviano",
    "BAM - Bosnia and Herzegovina convertible mark",
    "BWP - Botswana pula",
    "BRL - Brazilian real",
    "BND - Brunei dollar",
    "BGN - Bulgarian lev",
    "MMK - Burmese kyat",
    "BIF - Burundian franc",
    "XPF - CFP franc",
    "KHR - Cambodian riel",
    "CAD - Canadian dollar",
    "CVE - Cape Verdean escudo",
    "KYD - Cayman Islands dollar",
    "XAF - Central African CFA franc",
    "CLP - Chilean peso",
    "COP - Colombian peso",
    "KMF - Comorian franc",
    "CDF - Congolese franc",
    "CRC - Costa Rican colón",
    "HRK - Croatian kuna",
    "CUC - Cuban convertible peso",
    "CUP - Cuban peso",
    "CZK - Czech koruna",
    "DKK - Danish krone",
    "DJF - Djiboutian franc",
    "DOP - Dominican peso",
    "XCD - Eastern Caribbean dollar",
    "EGP - Egyptian pound",
    "ERN - Eritrean nakfa",
    "ETB - Ethiopian birr",
    "EUR - Euro",
    "FKP - Falkland Islands pound",
    "FJD - Fijian dollar",
    "GMD - Gambian dalasi",
    "GEL - Georgian lari",
    "GHS - Ghanaian cedi",
    "GIP - Gibraltar pound",
    "XAU - Gold (troy ounce)",
    "GTQ - Guatemalan quetzal",
    "GGP - Guernsey pound",
    "GNF - Guinean franc",
    "GYD - Guyanese dollar",
    "HTG - Haitian gourde",
    "HNL - Honduran lempira",
    "HKD - Hong Kong dollar",
    "HUF - Hungarian forint",
    "ISK - Icelandic króna",
    "INR - Indian rupee",
    "IDR - Indonesian rupiah",
    "IRR - Iranian rial",
    "IQD - Iraqi dinar",
    "ILS - Israeli new shekel",
    "JMD - Jamaican dollar",
    "JPY - Japanese yen",
    "JEP - Jersey pound",
    "JOD - Jordanian dinar",
    "KZT - Kazakhstani tenge",
    "KES - Kenyan shilling",
    "KWD - Kuwaiti dinar",
    "KGS - Kyrgyzstani som",
    "LAK - Lao kip",
    "LBP - Lebanese pound",
    "LSL - Lesotho loti",
    "LRD - Liberian dollar",
    "LYD - Libyan dinar",
    "MOP - Macanese pataca",
    "MKD - Macedonian denar",
    "MGA - Malagasy ariary",
    "MWK - Malawian kwacha",
    "MYR - Malaysian ringgit",
    "MVR - Maldivian rufiyaa",
    "IMP - Manx pound",
    "MRU - Mauritanian ouguiya",
    "MUR - Mauritian rupee",
    "MXN - Mexican peso",
    "MDL - Moldovan leu",
    "MNT - Mongolian tögrög",
    "MAD - Moroccan dirham",
    "MZN - Mozambican metical",
    "NAD - Namibian dollar",
    "NPR - Nepalese rupee",
    "ANG - Netherlands Antillean guilder",
    "TWD - New Taiwan dollar",
    "NZD - New Zealand dollar",
    "NIO - Nicaraguan córdoba",
    "NGN - Nigerian naira",
    "NOK - Norwegian krone",
    "OMR - Omani rial",
    "PKR - Pakistani rupee",
    "PAB - Panamanian balboa",
    "PGK - Papua New Guinean kina",
    "PYG - Paraguayan guaraní",
    "PEN - Peruvian sol",
    "PHP - Philippine peso",
    "PLN - Polish złoty",
    "GBP - Pound sterling",
    "QAR - Qatari riyal",
    "CNY - Renminbi",
    "RON - Romanian leu",
    "RUB - Russian ruble",
    "RWF - Rwandan franc",
    "SHP - Saint Helena pound",
    "SVC - Salvadoran colón",
    "WST - Samoan tālā",
    "SAR - Saudi riyal",
    "RSD - Serbian dinar",
    "SCR - Seychellois rupee",
    "SLL - Sierra Leonean leone",
    "XAG - Silver (troy ounce)",
    "SBD - Solomon Islands dollar",
    "SOS - Somali shilling",
    "ZAR - South African rand",
    "KRW - South Korean won",
    "SSP - South Sudanese pound",
    "XDR - Special drawing rights",
    "LKR - Sri Lankan rupee",
    "SDG - Sudanese pound",
    "SRD - Surinamese dollar",
    "SZL - Swazi lilangeni",
    "SEK - Swedish krona",
    "CHF - Swiss franc",
    "SYP - Syrian pound",
    "STN - São Tomé and Príncipe dobra",
    "TJS - Tajikistani somoni",
    "TZS - Tanzanian shilling",
    "USDT - Tether",
    "THB - Thai baht",
    "TOP - Tongan paʻanga",
    "TTD - Trinidad and Tobago dollar",
    "TND - Tunisian dinar",
    "TRY - Turkish lira",
    "TMT - Turkmenistan manat",
    "USDC - USD Coin",
    "UGX - Ugandan shilling",
    "UAH - Ukrainian hryvnia",
    "AED - United Arab Emirates dirham",
    "USD - United States dollar",
    "UYU - Uruguayan peso",
    "UZS - Uzbekistani soʻm",
    "VUV - Vanuatu vatu",
    "VES - Venezuelan bolívar",
    "VND - Vietnamese đồng",
    "XOF - West African CFA franc",
    "YER - Yemeni rial",
    "ZMW - Zambian kwacha",
    "ZWL - Zimbabwean dollar"
]
default_currency_index = currency_options.index("SGD - Singapore dollar")

# Initialize or load stored data
def load_stored_data():
    if 'payment_info' not in st.session_state:
        st.session_state['payment_info'] = {}

load_stored_data()

# Create the form in the left column
with col1:
    document_label = st.selectbox("Select Document", options=document_labels)
    merchant = st.text_input(label="Merchant", value="")
    date = st.date_input(label="Date", format="DD/MM/YYYY")
    document_category = st.selectbox(
        label="Document Category",
        options=["Expenses", "Income", "Bank statements", "Documents"]
    )
    subcategory = st.selectbox(label="Subcategory", options=subcategory_options[document_category])

    # Show text input for other subcategory if 'Other' is selected
    if subcategory == "Other":
        new_subcategory = st.text_input(label="Please specify other subcategory")
        subcategory = new_subcategory if new_subcategory else subcategory
    
    # Payment method selection outside the form
    payment_method = col1.selectbox("Payment Method", ["Cash", "PayNow", "Credit Card", "On Credit"], index=0)
    
    # Display additional field based on payment method selection outside the form
    account_number = ""
    if payment_method in ["PayNow", "Credit Card"]:
        field_label = f"{payment_method} Account Number"
        default_value = st.session_state['payment_info'].get(payment_method, '')
        account_number = col1.text_input(label=field_label, value=default_value)
    department = st.selectbox("Customer or Department", ["Harry Kek", "Nam Nguyen", "HR", "Accounting"], index=0)
    reference = st.text_input(label="Reference", value="")
    tax_calculation = st.radio(label="Tax Calculation", options=["Tax Included", "Tax Excluded"])
    total_amount = st.number_input(label="Total Amount", value=0.00)
    tax_amount = st.number_input(label="Tax amount", value=0.00)
    # Calculate tax percentage
    
    # Display tax percentage
    
    currency = st.selectbox(label="Currency", options=currency_options, index=default_currency_index)
    detail = st.text_input(label="Detail", value="")
    document_tag = st.text_input(label="Document tags", value="")
    
    if st.button("Done and Submit", type="primary"):
        # Collect all form data
        form_data = {
            "Merchant": merchant,
            "Date": date.strftime('%Y-%m-%d'),
            "Document Category": document_category,
            "Subcategory": subcategory,
            "Payment Method": payment_method,
            "Account Number": account_number,
            "Reference": reference,
            "Tax Calculation": tax_calculation,
            "Total Amount": total_amount,
            "Tax Amount": tax_amount,
            "Currency": currency,
            "Detail": detail,
            "Document Tags": document_tag,
            "Document Label": document_label,
            "Image URL": image_urls[document_label] if document_label in image_urls else None
        }
        
        # Write JSON data to a file
        with open('expense_report.json', 'w') as json_file:
            json.dump(form_data, json_file, indent=4)

        # Provide download button for JSON file
        with open('expense_report.json', 'r') as json_file:
            json_data = json_file.read()
        st.download_button("Download JSON", json_data, "expense_report.json", "application/json")
        
        st.success("Expense report submitted successfully!")

# Create the image upload section in the right column
with col2:
    image_file = st.file_uploader("Upload Invoice or Receipt", type=["jpg", "jpeg", "png"])

    if image_file is not None:
        uploaded_image = Image.open(image_file)
        st.image(uploaded_image, use_column_width="always")
    else:
        # Show document image if a document is selected from dropdown
        if document_label in image_urls:
            image_url = image_urls[document_label]
            response = requests.get(image_url, auth=auth)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                st.image(img, use_column_width="always")
            else:
                st.error("Unable to load image from URL.")
