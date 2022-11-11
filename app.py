import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from streamlit.components.v1 import iframe

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/compiled/certificate_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()


################################################################################
# Award Certificate
################################################################################

accounts = w3.eth.accounts
account = accounts[0]

# new code start here
# st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")

st.title("🎓 Cruzy Diploma Generator")


# leftside, rightside = st.columns(2)
# with leftside:
with st.form("left-side"):

    left, middle, right = st.columns(3)

    with left:
        st.subheader("Award")
        # with st.form(key="form1"):
        # form=left.form("form_left")
        # st.write("Here's the template we'll be using:")
        # form.image("template.png", width=300)
        student_account = st.selectbox("Select Account", options=accounts)
        certificate_details = st.text_input("The URI to the artwork", value="https://s3.amazonaws.com/sebales.com/penguin.jpg")
        award_button=st.form_submit_button("Award Certificate")
    
    with middle:
        st.subheader("Display")
        # with st.form("form2"):
        # form=middle.form("form_middle")
        certificate_id = st.number_input("Enter a Certificate Token ID to display", value=0, step=1)
        display_button=st.form_submit_button("Display Certificate")

    with right:
        env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
        template = env.get_template("templates.html")
        st.subheader("Export")
        # form=right.form("form_right")
        student = st.text_input("Student name")
        course = st.selectbox(
            "Choose course",
            ["FintechBootcamp"],
            index=0,
        )
        grade = st.slider("Grade", 0, 100, 100)
        # uri = st.text_input("Place URI Here")
        export_button=st.form_submit_button("Export Certificate")

if award_button:
    st.write(f"The certificate was awarded to {student_account}")
    tx_hash=contract.functions.awardCertificate(student_account, certificate_details).transact({'from': account, 'gas': 1000000})
    st.image(certificate_details) 
    # certificate_id =contract.functions.awardCertificate.call()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    temp_dictionary=dict(receipt)
    # st.write(temp_dictionary['logs'][0]['topics'])
    st.write(temp_dictionary)
    # st.write(f"The certificate was awarded to {certificate_id}")
    total_token_supply = contract.functions.totalSupply().call()
    token_id = st.selectbox("Artwork Tokens", list(range(total_token_supply)))
if display_button:
    # Get the certificate owner
    certificate_owner = contract.functions.ownerOf(certificate_id).call()
    st.write(f"The certificate was awarded to {certificate_owner}")
    # Get the certificate's metadata
    certificate_uri =str(contract.functions.tokenURI(certificate_id).call() )
    st.write(f"The certificate's tokenURI metadata is {certificate_uri}")
    # st.image(certificate_uri) 
if export_button:
    html = template.render(
        student=student,
        course=course,
        uri=certificate_details,
        grade=f"{grade}/100",
        date=date.today().strftime("%B %d, %Y"),
    )
    pdf = pdfkit.from_string(html, False)
    st.balloons()
    ## Download certificate
    st.success("🎉 Your diploma was generated!")
    # far_right.write(html, unsafe_allow_html=True)
    st.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name="diploma.pdf",
        mime="application/octet-stream",
    ) 
    

# with middle:
#     st.subheader("Display")
#     # with st.form("form2"):
#     form=middle.form("form_middle")
#     certificate_id = form.number_input("Enter a Certificate Token ID to display", value=0, step=1)
#     display_button=form.form_submit_button("Display Certificate")
#     if display_button:
#         # Get the certificate owner
#         certificate_owner = contract.functions.ownerOf(certificate_id).call()
#         form.write(f"The certificate was awarded to {certificate_owner}")
#         # Get the certificate's metadata
#         certificate_uri =str(contract.functions.tokenURI(certificate_id).call() )
#         form.write(f"The certificate's tokenURI metadata is {certificate_uri}")
#         # form.image(certificate_uri) 
# with right:
#     env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
#     template = env.get_template("templates.html")
#     st.subheader("Export")
#     form=right.form("form_right")
#     student = form.text_input("Student name")
#     course = form.selectbox(
#         "Choose course",
#         ["FintechBootcamp"],
#         index=0,
#     )
#     grade = form.slider("Grade", 0, 100, 100)
#     uri = form.text_input("Place URI Here")
#     export_button=form.form_submit_button("Export Certificate")
#     if export_button:
#         html = template.render(
#             student=student,
#             course=course,
#             uri=uri,
#             grade=f"{grade}/100",
#             date=date.today().strftime("%B %d, %Y"),
#         )
#         pdf = pdfkit.from_string(html, False)
#         form.balloons()
#         ## Download certificate
#         far_right.success("🎉 Your diploma was generated!")
#         # far_right.write(html, unsafe_allow_html=True)
#         far_right.download_button(
#             "⬇️ Download PDF",
#             data=pdf,
#             file_name="diploma.pdf",
#             mime="application/octet-stream",
#         )



                  


# #right side code
# right.write("Fill in the data:")
# form_right = right.form("template_form")
# student = form_right.text_input("Student name")
# course = form_right.selectbox(
#     "Choose course",
#     # ["Report Generation in Streamlit", "Advanced Cryptography"],
#     ["FintechBootcamp"],
#     index=0,
# )
# grade = form_right.slider("Grade", 1, 100, 100)
# uri = form_right.text_input("Place URI Here")



# submit = form_right.form_submit_button("Generate PDF")
# if submit:
    
#     html = template.render(
#         student=student,
#         course=course,
#         uri=uri,
#         grade=f"{grade}/100",
#         date=date.today().strftime("%B %d, %Y"),
        
#     )

#     pdf = pdfkit.from_string(html, False)
#     st.balloons()

#     right.success("🎉 Your diploma was generated!")
#     # st.write(html, unsafe_allow_html=True)
#     # st.write("")
#     right.download_button(
#         "⬇️ Download PDF",
#         data=pdf,
#         file_name="diploma.pdf",
#         mime="application/octet-stream",
#     )