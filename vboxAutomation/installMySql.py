import paramiko


def installMySQL(hostname, port, username, password, root_password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, port=port, username=username, password=password)
        print(f"Erfolgreich mit {hostname} als {username} verbunden.")

        # Wechsel in den su-Modus und dann MySQL installieren
        su_command = f"echo '{root_password}' | su -c 'apt-get update && apt-get install -y mysql-server'"

        # Der Befehl 'su' erfordert, dass das Root-Passwort eingegeben wird, und wir möchten den Befehl im Root-Modus ausführen.
        stdin, stdout, stderr = ssh.exec_command(su_command)

        # Fehler- und Standardausgabe abfangen
        stdout_output = stdout.read().decode()
        stderr_output = stderr.read().decode()

        if stdout_output:
            print("Standardausgabe:\n", stdout_output)
        if stderr_output:
            print("Fehlerausgabe:\n", stderr_output)

        print("Datenbankinstallation abgeschlossen.")

        # Installation überprüfen
        check_command = "mysql --version"
        stdin, stdout, stderr = ssh.exec_command(check_command)
        output = stdout.read().decode()

        if "mysql" in output:
            print("MySQL wurde erfolgreich installiert.")
        else:
            print("MySQL scheint nicht installiert zu sein.")

    except paramiko.AuthenticationException as auth_error:
        print(f"Authentifizierungsfehler: {auth_error}")
    except Exception as e:
        print(f"Fehler bei der Verbindung oder Installation: {e}")

    finally:
        ssh.close()
        print("Verbindung geschlossen.")


