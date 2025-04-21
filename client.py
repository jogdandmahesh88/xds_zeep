import requests
import os
import datetime

#below code is to find the Document
soap_request = """<?xml version='1.0' encoding='UTF-8'?>
<soapenv:Envelope
	xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
	xmlns:wsa="http://www.w3.org/2005/08/addressing"
	xmlns:query="urn:oasis:names:tc:ebxml-regrep:xsd:query:3.0"
	xmlns:rim="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0"
	xmlns:rs="urn:oasis:names:tc:ebxml-regrep:xsd:rs:3.0">
	<soapenv:Header>
		<wsa:To soapenv:mustUnderstand="true">http://localhost:8084/xdstools7.12.0/sim/default__registry01/reg/sq</wsa:To>
		<wsa:MessageID soapenv:mustUnderstand="true">urn:uuid:175709BC017996C4D31741859309458</wsa:MessageID>
		<wsa:Action soapenv:mustUnderstand="true">urn:ihe:iti:2007:RegistryStoredQuery</wsa:Action>
	</soapenv:Header>
	<soapenv:Body>
		<query:AdhocQueryRequest>
			<query:ResponseOption returnComposedObjects="true" returnType="LeafClass"/>
			<rim:AdhocQuery id="urn:uuid:14d4debf-8f97-4251-9a74-a90016b0af0d">
				<rim:Slot name="$XDSDocumentEntryPatientId">
                <rim:ValueList>
                    <rim:Value>'P0307123951.2^^^&amp;1.3.6.1.4.1.21367.13.20.1000&amp;ISO'</rim:Value>
                </rim:ValueList>
            </rim:Slot>

            <rim:Slot name="$XDSDocumentEntryType">
                <rim:ValueList>
                    <rim:Value>('urn:uuid:7edca82f-054d-47f2-a032-9b2a5b5186c1')</rim:Value>
                </rim:ValueList>
            </rim:Slot>

            <rim:Slot name="$XDSDocumentEntryStatus">
                <rim:ValueList>
                    <rim:Value>('urn:oasis:names:tc:ebxml-regrep:StatusType:Approved')</rim:Value>
                    <rim:Value>('urn:oasis:names:tc:ebxml-regrep:StatusType:Deprecated')</rim:Value>
                </rim:ValueList>
            </rim:Slot>

			</rim:AdhocQuery>
		</query:AdhocQueryRequest>
	</soapenv:Body>
</soapenv:Envelope>
"""

headers = {
    "Content-Type": "application/soap+xml; charset=utf-8"
}

url = "http://localhost:8084/xdstools7.12.0/sim/default__registry01/reg/sq"

response = requests.post(url, data=soap_request, headers=headers)

print("Response Code:", response.status_code)
print("Response Body:\n", response.text)

# below code is to find the Document get Document

soap_request = """<soapenv:Envelope
    xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
    xmlns:wsa="http://www.w3.org/2005/08/addressing"
    xmlns:query="urn:oasis:names:tc:ebxml-regrep:xsd:query:3.0"
    xmlns:rim="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0">
    
    <soapenv:Header>
        <wsa:To soapenv:mustUnderstand="true">http://localhost:8084/xdstools7.12.0/sim/default__registry01/reg/sq</wsa:To>
        <wsa:MessageID soapenv:mustUnderstand="true">urn:uuid:175709BC017996C4D31741868160897</wsa:MessageID>
        <wsa:Action soapenv:mustUnderstand="true">urn:ihe:iti:2007:RegistryStoredQuery</wsa:Action>
    </soapenv:Header>

    <soapenv:Body>
        <query:AdhocQueryRequest>
            <query:ResponseOption returnComposedObjects="true" returnType="LeafClass"/>
            
            <rim:AdhocQuery id="urn:uuid:5c4f972b-d56b-40ac-a5fc-c8ca9b40b9d4">
                
                <rim:Slot name="$MetadataLevel">
                    <rim:ValueList>
                        <rim:Value>1</rim:Value>
                    </rim:ValueList>
                </rim:Slot>

                <rim:Slot name="$XDSDocumentEntryEntryUUID">
                    <rim:ValueList>
                        <rim:Value>('urn:uuid:cb4d61b2-04b4-4e48-b1bd-d1e545f9d366')</rim:Value>
                    </rim:ValueList>
                </rim:Slot>

            </rim:AdhocQuery>
        </query:AdhocQueryRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

headers = {
    "Content-Type": "application/soap+xml; charset=utf-8"
}

url = "http://localhost:8084/xdstools7.12.0/sim/default__registry01/reg/sq"

response = requests.post(url, data=soap_request, headers=headers)

print("Response Code:", response.status_code)
print("Response Body:\n", response.text)

#below code is to retrive the Document
import requests

# Define the SOAP XML body
soap_request = """<?xml version='1.0' encoding='UTF-8'?>
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
        <wsa:To soapenv:mustUnderstand="true">http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/ret</wsa:To>
        <wsa:MessageID soapenv:mustUnderstand="true">urn:uuid:175709BC017996C4D31741869359321</wsa:MessageID>
        <wsa:Action soapenv:mustUnderstand="true">urn:ihe:iti:2007:RetrieveDocumentSet</wsa:Action>
    </soapenv:Header>
    <soapenv:Body>
        <RetrieveDocumentSetRequest xmlns="urn:ihe:iti:xds-b:2007">
            <DocumentRequest>
                <RepositoryUniqueId>1.1.4567332.1.2</RepositoryUniqueId>
                <DocumentUniqueId>1.2.42.20250307123950.32</DocumentUniqueId>
            </DocumentRequest>
        </RetrieveDocumentSetRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

