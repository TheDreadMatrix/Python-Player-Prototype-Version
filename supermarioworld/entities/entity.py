from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Set, Tuple, Type, TypeVar

import pygame


TComp = TypeVar("TComp")


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Velocity:
    x: float = 0.0
    y: float = 0.0


@dataclass
class Health:
    hp: int


@dataclass
class Gravity:
    value: float = 980.0


@dataclass
class Hitbox:
    w: float
    h: float


@dataclass
class PlayerInput:
    speed: float = 180.0


class Entity:
    """Lightweight handle around entity id."""

    def __init__(self, world: "World", entity_id: int):
        self.world = world
        self.entity_id = entity_id

    def add(self, component: object) -> "Entity":
        self.world.add_component(self.entity_id, component)
        return self

    def get(self, comp_type: Type[TComp]) -> Optional[TComp]:
        return self.world.get_component(self.entity_id, comp_type)

    def has(self, *comp_types: Type[object]) -> bool:
        return self.world.has_components(self.entity_id, *comp_types)

    def remove(self, comp_type: Type[object]) -> None:
        self.world.remove_component(self.entity_id, comp_type)


class World:
    def __init__(self):
        self._next_id = 1
        self._entities: Set[int] = set()
        self._components: Dict[Type[object], Dict[int, object]] = {}

    def create_entity(self) -> Entity:
        entity_id = self._next_id
        self._next_id += 1
        self._entities.add(entity_id)
        return Entity(self, entity_id)

    def add_component(self, entity_id: int, component: object) -> None:
        self._components.setdefault(type(component), {})[entity_id] = component

    def get_component(self, entity_id: int, comp_type: Type[TComp]) -> Optional[TComp]:
        comp_map = self._components.get(comp_type)
        if not comp_map:
            return None
        return comp_map.get(entity_id)  # type: ignore[return-value]

    def remove_component(self, entity_id: int, comp_type: Type[object]) -> None:
        comp_map = self._components.get(comp_type)
        if comp_map:
            comp_map.pop(entity_id, None)

    def has_components(self, entity_id: int, *comp_types: Type[object]) -> bool:
        return all(entity_id in self._components.get(comp_type, {}) for comp_type in comp_types)

    def query(self, *comp_types: Type[object]) -> Iterable[Tuple[int, ...]]:
        if not comp_types:
            return []

        first_map = self._components.get(comp_types[0], {})
        if not first_map:
            return []

        entity_ids = set(first_map.keys())
        for comp_type in comp_types[1:]:
            entity_ids &= set(self._components.get(comp_type, {}).keys())

        result = []
        for entity_id in entity_ids:
            row = [entity_id]
            for comp_type in comp_types:
                row.append(self._components[comp_type][entity_id])
            result.append(tuple(row))
        return result


class InputSystem:
    """Reads WASD and writes horizontal velocity for player entities."""

    def update(self, world: World, dt: float) -> None:
        keys = pygame.key.get_pressed()
        horizontal = 0
        if keys[pygame.K_a]:
            horizontal -= 1
        if keys[pygame.K_d]:
            horizontal += 1

        for _, vel, player_input in world.query(Velocity, PlayerInput):
            vel.x = horizontal * player_input.speed


class PhysicsSystem:
    def update(self, world: World, dt: float) -> None:
        for _, pos, vel in world.query(Position, Velocity):
            pos.x += vel.x * dt
            pos.y += vel.y * dt


class GravitySystem:
    def update(self, world: World, dt: float) -> None:
        for _, vel, gravity in world.query(Velocity, Gravity):
            vel.y += gravity.value * dt


def create_player(world: World, x: float, y: float) -> Entity:
    return (
        world.create_entity()
        .add(Position(x=x, y=y))
        .add(Velocity())
        .add(Hitbox(w=16, h=32))
        .add(Health(hp=3))
        .add(Gravity(980.0))
        .add(PlayerInput(speed=180.0))
    )
