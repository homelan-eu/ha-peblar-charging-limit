# homelan.eu Peblar Charging Limit

A small Home Assistant custom integration that adds the **user-defined charging
limit** of a Peblar EV charger as a slider (in amperes). This is the limit shown
at the top of the charger's *Smart Charging* page.

It builds on the built-in [Peblar integration](https://www.home-assistant.io/integrations/peblar/)
and reuses its logged-in connection, so it needs **no credentials or settings**
of its own. It is meant as a stopgap until the built-in integration offers this
setting itself (see [discussion #5491](https://github.com/orgs/home-assistant/discussions/5491)).

> Nederlandstalig? Zie [onderaan](#nederlands).

## Features

- Number entity `User charge limit (homelan.eu)` on your existing Peblar device.
- Range from 6 A up to the lower of the charger's hardware rating and the
  installation's fixed current limit.
- Unavailable when the charger does not allow changing the limit.
- Reloads itself when the built-in Peblar integration reloads.

## Requirements

- Home Assistant 2026.11 or newer (tested on 2026.11.1).
- The built-in Peblar integration, set up and loaded.

## Installation

### HACS (custom repository)

1. In HACS, open the menu (⋮) → **Custom repositories**.
2. Add `https://github.com/homelan-eu/ha-peblar-charging-limit` with type **Integration**.
3. Install **homelan.eu Peblar Charging Limit** and restart Home Assistant.

### Manual

1. Copy `custom_components/homelan_peblar_charging_limit` into the
   `custom_components` folder of your Home Assistant configuration.
2. Restart Home Assistant.

### Set up

**Settings → Devices & services → Add integration →
homelan.eu Peblar Charging Limit**, then confirm.

## Important

- This integration reads **internal parts of the built-in Peblar integration**,
  not a public API. A Home Assistant update may break it. When that happens it
  stops with a clear error message instead of failing repeatedly.
- It changes the charging current of a real charger. Use at your own risk.
- Not affiliated with or endorsed by Peblar or Home Assistant.

## License

[MIT](LICENSE)

---

## Nederlands

Een kleine custom integration voor Home Assistant die de **door de gebruiker
ingestelde laadlimiet** van een Peblar-laadpaal als schuifregelaar (in ampère)
toevoegt. Dit is de limiet bovenaan de *Smart Charging*-pagina van de lader.

De integratie gebruikt de verbinding van de ingebouwde Peblar-integratie en
heeft dus geen eigen inloggegevens of instellingen nodig. Installeren gaat via
HACS (custom repository) of door de map `custom_components/homelan_peblar_charging_limit`
handmatig te kopiëren; daarna Home Assistant herstarten en de integratie
toevoegen via **Instellingen → Apparaten & diensten**.

Let op: de integratie leunt op interne onderdelen van de ingebouwde
Peblar-integratie en kan na een Home Assistant-update stoppen met werken.
Gebruik op eigen risico; niet verbonden aan Peblar of Home Assistant.
