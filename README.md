# Progetto Finale: FastAPI Web App

Un'applicazione web moderna e reattiva sviluppata con **FastAPI**, che combina funzionalità di elaborazione immagini locale con un **Pokédex Interattivo** avanzato interamente localizzato in italiano.

## 🚀 Funzionalità Principali

### 1. Elaborazione e Analisi Immagini
- Upload di file d'immagine locali direttamente dall'interfaccia web.
- Endpoint dedicato per l'analisi dei file multimediali inviati tramite form multipart (`enctype="multipart/form-data"`).

### 2. Pokédex Interattivo Avanzato (RPG)
- **Integrazione API Esterna:** Connessione asincrona in tempo reale a [PokéAPI](https://pokeapi.co/) tramite la libreria `httpx`.
- **Navigazione Ricorsiva dell'Albero Evolutivo:** Algoritmo ricorsivo personalizzato che analizza la struttura complessa delle `evolution_chain` dell'API per estrarre accuratamente le forme precedenti ("Evolve da") e le evoluzioni successive ("Evolve in").
- **Localizzazione Completa:** - Traduzione automatica dei tipi di Pokémon dall'inglese all'italiano (es. *Fire* -> *Fuoco*, *Electric* -> *Elettro*).
  - Conversione dinamica delle generazioni di origine dai numeri romani ai numeri arabi (es. *Generation I* -> *Generazione 1*).
- **Dati Tecnici:** Mostra informazioni dettagliate quali Origine (Generazione), Esperienza Base (XP), peso (in ettogrammi) e sprite ufficiali.

---

## 🛠️ Tech Stack & Librerie

- **Backend Framework:** FastAPI (Asynchronous Server Gateway Interface)
- **Web Server:** Uvicorn (con supporto `--reload` per lo sviluppo)
- **Template Engine:** Jinja2 (per il rendering dinamico dell'HTML e gestione dei blocchi condizionali `{% if %}`)
- **HTTP Client:** HTTPX (per chiamate asincrone non bloccanti alle API esterne)
- **Frontend:** HTML5 purificato e CSS3 personalizzato (`/static/style.css`)

---

## 📂 Struttura del Progetto

```text
Progetto finale/
├── main.py                 # Core dell'applicazione, rotte FastAPI e logica API
├── static/
│   └── style.css           # Stili grafici per il layout (container, card, bottoni)
└── templates/
    ├── index.html          # Home page (Sezione immagini e link al Pokedex)
    └── pokedex.html        # Pagina dedicata alla ricerca e visualizzazione dei Pokémon