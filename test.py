import uuid
import requests
import datetime
from flask import request, jsonify
import xml.sax.saxutils as xml_utils
import base64

@app.route("/provide_register", methods=["POST"])
def provide_register():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400
            
        patient_id = request.form.get("patientId") or "12335^^^&amp;1.2.3.4.5&amp;ISO"
        patient_id = xml_utils.escape(patient_id)
        mime_type = file.mimetype or "application/pdf"
        
        # Read and encode document content
        document_content = file.read()
        document_content_b64 = base64.b64encode(document_content).decode('utf-8')
        
        # Generate all required IDs
        document_id = f"urn:uuid:{uuid.uuid4()}"
        submission_set_id = f"urn:uuid:{uuid.uuid4()}"
        message_id = f"urn:uuid:{uuid.uuid4()}"
        boundary = f"MIMEBoundary_{uuid.uuid4().hex}"
        
        # HL7 V2 format timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Build the complete SOAP envelope
        soap_envelope = f'''<?xml version="1.0" encoding="UTF-8"?>
<S:Envelope xmlns:S="http://www.w3.org/2003/05/soap-envelope"
             xmlns:wsa="http://www.w3.org/2005/08/addressing">
    <S:Header>
        <wsa:To S:mustUnderstand="true">http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/prb</wsa:To>
        <wsa:Action S:mustUnderstand="true">urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b</wsa:Action>
        <wsa:MessageID S:mustUnderstand="true">{message_id}</wsa:MessageID>
        <wsa:ReplyTo S:mustUnderstand="true">
            <wsa:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </S:Header>
    <S:Body>
        <ProvideAndRegisterDocumentSetRequest xmlns="urn:ihe:iti:xds-b:2007">
            <SubmitObjectsRequest xmlns="urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0">
                <RegistryObjectList xmlns="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0">
                    <!-- Submission Set -->
                    <RegistryPackage id="{submission_set_id}" objectType="urn:uuid:a54d6aa5-d40d-43f9-88c5-b4633d873bdd">
                        <Slot name="submissionTime">
                            <ValueList>
                                <Value>{timestamp}</Value>
                            </ValueList>
                        </Slot>
                        <Name>
                            <LocalizedString value="Sample Submission"/>
                        </Name>
                        <Description>
                            <LocalizedString value="Submission of clinical documents"/>
                        </Description>
                        <Classification classifiedObject="{submission_set_id}" 
                                     classificationNode="urn:uuid:a7058bb9-b4e4-4307-ba5b-e3f0ab85e12d"
                                     id="urn:uuid:{uuid.uuid4()}"/>
                        <Classification classifiedObject="{submission_set_id}" 
                                     classificationNode="urn:uuid:aa543740-bdda-424e-8c96-df4873be8500"
                                     id="urn:uuid:{uuid.uuid4()}"/>
                        <ExternalIdentifier identificationScheme="urn:uuid:96fdda7c-d067-4183-912e-bf5ee74998a8" 
                                       value="{submission_set_id}"
                                       registryObject="{submission_set_id}"
                                       id="urn:uuid:{uuid.uuid4()}">
                            <Name>
                                <LocalizedString value="XDSSubmissionSet.uniqueId"/>
                            </Name>
                        </ExternalIdentifier>
                        <ExternalIdentifier identificationScheme="urn:uuid:554ac39e-e3fe-47fe-b233-965d2a147832" 
                                       value="1.3.6.1.4.1.21367.2009.1.2.1"
                                       registryObject="{submission_set_id}"
                                       id="urn:uuid:{uuid.uuid4()}">
                            <Name>
                                <LocalizedString value="XDSSubmissionSet.sourceId"/>
                            </Name>
                        </ExternalIdentifier>
                        <ExternalIdentifier identificationScheme="urn:uuid:6b5aea1a-874d-4603-a4bc-96a0a7b38446" 
                                       value="{patient_id}"
                                       registryObject="{submission_set_id}"
                                       id="urn:uuid:{uuid.uuid4()}">
                            <Name>
                                <LocalizedString value="XDSSubmissionSet.patientId"/>
                            </Name>
                        </ExternalIdentifier>
                    </RegistryPackage>
                    
                    <!-- Document Entry -->
                    <ExtrinsicObject id="{document_id}" mimeType="{mime_type}" objectType="urn:uuid:7edca82f-054d-47f2-a032-9b2a5b5186c1">
                        <Slot name="creationTime">
                            <ValueList>
                                <Value>{timestamp}</Value>
                            </ValueList>
                        </Slot>
                        <Slot name="languageCode">
                            <ValueList>
                                <Value>en-US</Value>
                            </ValueList>
                        </Slot>
                        <Slot name="sourcePatientId">
                            <ValueList>
                                <Value>{patient_id}</Value>
                            </ValueList>
                        </Slot>
                        <Name>
                            <LocalizedString value="Document"/>
                        </Name>
                        <Description>
                            <LocalizedString value="Document description"/>
                        </Description>
                        <!-- Required Classifications -->
                        <Classification classifiedObject="{document_id}" 
                                     classificationNode="urn:uuid:41a5887f-8865-4c09-adf7-e362475b143a"
                                     id="urn:uuid:{uuid.uuid4()}"/>
                        <Classification classifiedObject="{document_id}" 
                                     classificationNode="urn:uuid:f4f85eac-e6cb-4883-b524-f2705394840f"
                                     id="urn:uuid:{uuid.uuid4()}"/>
                        <Classification classifiedObject="{document_id}" 
                                     classificationNode="urn:uuid:a09d5840-386c-46f2-b5ad-9c3699a4309d"
                                     id="urn:uuid:{uuid.uuid4()}"/>
                        <Classification classifiedObject="{document_id}" 
                                     classificationNode="urn:uuid:f33fb8ac-18af-42cc-ae0e-ed0b0bdb91e1"
                                     id="urn:uuid:{uuid.uuid4()}"/>
                        <Classification classifiedObject="{document_id}" 
                                     classificationNode="urn:uuid:f0306f51-975f-434e-a61c-c59651d33983"
                                     id="urn:uuid:{uuid.uuid4()}"/>
                        <Classification classifiedObject="{document_id}" 
                                     classificationNode="urn:uuid:cccf5598-8b07-4b77-a05e-ae952c785ead"
                                     id="urn:uuid:{uuid.uuid4()}"/>
                        <!-- Required External Identifiers -->
                        <ExternalIdentifier identificationScheme="urn:uuid:2e82c1f6-a085-4c72-9da3-8640a32e42ab" 
                                       value="{document_id}"
                                       registryObject="{document_id}"
                                       id="urn:uuid:{uuid.uuid4()}">
                            <Name>
                                <LocalizedString value="XDSDocumentEntry.uniqueId"/>
                            </Name>
                        </ExternalIdentifier>
                        <ExternalIdentifier identificationScheme="urn:uuid:58a6f841-87b3-4a3e-92fd-a8ffeff98427" 
                                       value="{patient_id}"
                                       registryObject="{document_id}"
                                       id="urn:uuid:{uuid.uuid4()}">
                            <Name>
                                <LocalizedString value="XDSDocumentEntry.patientId"/>
                            </Name>
                        </ExternalIdentifier>
                    </ExtrinsicObject>
                    
                    <!-- Association between SubmissionSet and Document -->
                    <Association associationType="urn:oasis:names:tc:ebxml-regrep:AssociationType:HasMember" 
                            sourceObject="{submission_set_id}"
                            targetObject="{document_id}"
                            id="urn:uuid:{uuid.uuid4()}">
                        <Slot name="SubmissionSetStatus">
                            <ValueList>
                                <Value>Original</Value>
                            </ValueList>
                        </Slot>
                    </Association>
                </RegistryObjectList>
            </SubmitObjectsRequest>
            <Document id="{document_id}">{document_content_b64}</Document>
        </ProvideAndRegisterDocumentSetRequest>
    </S:Body>
</S:Envelope>'''

        # Build the multipart message
        multipart_body = (
            f"--{boundary}\r\n"
            f'Content-Type: application/xop+xml; charset=UTF-8; type="application/soap+xml"\r\n'
            f'Content-Transfer-Encoding: binary\r\n'
            f'Content-ID: <root.message@xds>\r\n\r\n'
            f'{soap_envelope}\r\n'
            f"--{boundary}\r\n"
            f"Content-Type: {mime_type}\r\n"
            f"Content-Transfer-Encoding: binary\r\n"
            f"Content-ID: <{document_id}>\r\n\r\n"
        ).encode('utf-8') + document_content + f"\r\n--{boundary}--\r\n".encode('utf-8')

        # Set headers
        headers = {
            "Content-Type": f'multipart/related; boundary="{boundary}"; type="application/xop+xml"; '
                          f'start="<root.message@xds>"; start-info="application/soap+xml"; '
                          f'action="urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b"',
            "MIME-Version": "1.0"
        }

        # Send request
        xds_url = "http://localhost:8084/xdstools7.12.0/sim/default__repository01/rep/prb"
        response = requests.post(xds_url, data=multipart_body, headers=headers)

        return jsonify({
            "status": response.status_code,
            "response": response.text
        }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500