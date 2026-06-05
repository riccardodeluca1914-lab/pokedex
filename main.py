from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Form
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx

from PIL import Image, UnidentifiedImageError
import io

# Creiamo l'applicazione
app = FastAPI()

# --- Configurazione HTML e CSS ---
# Diciamo a FastAPI dove trovare i file CSS (e in futuro JavaScript o immagini statiche)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Diciamo a FastAPI dove trovare i file HTML (usando Jinja2, lo stesso motore di Flask)
templates = Jinja2Templates(directory="templates")

# --- Le nostre rotte ---

@app.get("/")
async def leggi_pagina_principale(request: Request):
    # Usiamo i parametri espliciti (request, name, context) 
    # compatibili con le ultime versioni di FastAPI
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"messaggio": "Ciao! Questo è il mio progetto finale."}
    )
    # Questa rotta serve solo ad aprire la pagina vuota del Pokédex
@app.get("/pokedex/")
async def apri_pokedex(request: Request):
    return templates.TemplateResponse(request=request, name="pokedex.html", context={})


@app.post("/cerca-pokemon-web/")
async def cerca_pokemon_web(request: Request, nome_pokemon: str = Form(...)):
    
    # Il nostro traduttore super-veloce
    dizionario_tipi = {
        "normal": "Normale", "fighting": "Lotta", "flying": "Volante",
        "poison": "Veleno", "ground": "Terra", "rock": "Roccia",
        "bug": "Coleottero", "ghost": "Spettro", "steel": "Acciaio",
        "fire": "Fuoco", "water": "Acqua", "grass": "Erba",
        "electric": "Elettro", "psychic": "Psico", "ice": "Ghiaccio",
        "dragon": "Drago", "dark": "Buio", "fairy": "Folletto"
    }
    
    url_api = f"https://pokeapi.co/api/v2/pokemon/{nome_pokemon.lower()}"
    
    async with httpx.AsyncClient() as client:
        risposta = await client.get(url_api)
        
        if risposta.status_code == 404:
            return templates.TemplateResponse(
                request=request, name="pokedex.html", 
                context={"errore_api": f"Ops! Nessun Pokémon chiamato '{nome_pokemon}' trovato."}
            )
            
        dati = risposta.json()
        
        evolve_da = "Nessuno"
        evolve_in = "Nessuno"
        generazione_ita = "Sconosciuta" 
        
        try:
            species_url = dati["species"]["url"]
            risposta_specie = await client.get(species_url)
            
            if risposta_specie.status_code == 200:
                specie = risposta_specie.json()
                
                

                dizionario_numeri = {
                    "I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", 
                    "VI": "6", "VII": "7", "VIII": "8", "IX": "9", "X": "10"
                }
                
                gen_grezza = specie.get("generation", {}).get("name", "")
                if gen_grezza.startswith("generation-"):
                   
                    num_romano = gen_grezza.split("-")[1].upper()
                    
                   
                    num_arabo = dizionario_numeri.get(num_romano, num_romano)
                    
                    generazione_ita = f"Generazione {num_arabo}"
                
                
                if specie.get("evolves_from_species"):
                    evolve_da = specie["evolves_from_species"]["name"].capitalize()
                
                if specie.get("evolution_chain"):
                    chain_url = specie["evolution_chain"]["url"]
                    risposta_chain = await client.get(chain_url)
                    
                    if risposta_chain.status_code == 200:
                        chain = risposta_chain.json()
                        def cerca_evoluzioni(nodo, nome_target):
                            if nodo["species"]["name"] == nome_target:
                                return [evo["species"]["name"].capitalize() for evo in nodo.get("evolves_to", [])]
                            for evo in nodo.get("evolves_to", []):
                                risultato = cerca_evoluzioni(evo, nome_target)
                                if risultato:
                                    return risultato
                            return []
                        
                        evoluzioni = cerca_evoluzioni(chain["chain"], nome_pokemon.lower())
                        if evoluzioni:
                            evolve_in = ", ".join(evoluzioni)
        except Exception:
            pass 

        
        tipo_inglese = dati["types"][0]["type"]["name"]
        tipo_tradotto = dizionario_tipi.get(tipo_inglese, tipo_inglese.capitalize())

        

        pokemon_trovato = {
            "nome": dati["name"].capitalize(),
            "peso": dati["weight"],
            "esperienza_base": dati["base_experience"],
            "tipo_principale": tipo_tradotto,          
            "generazione": generazione_ita,   
            "foto_url": dati["sprites"]["front_default"],
            "evolve_da": evolve_da,
            "evolve_in": evolve_in
        }
    return templates.TemplateResponse(
        request=request, 
        name="pokedex.html", 
        context={"pokemon": pokemon_trovato, "generazione_ita": generazione_ita}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)    