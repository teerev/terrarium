# Terrarium

Terrarium is a small, deterministic simulation sandbox with snapshot/replay export utilities.

## Replay format

The replay JSON format is documented in `docs/replay-format.md`.

- Export: `terrarium.io.export_replay(sim, path)`
- Schema model: `terrarium.io.ReplaySchema`
- Validation: `terrarium.io.validate_replay(data)`
