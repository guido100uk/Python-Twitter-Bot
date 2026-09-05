# Home Assistant — Light Schedule & Presence Simulator

Drop-in package for Home Assistant that provides:

1. **Light schedule** — morning on, evening on, night off at times you set in the UI
2. **Presence simulator** — randomly turns lights on and off to look like someone is home

## Install

1. Copy `packages/light_schedule_presence.yaml` into your HA config folder as:

   ```text
   config/packages/light_schedule_presence.yaml
   ```

2. Enable packages in `configuration.yaml` (see `configuration_snippet.yaml`):

   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```

3. Edit the light entity IDs in the package so they match your house:

   - Group under `light:` → `Presence simulator lights`
   - Morning automation target list (`light.kitchen`, `light.hallway`)

4. Restart Home Assistant (or reload helpers, automations, scripts, and groups).

5. In **Settings → Devices & Services → Helpers**, set the schedule times, for example:

   | Helper | Suggested value |
   | --- | --- |
   | Morning lights on | `07:00` |
   | Evening lights on | `18:30` |
   | Night lights off | `23:00` |

6. Optional: add `lovelace/lights_presence_card.yaml` as a dashboard card for easy control.

## How to use

### Normal day schedule

1. Turn **on** `Light schedule`
2. Leave **Presence simulator** off
3. Lights follow morning → evening → night times

While the presence simulator is on, the schedule automations do nothing so the two modes do not fight each other.

### Presence simulator (away / vacation)

1. Turn **on** `Presence simulator`
2. Keep **Presence simulator only when away** on (default) so it runs only when `zone.home` has 0 people
3. The loop picks a random light from the group, turns it on at a random brightness for a random duration, turns it off, waits a random gap, then repeats
4. When someone returns home (or you turn the simulator off), the loop stops and the group lights turn off

Tune realism with the four number helpers (min/max minutes on and off). Wider ranges look more natural.

## Files

| Path | Purpose |
| --- | --- |
| `packages/light_schedule_presence.yaml` | Helpers, light group, scripts, automations |
| `configuration_snippet.yaml` | Packages include for `configuration.yaml` |
| `lovelace/lights_presence_card.yaml` | Optional dashboard card |

## Notes

- Replace placeholder entities (`light.living_room`, etc.) before relying on this in production; missing entities will log errors.
- The simulator uses `zone.home` person count. If you track presence differently, change those conditions to your person/group entities.
- Brightness is skipped automatically by lights that do not support it.
