# Vattenfall Tijdprijs

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/max1weber/ha-addon-vattenfall-tijdprijs-trend.svg)](https://github.com/max1weber/ha-addon-vattenfall-tijdprijs-trend/releases)
[![License](https://img.shields.io/github/license/max1weber/ha-addon-vattenfall-tijdprijs-trend.svg)](LICENSE)

Home Assistant integratie voor Vattenfall TijdPrijs dynamische energieprijzen.

[English version below](#english-version)

---

## 🇳🇱 Nederlandse Versie

### Functies

Deze integratie biedt sensoren voor:

- **Importprijs** - Dynamische prijs voor stroomverbruik (€/kWh)
- **Terugleververgoeding** - Vergoeding voor teruggeleverde stroom (€/kWh)
- **Terugleverkosten** - Kosten voor het terugleveren van stroom (€/kWh)
- **Vaste leveringskosten** - Dagelijkse vaste kosten voor levering (€/dag)
- **Vaste netbeheerkosten** - Dagelijkse netbeheerkosten (€/dag)
- **Vaste terugleverkosten** - Dagelijkse vaste kosten voor teruglevering (€/dag)

### BTW

Alle prijzen zijn **inclusief 21% BTW** en bedoeld voor particuliere gebruikers.

### Installatie

#### Via HACS (Aanbevolen)

1. Open HACS in Home Assistant
2. Ga naar "Integrations"
3. Klik op de drie stippen rechtsboven (⋮)
4. Kies "Custom repositories"
5. Voeg deze URL toe: `https://github.com/max1weber/ha-addon-vattenfall-tijdprijs-trend`
6. Selecteer "Integration" als categorie
7. Klik op "Add"
8. Zoek naar "Vattenfall Tijdprijs" en klik op "Download"
9. Herstart Home Assistant

#### Handmatige Installatie

1. Kopieer de map `custom_components/vattenfall_tijdprijs` naar je Home Assistant `config/custom_components/` map
2. Herstart Home Assistant

### Configuratie

1. Ga naar **Instellingen** → **Apparaten & Services**
2. Klik op **Integratie toevoegen** (rechtsonder)
3. Zoek naar **Vattenfall Tijdprijs**
4. Voer de tarieven in:
   - Alle velden hebben standaardwaarden die je kunt aanpassen
   - Variabele prijzen in €/kWh
   - Vaste kosten in €/dag

### Gebruik in Automatiseringen

Voorbeeld om apparaten te schakelen op basis van de stroomprijs:

```yaml
automation:
  - alias: "Boiler aan bij lage prijs"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vattenfall_tijdprijs_importprijs
        below: 0.15
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.boiler

  - alias: "Wasmachine uitstellen bij hoge prijs"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vattenfall_tijdprijs_importprijs
        above: 0.40
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.wasmachine
```

### Energy Dashboard Integratie

Deze sensoren kunnen gebruikt worden in het Home Assistant Energy Dashboard om je energiekosten bij te houden.

### Support

Voor vragen en problemen, gebruik de [GitHub issue tracker](https://github.com/max1weber/ha-addon-vattenfall-tijdprijs-trend/issues).

### Licentie

Dit project is gelicenseerd onder **GNU AGPL v3**. Eventuele aanpassingen moeten openbaar worden gemaakt.

---

## 🇬🇧 English Version

Home Assistant integration for Vattenfall TijdPrijs dynamic energy pricing.

### Features

This integration provides sensors for:

- **Import Price** - Dynamic price for electricity consumption (€/kWh)
- **Export Compensation** - Compensation for exported electricity (€/kWh)
- **Export Costs** - Costs for exporting electricity (€/kWh)
- **Fixed Delivery Costs** - Daily fixed delivery costs (€/day)
- **Fixed Grid Costs** - Daily fixed grid costs (€/day)
- **Fixed Export Costs** - Daily fixed export costs (€/day)

### VAT

All prices are **VAT included (21%)** and intended for residential users.

### Installation

#### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right (⋮)
4. Select "Custom repositories"
5. Add this URL: `https://github.com/max1weber/ha-addon-vattenfall-tijdprijs-trend`
6. Select "Integration" as category
7. Click "Add"
8. Search for "Vattenfall Tijdprijs" and click "Download"
9. Restart Home Assistant

#### Manual Installation

1. Copy the `custom_components/vattenfall_tijdprijs` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

### Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration** (bottom right)
3. Search for **Vattenfall Tijdprijs**
4. Enter your tariffs:
   - All fields have default values that you can adjust
   - Variable prices in €/kWh
   - Fixed costs in €/day

### Use in Automations

Example to control devices based on electricity price:

```yaml
automation:
  - alias: "Turn on water heater at low price"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vattenfall_tijdprijs_importprijs
        below: 0.15
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.water_heater

  - alias: "Postpone washing machine at high price"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vattenfall_tijdprijs_importprijs
        above: 0.40
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.washing_machine
```

### Energy Dashboard Integration

These sensors can be used in the Home Assistant Energy Dashboard to track your energy costs.

### Support

For questions and issues, use the [GitHub issue tracker](https://github.com/max1weber/ha-addon-vattenfall-tijdprijs-trend/issues).

### License

This project is licensed under **GNU AGPL v3**. Any deployed modifications must publish their source code.
