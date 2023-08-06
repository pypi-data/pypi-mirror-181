import crypto

def decrypt_responses(request, formsecretkey, securehttp=True):

    #Verify that the HTTP request was sent by FormSG
    #Documentation: https://github.com/opengovsg/formsg-javascript-sdk#verifying-signatures-manually
    headers = request.headers['X-Formsg-Signature']

    #If securehttp is set to True, replace http with https. This problem was encountered using testing
    #with ngrok where request.url returned http, but webhook provided was https
    if securehttp:
        uri = request.url.replace("http://", "https://")
    else:
        uri = request.url
    crypto.verify_sig_headers(uri, headers)

    #Decrypt the encrypted portion of the data
    data = request.json
    data['data']['decryptedContent'] = crypto.decrypt_content(formsecretkey, data['data']['encryptedContent'])
    del data['data']['encryptedContent']

    return data

