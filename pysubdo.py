import requests
from fpdf import FPDF

def find_subdomains(domain):
    # Query the Certificate Transparency logs on crt.sh for subdomains of the given domain
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    response = requests.get(url)
    subdomains = []
    if response.status_code == 200:
        # Parse the JSON response and extract the subdomains
        data = response.json()
        for entry in data:
            name_value = entry.get("name_value")
            if name_value.endswith(domain):
                subdomain = name_value[:-len(domain)-1]
                subdomains.append(subdomain)
    return subdomains

# Write the subdomains to a PDF file
def write_to_pdf(subdomains, domain):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Subdomains of {domain}:", ln=1, align="C")
    for subdomain in subdomains:
        pdf.cell(200, 10, txt=subdomain, ln=1, align="C")
    pdf.output(f"{domain}_subdomains.pdf")

# Write the subdomains to a text file
def write_to_text(subdomains, domain):
    with open(f"{domain}_subdomains.txt", "w") as f:
        for subdomain in subdomains:
            f.write(f"{subdomain}\n")

# Example usage
domain = input("Enter a domain name: ")
subdomains = find_subdomains(domain)
write_to_pdf(subdomains, domain)
write_to_text(subdomains, domain)
