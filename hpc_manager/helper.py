
def req_json(req):
    """
    Gets the JSON body from req (already processed by JSONTranslator)
    """

    return req.context["doc"]