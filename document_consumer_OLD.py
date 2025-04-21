from flask import Flask, request, jsonify, send_file
import requests
import os
import datetime
from email import message_from_bytes
from io import BytesIO
import xml.etree.ElementTree as ET

app = Flask(__name__)

BASE_URL = "http://localhost:8084/xdstools7.12.0/sim/"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_response(endpoint, soap_request, response):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(LOG_DIR, f"log_{endpoint}_{timestamp}.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        log.write("==== SOAP Request ====\n")
        log.write(f"Request Body:\n{soap_request}\n\n")
        log.write("==== Response ====\n")
        log.write(f"Response Code: {response.status_code}\n")
        log.write(f"Response Body:\n{response.text}\n")
    return log_file

@app.route("/find_document", methods=["GET","POST"])
def find_document():
    data = request.json
    patient_id = data.get("XDSDocumentEntryPatientId")
    print("-------patient_id------", patient_id)
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
                            <rim:Value>{formatted_patient_id}</rim:Value>
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
    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}
    url = BASE_URL + "default__registry01/reg/sq"
    response = requests.post(url, data=soap_request, headers=headers)
    log_file = log_response("find_document", soap_request, response)
    return jsonify({"status": response.status_code, "response": response.text, "log": log_file})

@app.route("/get_document", methods=["GET","POST"])
def get_document():
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
</soapenv:Envelope>"""
    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}
    url = BASE_URL + "default__registry01/reg/sq"
    response = requests.post(url, data=soap_request, headers=headers)
    log_file = log_response("get_document", soap_request, response)
    return jsonify({"status": response.status_code, "response": response.text, "log": log_file})

@app.route('/retrieve_document', methods=['POST', 'GET'])
def retrieve_document():
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
                    <DocumentUniqueId>1.2.42.20250307123950.22</DocumentUniqueId>
                </DocumentRequest>
            </RetrieveDocumentSetRequest>
        </soapenv:Body>
    </soapenv:Envelope>
    """

    # Define the URL
    url = "http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/ret"

    # Define the multipart headers
    headers = {
        "Content-Type": "multipart/related; boundary=MIMEBoundary1234567890; type=\"application/xop+xml\"; start=\"<rootpart@soapui.org>\"; start-info=\"application/soap+xml\""
    }

    # Define the multipart request body with correct formatting
    multipart_body = (
        "--MIMEBoundary1234567890\r\n"
        "Content-Type: application/xop+xml; charset=UTF-8; type=\"application/soap+xml\"\r\n"
        "Content-Transfer-Encoding: 8bit\r\n"
        "Content-ID: <rootpart@soapui.org>\r\n"
        "\r\n"
        f"{soap_request}\r\n"
        "--MIMEBoundary1234567890--\r\n"
    )

    # Send the request
    response = requests.post(url, data=multipart_body.encode('utf-8'), headers=headers)
    # Save the response content as a PDF file
    pdf_filename = "retrieved_document.pdf"
    with open(pdf_filename, "wb") as pdf_file:
        pdf_file.write(response.content)

    print(f"PDF saved successfully as '{pdf_filename}'")

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

    # Parse the multipart response
    content_type = response.headers.get("Content-Type")
    if content_type and "multipart/related" in content_type:
        # Parse the multipart response
        msg = message_from_bytes(response.content)
        if msg.is_multipart():
            for part in msg.get_payload():
                content_type = part.get_content_type()
                content_id = part.get("Content-ID", "").strip("<>")
                content_disposition = part.get("Content-Disposition", "")
                payload = part.get_payload(decode=True)

                if content_type == "application/xop+xml":
                    # This is the SOAP response part
                    soap_response = payload.decode("utf-8")
                    log.write("\n==== SOAP Response Part ====\n")
                    log.write(soap_response)
                elif content_type == "application/pdf":
                    # This is the PDF document part
                    pdf_file = os.path.join(log_dir, f"document_{content_id}.pdf")
                    with open(pdf_file, "wb") as f:
                        f.write(payload)
                    log.write(f"\n==== PDF Document Saved ====\n")
                    log.write(f"PDF saved to: {pdf_file}\n")

                    # Return the PDF file as a downloadable response
                    return send_file(pdf_file, as_attachment=True, download_name="document.pdf")

    # Return the response as JSON
    return jsonify({
        "response_code": response.status_code,
        "response_body": response.text,
        "log_file": log_file
    })


#Single endpoint to retrive the document.

BASE_URL = "http://localhost:8084/xdstools7.12.0/sim/"
HEADERS_SOAP = {"Content-Type": "application/soap+xml; charset=utf-8"}
HEADERS_MULTIPART = {
    "Content-Type": "multipart/related; boundary=MIMEBoundary1234567890; type=\"application/xop+xml\"; start=\"<rootpart@soapui.org>\"; start-info=\"application/soap+xml\""
}

