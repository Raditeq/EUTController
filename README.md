# EUT Controller TCP server
Python EUT controller tcp server

This example python script can be used together with the EUT Controller device driver of RadiMation. The RadiMation driver will send EUT information and Test information items to this python eut controller tcp server. Additionally it is possible to update test information items in the test data.
## Receiving EUT information items
At the start of a test the RadiMation EUT Controller driver will send all known EUT information items to the EUT Controller server.

The format is: EUTINFO key=value
## Receiving Test information items
At the start and during a test the RadiMation EUT Controller driver will send test information items to the EUT Controller server.

The format is: TESTINFO key=value
## Update test information in the RadiMation test data
The EUT Controller driver will send a request "TESTINFO?" to the server and the EUT Controller Server is then able to respond with a key and value which will update or create new information items.

The format to send information back is: key=value
