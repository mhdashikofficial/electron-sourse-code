import subprocess
import argparse
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", required=True, help="domain to be scanned")
parser.add_argument("-e", "--email", required=True, help="email address to send the report")
args = parser.parse_args()

# Run Nmap and save the output to a file
nmap_output_file = "nmap_output.txt"
subprocess.run(["nmap", args.domain, "-oN", nmap_output_file])

# Run Nikto and save the output to a file
nikto_output_file = "nikto_output.txt"
subprocess.run(["nikto", "-h", args.domain, "-o", nikto_output_file])

# Run Amass and save the output to a file
amass_output_file = "amass_output.txt"
subprocess.run(["amass", "enum", "-d", args.domain, "-o", amass_output_file])

# Run Subfinder and save the output to a file
subfinder_output_file = "subfinder_output.txt"
subprocess.run(["subfinder", "-d", args.domain, "-o", subfinder_output_file])

# Merge all the output files into one file
with open("merged_output.txt", "w") as outfile:
    outfile.write("Nmap Output:\n")
    with open(nmap_output_file) as infile:
        outfile.write(infile.read())
    outfile.write("\nNikto Output:\n")
    with open(nikto_output_file) as infile:
        outfile.write(infile.read())
    outfile.write("\nAmass Output:\n")
    with open(amass_output_file) as infile:
        outfile.write(infile.read())
    outfile.write("\nSubfinder Output:\n")
    with open(subfinder_output_file) as infile:
        outfile.write(infile.read())

# Convert the merged output file to PDF
os.system("cat merged_output.txt | a2ps -1 --medium=Letter -o - | ps2pdf - output.pdf")

# Load the SMTP details from the .env file
load_dotenv()
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")

# Send the PDF file via email
to_addr = args.email
msg = MIMEMultipart()
