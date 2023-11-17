# cronjob_script.py
import subprocess

def run_notebook_scraping():
    try:
        # Convert Jupyter Notebook to script
        subprocess.run(['jupyter', 'nbconvert', '--to', 'script', 'C:\\Users\\yaya-\\Documents\\Github\\JAN23CDE_satisfaction\\src\\notebook_scraping.ipynb'])
        
        # Run the generated script
        subprocess.run(['python', 'C:\\Users\\yaya-\\Documents\\Github\\JAN23CDE_satisfaction\\src\\notebook_scraping.py'])
    except Exception as e:
        print(f"Error running notebook scraping: {e}")

def run_bdd_trustpilot():
    try:
        # Run the Elasticsearch script
        subprocess.run(['python', 'C:\\Users\\yaya-\\Documents\\Github\\JAN23CDE_satisfaction\\src\\bdd_trustpilot.py'])
    except Exception as e:
        print(f"Error running bdd_trustpilot script: {e}")

if __name__ == "__main__":
    run_notebook_scraping()
    run_bdd_trustpilot()
