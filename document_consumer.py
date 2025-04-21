from flask import Flask, request, jsonify, send_file,Response
import requests
import os
import datetime
from request_body import *
import io
from flask_cors import CORS
import html
from bs4 import BeautifulSoup
import base64

app = Flask(__name__)
CORS(app)
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

    request_body = request.json
    XDSDocumentEntryPatientId = request_body.get('XDSDocumentEntryPatientId')
    XDSDocumentEntryPatientId= html.escape(XDSDocumentEntryPatientId)
    print(XDSDocumentEntryPatientId)
    # XDSDocumentEntryType = request_body.get('XDSDocumentEntryType')
    # XDSDocumentEntryStatus1 = request_body.get('XDSDocumentEntryStatus1')
    # XDSDocumentEntryStatus2 = request_body.get('XDSDocumentEntryStatus2')

    soap_request = find_document_request.format(XDSDocumentEntryPatientId)
    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}
    url = BASE_URL + "default__registry01/reg/sq"
    response = requests.post(url, data=soap_request, headers=headers)
    soup = BeautifulSoup(response.text, "xml")

    # Extract Document IDs along with mimeType and corresponding DocA values
    documents = []
    for obj in soup.find_all("ExtrinsicObject"):
        doc_id = obj.get("id", "unknown")
        mime_type = obj.get("mimeType", "unknown")
        localized_string = obj.find("LocalizedString")
        doc_value = localized_string["value"] if localized_string else "unknown"
        
        documents.append({"id": doc_id, "mimeType": mime_type, "Title": doc_value})
    
    print("===================", response.text)
    return jsonify(
        {
            "status": response.status_code,
            "Documents": documents,
            # "response": response.text,
        }
    )

@app.route("/get_document", methods=["GET","POST"])
def get_document():
    request_body = request.json
    XDSDocumentEntryEntryUUID = request_body.get('XDSDocumentEntryEntryUUID')
    soap_request = get_document_request.format(XDSDocumentEntryEntryUUID)
    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}
    url = BASE_URL + "default__registry01/reg/sq"
    response = requests.post(url, data=soap_request, headers=headers)
    print(response.text)
    soup = BeautifulSoup(response.text, "xml")

    # Find the <ExternalIdentifier> element with the specific identificationScheme
    external_identifier = soup.find("ExternalIdentifier", {"identificationScheme": "urn:uuid:2e82c1f6-a085-4c72-9da3-8640a32e42ab"})
    if external_identifier and external_identifier.has_attr("value"):
        value = external_identifier["value"]
        print("Extracted Value:", value)
    else:
        value = None
        print("No value found for the specified identificationScheme.")
    # Extract RepositoryUniqueId
    repository_unique_id = None
    slot_element = soup.find("Slot", {"name": "repositoryUniqueId"})
    if slot_element:
        value_list = slot_element.find("ValueList")
        if value_list:
            value_element = value_list.find("Value")
            if value_element:
                repository_unique_id = value_element.text
                print("RepositoryUniqueId:", repository_unique_id)

    return jsonify({"status": response.status_code,"RepositoryUniqueId": repository_unique_id, "Document_uniqueId": value})


@app.route('/retrieve_document', methods=['POST'])
def retrieve_document():
    request_body = request.json
    # RepositoryUniqueId = request_body.get('RepositoryUniqueId')
    DocumentUniqueId = request_body.get('DocumentUniqueIds')[0]

    # Construct the SOAP request
    soap_request = retrieve_document_request.format(DocumentUniqueId)
    url = "http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/ret"

    headers = {
        "Content-Type": "multipart/related; type=\"application/xop+xml\"; boundary=MIMEBoundary1234567890; start=\"<rootpart@soapui.org>\"; start-info=\"application/soap+xml\""
    }

    multipart_body = (
        "--MIMEBoundary1234567890\r\n"
        "Content-Type: application/xop+xml; charset=UTF-8; type=\"application/soap+xml\"\r\n"
        "Content-Transfer-Encoding: 8bit\r\n"
        "Content-ID: <rootpart@soapui.org>\r\n"
        "\r\n"
        f"{soap_request}\r\n"
        "--MIMEBoundary1234567890--\r\n"
    )

    # Send the request to the XDS repository
    response = requests.post(url, data=multipart_body, headers=headers)

    if response.status_code == 200:
        # Extract the PDF part from the MIME response
        boundary = b"--MIMEBoundary112233445566778899"
        parts = response.content.split(boundary)
        for part in parts:
            if b"Content-Type: application/pdf" in part:
                # Extract the PDF content
                pdf_start = part.find(b"%PDF")
                pdf_content = part[pdf_start:]
                return Response(pdf_content, content_type="application/pdf")
        return jsonify({"error": "PDF not found in response"}), 500
    else:
        return jsonify({"error": response.text}), response.status_code



