# Vattenfall Tijdprijs

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/max1weber/ha-addon-vattenfall-tijdprijs-trend.svg)](https://github.com/max1weber/ha-addon-vattenfall-tijdprijs-trend/releases)
[![License](https://img.shields.io/github/license/max1weber/ha-addon-vattenfall-tijdprijs-trend.svg)](LICENSE)

Home Assistant integratie voor Vattenfall TijdPrijs dynamische energieprijzen.

[English version below](#english-version)

---

## 🇳🇱 Nederlandse Versie

### Functies

Deze integratie biedt geavanceerde energieprijsberekening voor Vattenfall TijdPrijs met ondersteuning voor:

- **Tijdsgebonden Tarieven** - Verschillende tarieven voor zomer/winter en normale/dal perioden
- **Verbruikstiers** - Aangepaste prijzen op basis van jaarlijks verbruik (0-2900, 2900-10000, 10000-50000, 50000+ kWh)
- **Vaste Kosten** - Dagelijkse vaste leveringskosten, systeembeheerkosten en belastingvermindering
- **Teruglever Tarieven** - Vergoeding en kosten voor teruggeleverde stroom
- **Sensorintegratie** - Automatische verbruikstracking via Home Assistant sensoren

### Prijsberekening

De integratie berekent energieprijzen op basis van:
- Zomer/winter seizoen (april-september = zomer, oktober-maart = winter)
- Dagtijden (normaal, dal doordeweeks, dal weekend)
- Jaarlijks verbruik (bepaalt het tarieftier)
- Energiebelasting + leveringstarieven (beide inclusief 21% BTW)

### Standaardwaarden

Alle configuratievelden hebben redelijke standaardwaarden vooraf ingesteld:
- Zomer: 0,115 €/kWh (normaal), 0,018 €/kWh (dal), 0,000 €/kWh (weekend dal)
- Winter: 0,141 €/kWh (normaal), 0,087 €/kWh (dal dag), 0,071 €/kWh (dal nacht)
- Vaste kosten: 0,296 €/dag (levering), -1,723 €/dag (belastingvermindering), 1,304 €/dag (systeembeheer)

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

De configuratiewizard begeleidt je door de volgende stappen:

1. **Jaarverbruik** - Voer uw geschatte jaarlijks verbruik in (bepaalt het tarieftier) of link een bestaande sensor
2. **Vaste Kosten** - Configureer dagelijkse vaste kosten (standaardwaarden zijn vooraf ingevuld)
3. **Leveringstarieven** (optioneel) - Pas de leveringstarieven aan voor elke periode/tier of gebruik standaardwaarden
4. **Teruglever Tarieven** - Stel de vergoeding en kosten voor teruggeleverde stroom in

Alle velden hebben standaardwaarden, dus je kunt de configuratie direct voltooien of afzonderlijke velden aanpassen.

### Geëxporteerde Sensoren

Na configuratie zijn de volgende entiteiten beschikbaar in Home Assistant:

- `sensor.vattenfall_tijdprijs_*_importprijs` - Huidige importprijs (€/kWh)
- `sensor.vattenfall_tijdprijs_*_terugleververgoeding` - Teruglever vergoeding (€/kWh)
- `sensor.vattenfall_tijdprijs_*_terugleverkosten` - Teruglever kosten (€/kWh)
- `sensor.vattenfall_tijdprijs_*_vaste_leveringskosten` - Dagelijkse vaste leveringskosten (€/dag)
- `sensor.vattenfall_tijdprijs_*_vaste_netbeheerkosten` - Dagelijkse systeembeheerkosten (€/dag)
- `sensor.vattenfall_tijdprijs_*_vaste_terugleverkosten` - Dagelijkse teruglever vaste kosten (€/dag)

### Gebruik in Automatiseringen

Voorbeeld om apparaten te schakelen op basis van de stroomprijs:

```yaml
automation:
  - alias: "Boiler aan bij lage prijs"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vattenfall_tijdprijs_importprijs
        below: 0.20
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

Home Assistant integration for Vattenfall TijdPrijs dynamic energy pricing with time-of-use rates and consumption-based pricing tiers.

### Features

This integration provides advanced energy price calculations with:

- **Time-of-Use Pricing** - Different rates for summer/winter and normal/off-peak periods
- **Consumption Tiers** - Custom pricing based on annual consumption (0-2900, 2900-10000, 10000-50000, 50000+ kWh)
- **Fixed Costs** - Daily fixed delivery costs, grid management costs, and tax reductions
- **Export Pricing** - Compensation and costs for exported electricity
- **Sensor Integration** - Automatic consumption tracking via Home Assistant sensors

### Price Calculation

The integration calculates energy prices based on:
- Season (summer: April-September, winter: October-March)
- Time of day (normal, off-peak weekday, off-peak weekend)
- Annual consumption (determines your pricing tier)
- Energy tax + delivery rates (both including 21% VAT)

### Default Values

All configuration fields come with reasonable default values pre-filled:
- Summer: 0.115 €/kWh (normal), 0.018 €/kWh (off-peak), 0.000 €/kWh (weekend off-peak)
- Winter: 0.141 €/kWh (normal), 0.087 €/kWh (off-peak day), 0.071 €/kWh (off-peak night)
- Fixed costs: 0.296 €/day (delivery), -1.723 €/day (tax reduction), 1.304 €/day (grid management)

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

The configuration wizard guides you through the following steps:

1. **Annual Consumption** - Enter your estimated annual consumption (determines pricing tier) or link an existing sensor
2. **Fixed Costs** - Configure daily fixed costs (default values are pre-filled)
3. **Delivery Rates** (optional) - Customize delivery rates for each period/tier or use standard rates
4. **Export Rates** - Set compensation and costs for exported electricity

All fields have default values, so you can complete the configuration immediately or adjust individual fields as needed.

### Use in Automations

Example to control devices based on electricity price:

```yaml
automation:
  - alias: "Turn on water heater at low price"
    trigger:
      - platform: numeric_state
        entity_id: sensor.vattenfall_tijdprijs_importprijs
        below: 0.20
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

### Exported Sensors

After configuration, the following entities are available in Home Assistant:

- `sensor.vattenfall_tijdprijs_*_importprijs` - Current import price (€/kWh)
- `sensor.vattenfall_tijdprijs_*_terugleververgoeding` - Export compensation (€/kWh)
- `sensor.vattenfall_tijdprijs_*_terugleverkosten` - Export costs (€/kWh)
- `sensor.vattenfall_tijdprijs_*_vaste_leveringskosten` - Daily fixed delivery costs (€/day)
- `sensor.vattenfall_tijdprijs_*_vaste_netbeheerkosten` - Daily grid management costs (€/day)
- `sensor.vattenfall_tijdprijs_*_vaste_terugleverkosten` - Daily fixed export costs (€/day)

### Energy Dashboard Integration

These sensors can be used in the Home Assistant Energy Dashboard to track your energy costs.

### Support

For questions and issues, use the [GitHub issue tracker](https://github.com/max1weber/ha-addon-vattenfall-tijdprijs-trend/issues).

### License

This project is licensed under **GNU AGPL v3**. Any deployed modifications must publish their source code.
