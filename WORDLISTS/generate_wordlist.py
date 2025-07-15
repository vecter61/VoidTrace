base_words = [
    "www", "mail", "ftp", "admin", "api", "dev", "test", "stage", "uat", "beta",
    "portal", "secure", "vpn", "webmail", "m", "mobile", "support", "blog",
    "cdn", "static", "shop", "docs", "status", "news", "auth", "gateway",
    "payments", "crm", "erp", "dashboard", "hr", "intranet", "ops", "backup",
    "db", "smtp", "pop3", "imap", "office", "exchange", "internal", "external",
    "partners", "devops", "ci", "cd", "jenkins", "gitlab", "github", "bitbucket",
    "docker", "k8s", "kubernetes", "vault", "consul", "prometheus", "grafana",
    "alertmanager", "elk", "logstash", "kibana", "splunk", "zabbix", "nagios"
]

prefixes = ["", "api-", "dev-", "test-", "stage-", "uat-", "beta-", "prod-", "backup-", "old-"]
suffixes = ["", "-dev", "-test", "-stage", "-uat", "-beta", "-prod", "-backup", "-old"]

filename = int(input("Enter The Filename to save the wordlist: ").strip())

with open(filename, "w") as f:
    # Write base words with no prefix or suffix
    for word in base_words:
        f.write(word + "\n")

    # Add numeric suffixes up to 1000 for base words
    for word in base_words:
        for i in range(1, 1001):
            f.write(f"{word}{i}\n")

    # Combine prefixes, base words, and suffixes with numeric suffixes
    for prefix in prefixes:
        for word in base_words:
            for suffix in suffixes:
                # Skip the case where all are empty (already written)
                if prefix == "" and suffix == "":
                    continue
                f.write(f"{prefix}{word}{suffix}\n")
                # Add numeric suffixes for these combinations
                for i in range(1, 101):
                    f.write(f"{prefix}{word}{suffix}{i}\n")

print(f"Wordlist generated and saved to {filename} with over 150,000 entries.")
