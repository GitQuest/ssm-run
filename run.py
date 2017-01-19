import sys

f = open(sys.argv[2])
id = sys.argv[1]

commands = [x for x in f.read().split('\n') if x]

import boto3
ssm = boto3.client("ssm")

res = ssm.send_command(InstanceIds=[id],
        DocumentName="AWS-RunPowerShellScript",
        Parameters=dict(commands=commands))

cmd_id = res["Command"]["CommandId"]

while True:

    try:

        r = ssm.get_command_invocation(
                CommandId=cmd_id,
                InstanceId=id)

        if r["Status"] in ['Success','Failed']:
            break

        print(r["Status"])

    except Exception as ex:
        pass

    import time
    time.sleep(1)

res = ssm.list_command_invocations(
        CommandId=cmd_id, 
        Details=True)

print("\n")
print(res["CommandInvocations"][0]["CommandPlugins"][0]["Output"])

