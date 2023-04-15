import time
import boto3
import paramiko
import os
import json
SNS_ARN = 'arn:aws:sns:ap-south-1:144883820914:secScraperTopic'

rsa_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAn4/Vu3/OAaTlKZsq3BfUTA4uZQCxk3xaIOU2cH9towhEPwqJ
LXhh9ePXFrPb8j14kQTGcqOYKjhbrLpQTbfGRmT1ccRQAcdoZ1pX/Bvnf01rgI9p
/CAAjBbS0ybT9bge9B5d7SiUY8BA4+hLTmxHV1WfswBoZQg/rCRk/+7sqeTQSvFQ
HrdyOsyIbRtoYSMTYWfTF1UseV3MMLm6A9GsllNEG+cabaEpNaZ4eCO8jSWSpfaf
vqBzLLoAN4W/uA+uVCzx9lNhSfhv3U7spXtmGIHF29AMLTY5LJwF0STRmzrhdSt6
L1JwdKm/MeDSQJi44A9eoLl0AN7r+SeHqLRD/wIDAQABAoIBAHKUwXDxqCe6F+42
xSJj4knzbRGO2/YDOF2i++LxPvPyPb/fev6yEfaXdJ+S7QEZb3kEKtWr8NtwuTRi
XsRQkgt++FqIFMQSREDjuYcLKsRZ/jbFxeANwxbWVPLYUSGE5IV9QQnLODQhnPeM
mndofhqTHClYw565u6+MOxMmqcCdsJNAUAap7Zaf5hfr/y9k0eDGwf5JqQBSY+Iz
cRyfgFmmQswKqlQ2uTJE6gBdJAUPykTi90ihsWFSfDU/pbCyz9Lx88wcn/7yCkhJ
SIeF0lHq25AAHgHKvwO30t28hlGsZ/YFwz9Co1Moni+pk+0G8Dwr4x2o2Yj5+8om
MhJApXECgYEA56nHCX4ElJy0w9UlKWvjJxUrfQ7FX5vdz88729CLDkhD5KicGHl4
1kFPPgDfFctCdzIBf6vpYep4oPd7QaAqZGv5xYx47z0n0e7zTmRbjRZODYVLZ21z
A8/CNt6YcRHT4tcEe4H0g0xJmdE36Q3REI9BY/jg7NkSCa7yyPFOTJUCgYEAsFMA
8EjZT8gUJvFxgIJHEFUFzhSYmDWuAQiwGe1XMW4KsT0xfmWZzEkW8Pr6K3u6UEo1
AeVuJ45HyFLUjEy+kQl4S9quC/CKHNM3ax4RyuOEHuRisHdu3jTVEp5u5NwzUfCT
PJMdqM3s+IVVyOI22PvCvqXo1FhFI6FIpFe2FUMCgYEA321QCGigtE/6y1C7uZpT
BzOUsNVZKJ/kKvN8kMEuDAVIbbTsb3JgR4vPiEZA4f0aSmlRJrg/q27/DogBOUbm
+9ljmNKlJF+AEyn5QObroUQc3U9sbQETR17NuiuvLIX8LDAiI5gvoZ4m8hHlcYEg
3G69q1SyYdvtWKeBgqmwUY0CgYBOTY4tJyzacVABu1dcan6Ekj1xt1PMxInxi5oo
6W2/Vc8JxtMj/pq+TfcSLWLLzLaA0XOY0/qHNnhKTf52D97RKhNyHDsOslOjWWlS
+JeOMluKHIJ3O5LQu0WkbxdwKxnfWacJT4vsWwbRluTxwQP6eFOTtrofEtQhbo6D
7S+/YQKBgFcz/pg/E3xYt80cYQpG6CDCHqitU8EO9lDfP81LpXTebgnqNAxztkj6
8H7J72GoiEM43fkz0/AioNfDe13FSJiljRcQhKD/4XZoDV0DOwUg+QMA34w5vD2f
p9arlzXR4K7wLiGaDafkKCNP7wZ6Wknw2TadZB6AiOHu+tmv4993
-----END RSA PRIVATE KEY-----"""

def lambda_handler(event=None, context=None):

    ec2 = boto3.resource('ec2', region_name='ap-south-1',aws_access_key_id='AKIASDO57VFZPXDBKKNV',aws_secret_access_key='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')

    instance_id = 'i-050bc887ad2ee2214'
    instance = ec2.Instance(instance_id)
    instance.start()

    print("EC2 instance started")

    time.sleep(60)

    key_location = '/tmp/sec_scraper_key.pem'

    with open(key_location,'w') as f:
        f.write(rsa_key)
    
    print("ip: ",instance.public_ip_address)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(key_location)
    ssh.connect(instance.public_ip_address,22, username='ubuntu', pkey=privkey)

    print("SSH done")

    commands = [
    '. ~/sec-scraper/xbrl-scrapper/script.sh'
    ]
    for command in commands:
        print("Executing {}".format(command))
        stdin , stdout, stderr = ssh.exec_command(command)
        stdin.flush()
        data = stdout.read().splitlines()
        print("Error: {}".format(stderr.read()))
        for line in data:
            print(line)
    ssh.close()
    return 'Success'


lambda_handler()