SOAP_FIND_DOCUMENT = """<?xml version='1.0' encoding='UTF-8'?>
<soapenv:Envelope
    xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
    xmlns:wsa="http://www.w3.org/2005/08/addressing"
    xmlns:query="urn:oasis:names:tc:ebxml-regrep:xsd:query:3.0"
    xmlns:rim="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0">
    <soapenv:Header>
        <wsa:To soapenv:mustUnderstand="true">{url}</wsa:To>
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

SOAP_RETRIEVE_DOCUMENT = """<?xml version='1.0' encoding='UTF-8'?>
<soapenv:Envelope
    xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
    xmlns:wsa="http://www.w3.org/2005/08/addressing"
    xmlns:query="urn:ihe:iti:xds-b:2007">
    <soapenv:Header>
        <wsa:To soapenv:mustUnderstand="true">{url}</wsa:To>
        <wsa:MessageID soapenv:mustUnderstand="true">urn:uuid:175709BC017996C4D31741859309459</wsa:MessageID>
        <wsa:Action soapenv:mustUnderstand="true">urn:ihe:iti:2007:RetrieveDocumentSet</wsa:Action>
    </soapenv:Header>
    <soapenv:Body>
        <query:RetrieveDocumentSetRequest>
            <query:DocumentRequest>
                <query:RepositoryUniqueId>1.3.6.1.4.1.21367.2010.1.2.300</query:RepositoryUniqueId>
                <query:DocumentUniqueId>{document_id}</query:DocumentUniqueId>
            </query:DocumentRequest>
        </query:RetrieveDocumentSetRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

def send_soap_request(url, soap_body, headers):
    """Sends a SOAP request and returns the response."""
    try:
        response = requests.post(url, data=soap_body, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error: {e}"

def extract_document_id(xml_response):
    """Extracts the DocumentUniqueId from the SOAP response XML."""
    namespace = {
        'S': 'http://www.w3.org/2003/05/soap-envelope',
        'rim': 'urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0'
    }
    try:
        root = ET.fromstring(xml_response)
        identifier_xpath = ".//rim:ExternalIdentifier[@identificationScheme='urn:uuid:2e82c1f6-a085-4c72-9da3-8640a32e42ab']"
        external_identifier = root.find(identifier_xpath, namespace)

        if external_identifier is not None:
            return external_identifier.get("value")

    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")

    return None

def create_multipart_body(soap_request):
    """Formats SOAP request into a multipart request body."""
    return (
        "--MIMEBoundary1234567890\r\n"
        "Content-Type: application/xop+xml; charset=UTF-8; type=\"application/soap+xml\"\r\n"
        "Content-Transfer-Encoding: 8bit\r\n"
        "Content-ID: <rootpart@soapui.org>\r\n"
        "\r\n"
        f"{soap_request}\r\n"
        "--MIMEBoundary1234567890--\r\n"
    ).encode('utf-8')

def save_document(response_content, filename="retrieved_document_new.pdf"):
    """Saves the retrieved document content as a PDF."""
    with open(filename, "wb") as pdf_file:
        pdf_file.write(response_content)
    print(f"PDF saved successfully as '{filename}'")
    return filename

@app.route("/find_document_and_retrieve", methods=["GET", "POST"])
def find_document_and_retrieve():
    """Finds a document and retrieves it."""
    # Step 1: Find Document
    registry_url = BASE_URL + "default__registry01/reg/sq"
    find_document_request = SOAP_FIND_DOCUMENT.format(url=registry_url)

    find_response = send_soap_request(registry_url, find_document_request, HEADERS_SOAP)
    print("==================== First Response ====================")
    print(find_response)

    document_id = extract_document_id(find_response)
    if not document_id:
        return jsonify({"status": "error", "message": "Document ID not found"}), 400

    print(f"Document ID Found: {document_id}")

    # Step 2: Retrieve Document
    repository_url = BASE_URL + "default__repository01/rep/ret"
    retrieve_document_request = SOAP_RETRIEVE_DOCUMENT.format(url=repository_url, document_id=document_id)

    multipart_body = create_multipart_body(retrieve_document_request)
    retrieve_response = requests.post(repository_url, data=multipart_body, headers=HEADERS_MULTIPART)

    # Save retrieved document
    pdf_filename = save_document(retrieve_response.content)

    print("==================== Retrieve Document Response ====================")
    print(retrieve_response.text)

    return jsonify({
        "status": retrieve_response.status_code,
        "document_id": document_id,
        "pdf_file": pdf_filename
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
