import paramiko


def fill_sampleDataMySQL(hostname, port, username, password, root_password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, port=port, username=username, password=password)
        print(f"Erfolgreich mit {hostname} als {username} verbunden.")

        # gucke ob git installliert ist
        check_git_command = "git --version"
        stdin, stdout, stderr = ssh.exec_command(check_git_command)
        git_installed = "git version" in stdout.read().decode()

        if git_installed:
            print("Git ist bereits installiert.")
        else:
            # Wechsel in den su-Modus und dann erst git installieren
            su_install_git_command = f"echo '{root_password}' | su -c 'apt install -y git'"

            # den vorherigen Befehl im su Modus ausführen
            # für alle folgenden Befehle ist dies nicht mehr nötig, von daher kann auf den ersten Befehl verzichtet werden
            stdin, stdout, stderr = ssh.exec_command(su_install_git_command)
            print("Git-Installation gestartet.")
            # Fehler- und Standardausgabe abfangen
            stdout_output = stdout.read().decode()
            stderr_output = stderr.read().decode()

            if stdout_output:
                print("Standardausgabe:\n", stdout_output)
            if stderr_output:
                print("Fehlerausgabe:\n", stderr_output)

            print("Git-Installation abgeschlossen.")

        # Prüfen, ob das Verzeichnis `test_db` bereits existiert
        check_dir_command = "test -d test_db && echo 'exists' || echo 'not exists'"
        stdin, stdout, stderr = ssh.exec_command(check_dir_command)
        dir_status = stdout.read().decode().strip()

        if dir_status == "exists":
            print("Das Verzeichnis test_db existiert bereits, das Klonen wird übersprungen.")
        else:
            # Klone das Repo im su-Modus
            su_clone_repo_command = f"echo '{root_password}' | su -c 'git clone https://github.com/datacharmer/test_db'"
            stdin, stdout, stderr = ssh.exec_command(su_clone_repo_command)
            stdout_output = stdout.read().decode()
            stderr_output = stderr.read().decode()

            if stdout_output:
                print("Standardausgabe:\n", stdout_output)
            if stderr_output:
                print("Fehlerausgabe:\n", stderr_output)

            print("Das Repository wurde erfolgreich geklont.")

        # In das geklonte Verzeichnis wechseln und ein Kommando ausführen
        su_cd_command = f"echo '{root_password}' | su -c 'cd test_db && ls -l'"
        stdin, stdout, stderr = ssh.exec_command(su_cd_command)
        stdout_output = stdout.read().decode()
        stderr_output = stderr.read().decode()

        if stdout_output:
            print("Standardausgabe:\n", stdout_output)
        if stderr_output:
            print("Fehlerausgabe:\n", stderr_output)

        print("Erfolgreich in das Verzeichnis test_db gewechselt und Inhalt angezeigt.")

        # Versuch, sich bei MySQL anzumelden und die Datenbank employees zu erstellen
        su_mysql_create_db = f"echo '{root_password}' | su -c \"mysql -u root -p{root_password} -e 'CREATE DATABASE IF NOT EXISTS employees;'\""
        stdin, stdout, stderr = ssh.exec_command(su_mysql_create_db)
        stdout_output = stdout.read().decode()
        stderr_output = stderr.read().decode()

        if stdout_output:
            print("Standardausgabe (Datenbankerstellung):\n", stdout_output)
        if stderr_output:
            print("Fehlerausgabe (Datenbankerstellung):\n", stderr_output)

        print("Bei MySQL angemeldet und Datenbank erstellt.")

        # Haupt-SQL-Datei ausführen
        su_import_sql_command = (
            f"echo '{root_password}' | su -c 'mysql -u root -p{root_password} < /home/{username}/test_db/employees.sql'"
        )
        stdin, stdout, stderr = ssh.exec_command(su_import_sql_command)
        print(stdout.read().decode())
        print(stderr.read().decode())

        # Einzelne .dump-Dateien nacheinander laden
        dump_files = [
            "load_departments.dump",
            "load_employees.dump",
            "load_dept_emp.dump",
            "load_dept_manager.dump",
            "load_titles.dump",
            "load_salaries1.dump",
            "load_salaries2.dump",
            "load_salaries3.dump"
        ]

        for dump_file in dump_files:
            su_import_dump_command = (
                f"echo '{root_password}' | su -c 'mysql -u root -p{root_password} employees < /home/{username}/test_db/{dump_file}'"
            )
            stdin, stdout, stderr = ssh.exec_command(su_import_dump_command)
            print(f"Loading {dump_file}...")
            print(stdout.read().decode())
            print(stderr.read().decode())

        # Überprüfen, ob die Tabellen erstellt wurden
        su_verify_tables = f"echo '{root_password}' | su -c 'mysql -u root -p{root_password} employees < test_db/test_employees_md5.sql'"
        stdin, stdout, stderr = ssh.exec_command(su_verify_tables)
        stdout_output = stdout.read().decode()
        stderr_output = stderr.read().decode()

        if stdout_output:
            print("Standardausgabe (Tabellenüberprüfung):\n", stdout_output)
        if stderr_output:
            print("Fehlerausgabe (Tabellenüberprüfung):\n", stderr_output)

        print("Tabellen erfolgreich erstellt und überprüft.")

    except paramiko.AuthenticationException as auth_error:
        print(f"Authentifizierungsfehler: {auth_error}")
    except Exception as e:
        print(f"Fehler bei der Verbindung oder Installation: {e}")

    finally:
        ssh.close()
        print("Verbindung geschlossen.")

