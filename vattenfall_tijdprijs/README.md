# Vattenfall Tijdprijs

Home Assistant integratie voor Vattenfall TijdPrijs Trend energieprijzen.

## Features
- Dynamische importprijs
- Terugleververgoeding
- Terugleverkosten
- Vaste leveringskosten
- Vaste netbeheerkosten
- Vaste terugleverkosten

## BTW
Alle prijzen zijn **inclusief 21% btw** en bedoeld voor particuliere gebruikers.

## Installatie

### Via HACS (Aanbevolen)
1. Open HACS in Home Assistant
2. Ga naar "Integrations"
3. Klik op de drie stippen rechtsboven
4. Kies "Custom repositories"
5. Voeg deze URL toe: `https://github.com/max1weber/ha-addon-vattenfall-tijdprijs-trend`
6. Selecteer "Integration" als categorie
7. Klik op "Add"
8. Zoek naar "Vattenfall Tijdprijs" en installeer
9. Herstart Home Assistant

### Handmatig
1. Kopieer de map `custom_components/vattenfall_tijdprijs` naar je Home Assistant `custom_components` map
2. Herstart Home Assistant

## Configuratie

1. Ga naar Instellingen → Apparaten & Services
2. Klik op "Integratie toevoegen"
3. Zoek naar "Vattenfall Tijdprijs"
4. Voer je prijzen in (in €/kWh voor variabele prijzen, €/dag voor vaste kosten)

## Sensoren

De integratie maakt de volgende sensoren aan:

| Sensor | Eenheid | Beschrijving |
|--------|---------|--------------|
| Import prijs | €/kWh | Dynamische prijs voor stroomverbruik |
| Terugleververgoeding | €/kWh | Vergoeding voor teruggeleverde stroom |
| Terugleverkosten | €/kWh | Kosten voor het terugleveren |
| Vaste leveringskosten | €/dag | Dagelijkse vaste kosten voor levering |
| Vaste netbeheerkosten | €/dag | Dagelijkse netbeheerkosten |
| Vaste terugleverkosten | €/dag | Dagelijkse vaste kosten teruglevering |

## Gebruik in automatiseringen

Voorbeeld om apparaten te schakelen op basis van de stroomprijs:

```yaml
automation:
  - alias: "Boiler aan bij lage prijs"
    trigger:
      - platform: numeric_state
        entity_id: sensor.import_prijs
        below: 0.15
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.boiler
```

## Support

Voor vragen en problemen, gebruik de [GitHub issue tracker](https://github.com/max1weber/ha-addon-vattenfall-tijdprijs-trend/issues).


## License
This project is licensed under the **GNU AGPL v3**.

Any deployed modification must publish its source code.