# Define the multipart headers
headers = {
    "Content-Type": "multipart/related; "
    "type=\"application/xop+xml\";"
    " boundary=MIMEBoundary1234567890; "
    "start=\"<rootpart@soapui.org>\"; "
    "start-info=\"application/soap+xml\""
}

# Define the multipart request body
multipart_body = f"""--MIMEBoundary1234567890
Content-Type: application/xop+xml; charset=UTF-8; type="application/soap+xml"
Content-Transfer-Encoding: 8bit
Content-ID: <rootpart@soapui.org>

{soap_request}
--MIMEBoundary1234567890--
"""

# Define the URL
url = "http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/ret"

# Send the request
response = requests.post(url, data=multipart_body, headers=headers)
print("==============", type(response))

# Prepare log directory and file
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

# Save logs
with open(log_file, "w", encoding="utf-8") as log:
    log.write("==== SOAP Request ====\n")
    log.write(f"URL: {url}\n")
    log.write(f"Headers: {headers}\n")
    log.write(f"Request Body:\n{soap_request}\n\n")
    
    log.write("==== Response ====\n")
    log.write(f"Response Code: {response.status_code}\n")
    log.write(f"Response Headers: {response.headers}\n")
    log.write(f"Response Body:\n{response.text}\n")

print(f"Response logs saved to: {log_file}")
print("Response Code:", response.status_code)
print("Response Body:\n", response.text)



# import os
# import datetime
# import requests
# import re
# import base64
# from email import policy
# from email.parser import BytesParser

# # Define the SOAP XML body
# soap_request = """<?xml version='1.0' encoding='UTF-8'?>
# <soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
#     <soapenv:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
#         <wsa:To soapenv:mustUnderstand="true">http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/ret</wsa:To>
#         <wsa:MessageID soapenv:mustUnderstand="true">urn:uuid:175709BC017996C4D31741869359321</wsa:MessageID>
#         <wsa:Action soapenv:mustUnderstand="true">urn:ihe:iti:2007:RetrieveDocumentSet</wsa:Action>
#     </soapenv:Header>
#     <soapenv:Body>
#         <RetrieveDocumentSetRequest xmlns="urn:ihe:iti:xds-b:2007">
#             <DocumentRequest>
#                 <RepositoryUniqueId>1.1.4567332.1.2</RepositoryUniqueId>
#                 <DocumentUniqueId>1.2.42.20250307123950.32</DocumentUniqueId>
#             </DocumentRequest>
#         </RetrieveDocumentSetRequest>
#     </soapenv:Body>
# </soapenv:Envelope>
# """

# # Define headers
# headers = {
#     "Content-Type": "multipart/related; type=\"application/xop+xml\"; boundary=MIMEBoundary1234567890; start=\"<rootpart@soapui.org>\"; start-info=\"application/soap+xml\""
# }

# # Define the multipart request body
# multipart_body = f"""--MIMEBoundary1234567890
# Content-Type: application/xop+xml; charset=UTF-8; type="application/soap+xml"
# Content-Transfer-Encoding: 8bit
# Content-ID: <rootpart@soapui.org>

# {soap_request}
# --MIMEBoundary1234567890--"""

# # Define the URL
# url = "http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/ret"

# # Send the request
# response = requests.post(url, data=multipart_body, headers=headers)

# # Prepare log directory and file
# log_dir = "logs"
# os.makedirs(log_dir, exist_ok=True)
# timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# log_file = os.path.join(log_dir, f"log_{timestamp}.txt")

# # Save logs
# with open(log_file, "w", encoding="utf-8") as log:
#     log.write("==== SOAP Request ====\n")
#     log.write(f"URL: {url}\n")
#     log.write(f"Headers: {headers}\n")
#     log.write(f"Request Body:\n{soap_request}\n\n")
    
#     log.write("==== Response ====\n")
#     log.write(f"Response Code: {response.status_code}\n")
#     log.write(f"Response Headers: {response.headers}\n")
#     log.write(f"Response Body:\n{response.text}\n")

# print(f"Response logs saved to: {log_file}")

# # Extract and save the PDF document
# pdf_dir = "retrieved_documents"
# os.makedirs(pdf_dir, exist_ok=True)
# pdf_file = os.path.join(pdf_dir, f"retrieved_document_{timestamp}.pdf")

# # Parse the multipart response to extract the PDF content
# if "multipart/related" in response.headers.get("Content-Type", ""):
#     msg = BytesParser(policy=policy.default).parsebytes(response.content)
#     for part in msg.iter_parts():
#         if part.get_content_type() == "application/pdf":
#             pdf_content = part.get_payload(decode=True)
#             if pdf_content:
#                 with open(pdf_file, "wb") as pdf:
#                     pdf.write(pdf_content)
#                 print(f"PDF document saved to: {pdf_file}")
#                 break
# else:
#     print("No valid PDF document found in the response.")

