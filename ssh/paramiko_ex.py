
import paramiko, traceback
from paramiko_expect import SSHClientInteraction


def main():
    # Set login credentials and the server prompt
    hostname = '10.245.46.208'
    username = 'root'
    password = 'root'
    prompt = 'root@GPON-8R2:~# '
    cli_prompt = 'GPON-8R2# '


    # Use SSH client to login
    try:
        # Create a new SSH client object
        client = paramiko.SSHClient()

        # Set SSH key parameters to auto accept unknown hosts
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the host
        client.connect(hostname=hostname, username=username, password=password)

        # Create a client interaction class which will interact with the host
        interact = SSHClientInteraction(client, timeout=2, display=False)
        interact.expect(prompt)
        ##Send the command
        interact.send('pwd')        #only can using for linux mode in py3, py2 can using for CLI
        interact.expect(prompt, timeout=2)
        cmd_output_uname = interact.current_output_clean
        print(cmd_output_uname)

        interact.send('ll')
        interact.expect(prompt, timeout=2)
        cmd_output_uname = interact.current_output_clean
        print(cmd_output_uname)

        # interact.send('show card')
        # interact.expect(cli_prompt, timeout=2)
        # cmd_output_uname = interact.current_output_clean
        # print(cmd_output_uname)

    except KeyboardInterrupt:
        print('Ctrl+C interruption detected, stopping tail')
    except Exception:
        traceback.print_exc()
    finally:
        try:
            client.close()
        except:
            pass


if __name__ == '__main__':
    main()
