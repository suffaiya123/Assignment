class ResponseWrapper:
    def response(self, response, message, code):
        data = {
            "success": True,
            "response": response,
            "message": message
        }
        return (data, code)