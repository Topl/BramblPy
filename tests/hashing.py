from brambl.utils import Hash
import canonicaljson


password = 'My password is password.'
salt = Hash.get_random_bytes(32)
key = Hash.scrypt(password,salt,32,N=2**14, r=8, p=1)
result = Hash.gencipher('aes-256-ctr',key,'Hello World')
message = Hash.genDecipher(key,result)
print(message)


print(Hash.string('this is test','base58'))

print(Hash.file('/home/arjunmehta/Brambl-Py/tests/fileTest.txt','base64'))

