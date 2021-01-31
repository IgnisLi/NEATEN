from models import *

def save(identifier,voiceprint,key1,key2,keyH):
    user = Agreeuser(identifier=identifier,voiceprint=voiceprint,key1=key1,key2=key2,keyH=keyH)
    session=DBSession()
    session.add(user)
    session.commit()
    session.close()

def login_add(identifier,success):
    session = DBSession()
    login_user = Agreelogin(identifier=identifier,success=success)
    session.add(login_user)
    session.commit()
    session.close()

def findvoice(iden):
    session=DBSession()
    user_voice =session.query(Agreeuser).filter(Agreeuser.identifier==iden).one()
    # print(user_voice)
    voiceprint=user_voice.voiceprint
    key1=user_voice.key1
    key2=user_voice.key2
    keyH=user_voice.keyH
    session.close()
    return (voiceprint,key1,key2,keyH)