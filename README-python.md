# The Python BMW API wrapper

The `bmw.py` file is a basic module that you can import to make convenient use of the (unofficial, unsupported) BMW i3 API.  For details of the API, please see the main [README.md](README.md) file.

To use this, you will need to know some authentication details used by your phone app.  This can be discovered by capturing the traffic between the app and the server -- a process which beyond the scope of this document.  The protocol requires an 'access token', which expires periodically and is then regenerated using your API key and secret (analagous to your username and password). You can discover these by looking at the traffic at the time the app is re-authenticating.  

The request will contain the base64-encoded version of key:secret, which can be put in the credentials.json file as 'auth_basic'.  Until that time, you may be able to capture the access token and use that.
