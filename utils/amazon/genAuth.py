import boto3
from requests_aws4auth.aws4auth import AWS4Auth

import const as const

def genAuth():
    session = boto3.Session(
        aws_access_key_id=const.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=const.AWS_SECRET_KEY_ID,
        region_name=const.REGION_NAME
    )

    client = session.client('sts')

    res = client.assume_role(
        RoleArn=const.ROLE_ARN,
        RoleSessionName='session'
    )

    AccessKeyId = res['Credentials']['AccessKeyId']
    SecretAccessKey = res['Credentials']['SecretAccessKey']
    SessionToken = res['Credentials']['SessionToken']

    # print(AccessKeyId)
    # print(SecretAccessKey)
    # print(SessionToken)

    auth = AWS4Auth(
        AccessKeyId,
        SecretAccessKey,
        const.REGION_NAME,
        'execute-api',
        session_token=SessionToken
    )

    return auth


if __name__ == '__main__':
    genAuth()
