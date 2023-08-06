def parse_twilio_request_to_dictionary(request):
    """
    content type header from twilio is application/x-www-form-urlencoded
    so we first change it to a regular dictionary
    """
    return request.form.to_dict()

def resolve_tenant_id(data):
    tenant_id = data.get('wid')
    if not tenant_id:
        raise Exception("Tenant id not found in data")
    return tenant_id