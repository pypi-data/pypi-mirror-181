**This python package is unofficial and is not related in any way to Lidl. It was developed by reversed engineered requests and can stop working at anytime!**

# Lidl-Plus
**Python API for Lidl Plus**

## Installation
```commandline
pip install lidl-plus
```

## Usage
You need *Google Chrome* to run this tool.   
Alternatively, you can use the commandline tool `lidl-plus` to generate a Lidl Plus refresh token once on a device with Google Chrome.

#### Get tickets
```python
from lidlplus import LidlPlusApi

lidl = LidlPlusApi("DE", "de", refresh_token="XXXXXXXXXX")
for ticket in lidl.tickets():
    print(lidl.ticket(ticket["id"]))
```

#### Get token
```python
from lidlplus import LidlPlusApi

lidl = LidlPlusApi(language="DE", country="de")
lidl.login(phone="+4915784632296", password="password", verify_token_func=lambda: input("Insert code: "))
print(lidl.refresh_token)
```

## Generate refresh token
#### Prerequisites
You need to install *Google Chrome* and the additional packages *selenium-wire* and *getuseragent*
```commandline
pip install lidl-plus selenium-wire getuseragent
```
#### Usage
```commandline
$ lidl-plus auth
Enter lidl plus username (usually a phone number): +4915784632296
Enter lidl plus password: 
Enter language (DE, EN, ...): DE
Enter country (de, at, ...): de
Enter verify code: 590287
------------------------- refresh token ------------------------
2D4FC2A699AC703CAB8D017012658234917651203746021A4AA3F735C8A53B7F
----------------------------------------------------------------
```

