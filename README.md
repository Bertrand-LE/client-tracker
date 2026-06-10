# Client Tracker

Lokale tijdregistratie-app voor klanten en interventies.

## Installatie

1. **Zorg dat Python 3.8+ geïnstalleerd is.**

2. Installeer de afhankelijkheden:
   ```bash
   pip install flask
   ```

## Opstarten

```bash
python app.py
```

De browser opent automatisch op [http://localhost:5000](http://localhost:5000).

## Functies

- **Dashboard** — interventies van de huidige maand, meest recent eerst
- **Klanten** — klanten toevoegen, bewerken en verwijderen
- **Registreren** — nieuwe interventie loggen (klant, datum, type, duur, titel, notities)
- **Maandoverzicht** — filter per maand/jaar, gegroepeerd per klant, export naar CSV

## Gegevens

De SQLite-database wordt opgeslagen in `data/tracker.db` (staat in `.gitignore`).
