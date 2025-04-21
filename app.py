from flask import Flask, request, Response
from spyne import Application, rpc, ServiceBase, String, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import os

app = Flask(__name__)


from spyne import ComplexModel, Array, String, Boolean, Unicode

class Slot(ComplexModel):
    _type_info = {
        'name': String,
        'ValueList': Array(String)
    }

class AdhocQuery(ComplexModel):
    __namespace__ = "XDSbRegistry"
    _type_info = {
        'id': Unicode,
        'Slot': Array(Slot)
    }

class ResponseOption(ComplexModel):
    __namespace__ = "XDSbRegistry"

    returnComposedObjects = Boolean
    returnType = String

    def __init__(self, **kwargs):
        if "_attributes" in kwargs:
            attributes = kwargs["_attributes"]
            kwargs["returnComposedObjects"] = attributes.get("returnComposedObjects", False)
            kwargs["returnType"] = attributes.get("returnType", "")
            del kwargs["_attributes"]  # Remove to prevent unexpected argument error

        super().__init__(**kwargs)
    
# Response Handlers (Equivalent to DocumentRegistry_RegistryStoredQuery in Node.js)
class RegistryStoredQueryResponse(ComplexModel):
    __namespace__ = "file:/home/sumasoft/HL7_Project/xds_zeep/XDS.b_DocumentRepository.wsdl"
    response = String

def DocumentRegistry_RegistryStoredQuery():
    return RegistryStoredQueryResponse(response="Registry Query Response")

def DocumentRegistry_RegistryStoredQuery_ObjectRef(document_list):
    return RegistryStoredQueryResponse(response=f"Document References: {', '.join(document_list)}")

# SOAP Service Definition
class XDSbRegistryService(ServiceBase):
    
    @rpc(ResponseOption, AdhocQuery, _returns=RegistryStoredQueryResponse, _in_variable_names={'response_option': 'ResponseOption', 'adhoc_query': 'AdhocQuery'})
    def DocumentRegistry_RegistryStoredQuery(ctx, response_option, adhoc_query):
        print("Received ResponseOption:", response_option.returnType, response_option.returnComposedObjects)
        print("Received AdhocQuery ID:", adhoc_query.id)
        
        for slot in adhoc_query.Slot:
            print(f"Slot Name: {slot.name}, Values: {slot.ValueList}")

        if "$XDSDocumentEntryEntryUUID" in adhoc_query.id:
            return DocumentRegistry_RegistryStoredQuery()
        else:
            return DocumentRegistry_RegistryStoredQuery_ObjectRef(
                ["urn:uuid:78eda03c-47e0-44ed-bc10-f8700add5a93"]
            )


    @rpc(String, _returns=RegistryStoredQueryResponse)
    def DocumentRegistry_RegisterDocumentSet_b(ctx, document_set):
        return DocumentRegistry_RegistryStoredQuery()

# SOAP Application
soap_app = Application([XDSbRegistryService], 
                        'XDSbRegistry',
                        in_protocol=Soap11(validator='lxml'), 
                        out_protocol=Soap11())

wsgi_app = WsgiApplication(soap_app)

@app.route("/DocumentRegistry", methods=["GET", "POST"])
def soap_service():
    # Print request headers
    print("Headers:", request.headers)

    # Print request body
    try:
        request_body = request.data.decode("utf-8")
        print("Request Body:", request_body)
    except Exception as e:
        print("Error reading request body:", e)

    all_params = request.args.to_dict()
    print("Query Parameters:", all_params)
    response = wsgi_app(request.environ, start_response)
    return Response(response, content_type="text/xml")


def start_response(status, headers):
    print(status)
    print(headers)

    return headers

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)