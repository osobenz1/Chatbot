import tkinter as tk
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def on_submit():
    user_input = entry.get()  # Récupérer le texte saisi par l'utilisateur
    try:
        # Configuration de Selenium pour ouvrir le navigateur
        driver = webdriver.Chrome()
        
        # Recherche en ligne en utilisant l'entrée de l'utilisateur comme requête de recherche
        query = user_input.replace(" ", "+")
        url = f"https://www.ft.com/search?q={query}"
        driver.get(url)
        
        # Récupérer le contenu des trois premières pages de résultats de recherche
        all_content = ""
        for _ in range(3):
            # Attendre un court instant pour que la page se charge complètement
            time.sleep(2)
            
            # Capturer le contenu de la page actuelle
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            results = soup.find_all('div', class_='o-teaser__heading')
            
            # Ajouter le contenu de la page actuelle à la variable all_content
            for result in results:
                all_content += result.text.strip() + "\n"
            
            # Passer à la page suivante
            next_button = driver.find_element_by_xpath('//button[@title="Next"]')
            next_button.click()
        
        driver.quit()
        
        # Afficher le contenu des trois premières pages de résultats de recherche
        response_label.config(text=all_content)
    except Exception as e:
        print("Une erreur s'est produite lors de la recherche en ligne:", e)

# Créer une fenêtre
window = tk.Tk()
window.title("Chatbot")

# Créer un champ de saisie
entry = tk.Entry(window, width=50)
entry.pack(pady=10)

# Créer un bouton
submit_button = tk.Button(window, text="Soumettre", command=on_submit)
submit_button.pack()

# Étiquette pour afficher la réponse
response_label = tk.Label(window, text="")
response_label.pack(pady=10)

# Lancer la boucle principale de l'interface graphique
window.mainloop()