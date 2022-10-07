from twilio.rest import Client
import keys
account_sid = keys.passwords["account_sid"]
auth = keys.passwords["auth"]
client = Client(account_sid, auth)
message = client.messages.create(
    body = "wassup dargie",
    from_="+19896327913",
    to="+447849222651"
)
print(message.sid)