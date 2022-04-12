from twilio.rest import Client

account_sid = "AC160beabbacde45247733ce54890c6abc"
auth = "b7f44ee4a5765575a73f67fef286549d"
client = Client(account_sid, auth)
message = client.messages.create(
    body = "wassup dargie",
    from_="+19896327913",
    to="+447849222651"
)
print(message.sid)