import base64
from cryptography.fernet import Fernet



payload = b'gAAAAABiMD1AoxgLLC2YSiRT0k3ng7iHEHbBPY7l7wx_kZaNMK797gLoS3Z0435G7KBqE1ZTOpgewA4_Ev-fb4rcw5c9wqS8Bbd18lJOT-xZp_argIklVDu0UB0fik_MNlAggIJWHYKHyihBED6RGDRv0UWPR7H35X_Ge6d4oPjy3MB2kGxx_tNUo18L8FPuQHqCueDAUiK19cMZcrOJwbGekZiLMH1Jz1fl4ej9tWROzqExPjp7mjwQFFrjrAhMnQtMuxG_umbkpBPCQEcgEF5LbT76Kmf8OQ=='

key_str = 'correctstaplecorrectstaplecorrec'
key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)
plain = f.decrypt(payload)
exec(plain.decode())