def log_response(action, url, headers, request_body, response):
    log_file = os.path.join(LOG_DIR, f"log_{action}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
    with open(log_file, "w", encoding="utf-8") as log:
        log.write(f"==== {action.upper()} REQUEST ====\n")
        log.write(f"URL: {url}\n")
        log.write(f"Headers: {headers}\n")
        log.write(f"Request Body:\n{request_body}\n")
        log.write("==== RESPONSE ====\n")
        log.write(f"Response Code: {response.status_code}\n")
        log.write(f"Response Headers: {response.headers}\n")
        log.write(f"Response Body:\n{response.text}\n")
    print(f"Response logs saved to: {log_file}")


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from io import BytesIO
from email.generator import BytesGenerator
import uuid
import requests
from flask import request, jsonify
import datetime
import base64

@app.route('/provide_register', methods=['POST'])
def provide_register():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        pdf_content = file.read()
        mime_msg, content_type = build_xds_message(pdf_content, file.filename)

        xds_url = 'http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/prb'
        headers = {
            'Content-Type': content_type,
            'MIME-Version': '1.0',
            'SOAPAction': 'urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b'
        }

        response = requests.post(
            xds_url,
            data=mime_msg,
            headers=headers,
            timeout=30
        )

        return handle_response(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def build_xds_message(pdf_bytes, filename):
    """Build a complete XDS.b message with proper MIME packaging"""
    # Generate unique IDs
    doc_id = f"Document_{uuid.uuid4()}"
    message_id = f"urn:uuid:{uuid.uuid4()}"
    
    # Build the SOAP envelope
    soap_xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
                  xmlns:wsa="http://www.w3.org/2005/08/addressing"
                  xmlns:xdsb="urn:ihe:iti:xds-b:2007"
                  xmlns:lcm="urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0"
                  xmlns:rim="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0">
  <soapenv:Header>
    <wsa:To>http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/prb</wsa:To>
    <wsa:MessageID>{message_id}</wsa:MessageID>
    <wsa:Action>urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b</wsa:Action>
  </soapenv:Header>
  <soapenv:Body>
    <xdsb:ProvideAndRegisterDocumentSetRequest>
      <lcm:SubmitObjectsRequest>
        <rim:RegistryObjectList>
          <rim:ExtrinsicObject id="{doc_id}" mimeType="application/pdf" 
              objectType="urn:uuid:7edca82f-054d-47f2-a032-9b2a5b5186c1">
            <rim:Slot name="creationTime">
              <rim:ValueList>
                <rim:Value>{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}</rim:Value>
              </rim:ValueList>
            </rim:Slot>
            <rim:Name>
              <rim:LocalizedString value="{filename}"/>
            </rim:Name>
            <rim:Classification classificationScheme="urn:uuid:93606bcf-9494-43ec-9b4e-a7748d1a838d"
                classifiedObject="{doc_id}" nodeRepresentation="" 
                objectType="urn:oasis:names:tc:ebxml-regrep:ObjectType:RegistryObject:Classification"/>
          </rim:ExtrinsicObject>
        </rim:RegistryObjectList>
      </lcm:SubmitObjectsRequest>
      <xdsb:Document id="{doc_id}">{base64.b64encode(pdf_bytes).decode('utf-8')}</xdsb:Document>
    </xdsb:ProvideAndRegisterDocumentSetRequest>
  </soapenv:Body>
</soapenv:Envelope>"""

    # Create MIME message
    boundary = f"MIMEBoundary_{uuid.uuid4().hex}"
    msg = MIMEMultipart('related', boundary=boundary, type='application/xop+xml')
    
    # SOAP part
    soap_part = MIMEText(soap_xml, 'xml', 'utf-8')
    soap_part.add_header('Content-Type', 'application/xop+xml; charset=UTF-8; type="application/soap+xml"')
    soap_part.add_header('Content-ID', '<root.message@cxf.apache.org>')
    soap_part.add_header('Content-Transfer-Encoding', '8bit')
    msg.attach(soap_part)

    # PDF part
    pdf_part = MIMEApplication(
        pdf_bytes,
        'pdf',
        _encoder=lambda x: x  # Disable base64 encoding
    )
    pdf_part.add_header('Content-Type', 'application/pdf')
    pdf_part.add_header('Content-ID', f'<{doc_id}>')
    pdf_part.add_header('Content-Transfer-Encoding', 'binary')
    msg.attach(pdf_part)

    # Generate the MIME message
    msg_bytes = BytesIO()
    gen = BytesGenerator(msg_bytes, mangle_from_=False)
    gen.flatten(msg)
    
    content_type = (
        f'multipart/related; '
        f'boundary="{boundary}"; '
        f'type="application/xop+xml"; '
        f'start="<root.message@cxf.apache.org>"; '
        f'start-info="application/soap+xml"'
    )

    return msg_bytes.getvalue(), content_type

def handle_response(response):
    """Process the XDS repository response"""
    if response.status_code != 200:
        return jsonify({
            'error': 'XDS repository error',
            'status_code': response.status_code,
            'response': response.text
        }), 500
    
    try:
        # Parse the response to extract useful information
        return jsonify({
            'status_code': response.status_code,
            'response': response.text,
            # 'message': 'Document submitted successfully'
        })
    except Exception as e:
        return jsonify({
            'error': 'Failed to parse response',
            'status_code': response.status_code,
            'response': response.text,
            'exception': str(e)
        }), 500



if __name__ == "__main__":
    app.run(debug=True, port=5002)