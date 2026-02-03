from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.death import DeathRule
from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.entities.organism import Organism
from terrarium.events.emitter import EventEmitter, EventLog
from terrarium.events.schema import BirthEvent, DeathCause, DeathEvent
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_reproduction_emits_birth_event_with_expected_payload() -> None:
    world = WorldState(Grid(5, 5), seed=123)

    # tick should be captured at time of event
    assert world.tick == 0

    rng = SeededRNG(999)
    parent = Organism(position=Position(1, 2), energy=40, rng=rng)
    world.add_entity(parent)

    emitter = EventEmitter()
    log = EventLog()
    emitter.subscribe(log)

    rule = ReproductionRule(reproduction_cost_override=None)
    offspring = rule.apply(world, rng, emitter=emitter)

    assert len(offspring) == 1
    child = offspring[0]

    assert len(log.events) == 1
    evt = log.events[0]
    assert isinstance(evt, BirthEvent)

    assert evt.tick == world.tick
    assert evt.parent_id == parent.id
    assert evt.offspring_id == child.id
    assert dict(evt.genome) == child.genome.to_dict()
    assert evt.position == child.position
    assert evt.offspring_energy == int(child.energy)


def test_death_emits_death_event_before_removal_with_final_state() -> None:
    world = WorldState(Grid(5, 5), seed=123)

    rng = SeededRNG(999)
    org = Organism(position=Position(0, 0), energy=1, rng=rng)
    world.add_entity(org)

    # Set to zero to trigger death rule.
    org.energy = 0

    emitter = EventEmitter()
    log = EventLog()
    emitter.subscribe(log)

    removed = DeathRule().apply(world, emitter=emitter)

    assert removed == [org.id]
    assert world.get_entity(org.id) is None

    assert len(log.events) == 1
    evt = log.events[0]
    assert isinstance(evt, DeathEvent)

    assert evt.tick == world.tick
    assert evt.organism_id == org.id
    assert evt.cause == DeathCause.STARVATION
    assert evt.final_energy == 0
