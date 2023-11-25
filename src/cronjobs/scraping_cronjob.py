import subprocess

# Chemin vers les scripts à exécuter
scraping_script = r"C:\Users\yaya-\Documents\Github\JAN23CDE_satisfaction\src\scraping_trustpilot.py"
bdd_script = r"C:\Users\yaya-\Documents\Github\JAN23CDE_satisfaction\src\bdd_trustpilot.py"

# Commande pour exécuter le script de scraping
scraping_command = f"python {scraping_script}"

# Commande pour exécuter le script de base de données
bdd_command = f"python {bdd_script}"

# Exécuter le script de scraping
subprocess.run(scraping_command, shell=True, check=True)

# Exécuter le script de base de données après le scraping
subprocess.run(bdd_command, shell=True, check=True)
