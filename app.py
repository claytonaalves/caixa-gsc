from __future__ import print_function

from zeep import xsd

from requests import Session

from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken

from config import Config

session = Session()
session.verify = False
transport = Transport(session=session)

header = xsd.Element(
    'AuthenticationInfo',
    xsd.ComplexType([
        xsd.Element('userName', xsd.String()),
        xsd.Element('password', xsd.String())
    ])
)
header_value = header(userName=Config.username, password=Config.password)

url = Config.url

# GetList_Abertura(
#   Qualification: xsd:string, 
#   Token: xsd:string, 
#   Capturado: xsd:string,
#   startRecord: xsd:string, 
#   maxLimit: xsd:string,
# _soapheaders={parameters: ns0:AuthenticationInfo})

client = Client(url, transport=transport)

res = client.service.GetList_Abertura(Config.cpy, Config.token, "", "", "", _soapheaders=[header_value])
print(res)
