find_document_request = """<?xml version='1.0' encoding='UTF-8'?>
        <soapenv:Envelope
            xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://www.w3.org/2005/08/addressing"
            xmlns:query="urn:oasis:names:tc:ebxml-regrep:xsd:query:3.0"
            xmlns:rim="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0"
            xmlns:rs="urn:oasis:names:tc:ebxml-regrep:xsd:rs:3.0">
            <soapenv:Header>
                <wsa:To soapenv:mustUnderstand="true">http://localhost:8081/xdstools7.12.0/sim/default__registry_simulator/reg/sq</wsa:To>
                <wsa:MessageID soapenv:mustUnderstand="true">urn:uuid:175709BC017996C4D31741859309458</wsa:MessageID>
                <wsa:Action soapenv:mustUnderstand="true">urn:ihe:iti:2007:RegistryStoredQuery</wsa:Action>
            </soapenv:Header>
            <soapenv:Body>
                <query:AdhocQueryRequest>
                    <query:ResponseOption returnComposedObjects="true" returnType="LeafClass"/>
                    <rim:AdhocQuery id="urn:uuid:14d4debf-8f97-4251-9a74-a90016b0af0d">
                        <rim:Slot name="$XDSDocumentEntryPatientId">
                        <rim:ValueList>
                            <rim:Value>'{}'</rim:Value>
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


get_document_request = """<soapenv:Envelope
    xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
    xmlns:wsa="http://www.w3.org/2005/08/addressing"
    xmlns:query="urn:oasis:names:tc:ebxml-regrep:xsd:query:3.0"
    xmlns:rim="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0">
    
    <soapenv:Header>
        <wsa:To soapenv:mustUnderstand="true">http://localhost:8081/xdstools7.12.0/sim/default__registry_simulator/reg/sq</wsa:To>
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
                        <rim:Value>('{}')</rim:Value>
                    </rim:ValueList>
                </rim:Slot>

            </rim:AdhocQuery>
        </query:AdhocQueryRequest>
    </soapenv:Body>
</soapenv:Envelope>"""


retrieve_document_request = """<?xml version='1.0' encoding='UTF-8'?>
    <soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
        <soapenv:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
            <wsa:To soapenv:mustUnderstand="true">http://localhost:8081/xdstools7.12.0/sim/default__repository_simulator/rep/ret</wsa:To>
            <wsa:MessageID soapenv:mustUnderstand="true">urn:uuid:175709BC017996C4D31741869359321</wsa:MessageID>
            <wsa:Action soapenv:mustUnderstand="true">urn:ihe:iti:2007:RetrieveDocumentSet</wsa:Action>
        </soapenv:Header>
        <soapenv:Body>
            <RetrieveDocumentSetRequest xmlns="urn:ihe:iti:xds-b:2007">
                <DocumentRequest>
                    <RepositoryUniqueId>1.2.42.20250321131750.8</RepositoryUniqueId>
                    <DocumentUniqueId>{}</DocumentUniqueId>
                </DocumentRequest>
            </RetrieveDocumentSetRequest>
        </soapenv:Body>
    </soapenv:Envelope>
    """