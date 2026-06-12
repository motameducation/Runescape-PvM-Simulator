# this program is about creating a simple RPG game using OOP - it is a dumbed down version of Runescape
# this game will ask for equipment, player stats and the enemy's stats- it will compute the optimal rotation (that which deals the most damage). 
import math
import random

class AbilityHit:
    def __init__(self,min_pct: float,max_pct: float, delay_ticks: int = 0,crit_chance_bonus: float=0.0,crit_dmg_bonus: float=0.0,guaranteed_crit: bool = False, is_channeled_hit: bool = False):
        self.min_pct = min_pct
        self.max_pct = max_pct
        self.delay_ticks = delay_ticks
        self.crit_chance_bonus = crit_chance_bonus
        self.crit_dmg_bonus = crit_dmg_bonus
        self.guaranteed_crit = guaranteed_crit
        self.is_channeled_hit = is_channeled_hit
class Ability:
    def __init__(self, name: str, adren_cost: int, cooldown: int, is_channeled: bool = False):
        self.name = name
        self.adren_cost = adren_cost    # Positive for drain (e.g., -15), negative for gain (e.g., +8)
        self.cooldown_max = cooldown
        self.is_channeled = is_channeled
        # State variables (reset before each rotation simulation)
        self.current_cooldown = 0

    def is_ready(self):
        return self.current_cooldown == 0

    def tick_cooldown(self, ticks: int=1):
        self.current_cooldown = max(0,self.current_cooldown - ticks)
    def get_hits(self,player) ->list[AbilityHit]:
        """To be overriden by subclasses"""
        return []
    def apply_on_cast_effects(self,player,simulator):
        """Hook for abilities that apply buffs immediately e.g. sonic wave"""
        pass
    def apply_on_complete_effects(self,player,simulator):
        """Hook for abilities that apply effects after channelling e.g. Asphyxiate"""
        pass
class Player:
    def __init__(self, magic_level: int = 145, weapon_tier: int = 100, weapon_name: str = "FSoA",equip_magic_bonus: float = 255.3, ring: str = "Channelers", aspect: str = "Temporal Anomaly",perks: dict = None, relics:list = None, onTask: bool = False,armourset: str = "Elite Tectonic",hit_chance: float = 1.0):
        self.magic_level = magic_level
        self.weapon_tier = weapon_tier
        self.equip_magic_bonus = equip_magic_bonus
        self.perks = perks if perks else {"Precise":6,"Aftershock":4,"Biting":4,"Undead Slayer":1,"Impatient":4,"Crackling":4,"Ultimatums":4}
        self.relics = relics if relics else ["CoE","FotS"]
        self.aspect = aspect
        
        # In a full build, equipment would be its own class that modifies these stats
        self.active_buffs = ["Grimoire","Affliction","Vulnerability","Smoke Cloud","Soulsplit","Essence Corruption","RoV","Kalg"]
        if onTask:
            self.active_buffs.append("On Task")
        self.adrenaline = 100
    def get_base_ability_damage(self) -> float:
        f_M = 145 * math.log(1+0.6*(self.magic_level/145))/math.log(1.6)
        b = self.equip_magic_bonus
        t = self.weapon_tier
        term1 = math.floor(2.5*f_M)
        term2 = math.floor(1.25*f_M)
        term3 = math.floor(14.4*t + 1.5*b)
        return term1 + term2 + term3
    def get_crit_chance(self,hit: AbilityHit,channel_hit_index: int = 0) -> float:
        # Example: Biting perk or Grimoire would add to this
        chance = 0.1
        if "Grimoire" in self.active_buffs:
            chance +=0.12
        else:
            chance += 0.07
        if "Biting" in self.perks.keys():
            chance += self.perks["Biting"] * 0.02
        if "Elite Tectonic" in self.armourset:
            chance += 0.06
        if "Kalg" in self.active_buffs:
            chance += 0.06
        if self.ring == "Channelers" and hit.is_channeled_hit:
            chance += 0.04 * channel_hit_index
        return chance

    def get_crit_modifier(self,hit: AbilityHit,channel_hit_index: int = 0) -> float:
        base_crit_mod = 1.5
        if "Smoke Cloud" in self.active_buffs:
            base_crit_mod += 0.15
        if self.weapon_name == "FSoA":
            base_crit_mod += random.uniform(0.15,0.25)
        if self.ring == "Channelers" and hit.is_channeled_hit:
            base_crit_mod += 0.025 * channel_hit_index
        return base_crit_mod

    def calculate_mean_damage(self, ability: Ability) -> float:
        """Calculates expected average damage mathematically."""
        crit_chance = self.get_crit_chance()
        crit_mod = self.get_crit_modifier()
        
        # Mean = (Normal Hit Chance * Base) + (Crit Chance * Base * Crit Modifier)
        expected_multiplier = (1 - crit_chance) * 1.0 + (crit_chance * crit_mod)
        
        # Factor in active buffs like Sunshine (+50% magic damage)
        buff_multiplier = 1.5 if "Sunshine" in self.active_buffs else 1.0
        
        return ability.base_damage * expected_multiplier * buff_multiplier

    def roll_real_damage(self, ability: Ability) -> float:
        """Simulates an actual hit with RNG."""
        buff_multiplier = 1.5 if "Sunshine" in self.active_buffs else 1.0
        
        is_crit = random.random() < self.get_crit_chance()
        if is_crit:
            return ability.base_damage * self.get_crit_modifier() * buff_multiplier
        else:
            # RS damage usually rolls between roughly 20% and 100% of the max base hit
            rng_variance = random.uniform(0.2, 1.0) 
            return ability.base_damage * rng_variance * buff_multiplier

class Boss:
    def __init__(self, health: int,name: str):
        self.health = health
        self.max_health = health
        self.name = name

class GreaterConcentratedBlast(Ability):
    def __init__(self):
        super().__init__("Greater Concentrated Blast", adren_cost=-9,cooldown = 9,is_channeled=True)
    def get_hits(self,player) -> list[AbilityHit]:
        bonus_crit = 0.10 if "Anima Charged" in player.active_buffs else 0.0
        return [AbilityHit(0.40,0.50,delay_ticks=0,crit_chance_bonus=bonus_crit,is_channeled_hit=True),
                AbilityHit(0.40,0.50,delay_ticks=1,crit_chance_bonus=bonus_crit+0.07,is_channeled_hit=True),
                AbilityHit(0.40,0.50,delay_ticks=2,crit_chance_bonus=bonus_crit+0.14,is_channeled_hit=True)]

class Asphyxiate(Ability):
    def __init__(self):
        super().__init__("Asphyxiate", adren_cost=25,cooldown = 34,is_channeled=True)
    def get_hits(self,player) -> list[AbilityHit]:
        if player.armourset = "Tumeken":
            return [AbilityHit(0.72,0.84,delay_ticks=i,is_channelled_hit=True) for i in range(8)]
        return [AbilityHit(1.20,1.40,delay_ticks=i*2,is_channelled_hit=True) for i in range(4)]
class SmokeTendrils(Ability):
    def __init__(self):
        super().__init__("Smoke Tendrils", adren_cost=0, cooldown=75, is_channelled=True)
        
    def get_hits(self, player) -> list[AbilityHit]:
        hits = []
        base_min, base_max = 0.55, 0.65
        for i in range(4):
            # 1.2s = 2 game ticks between hits. Damage scales +10-15% per hit.
            hits.append(AbilityHit(
                min_pct=base_min + (i * 0.10), 
                max_pct=base_max + (i * 0.15), 
                delay_ticks=i * 2, 
                guaranteed_crit=True, 
                is_channelled_hit=True
            ))
        return hits
class FSoASpecial(Ability):
    def __init__(self):
        super().__init__("Instability",adren_cost=50,cooldown=100)
    def get_hits(self,player):
        return [AbilityHit(1.20,1.40,delay_ticks=0)]
    def apply_on_cast_effects(self,player,simulator):
        # adjust adrenaline of RoV is active
        if "RoV" in player.active_buffs:
            player.adrenaline += 5
        simulator.add_buff("Instability",duration_ticks=50)


class PendingHit:
    def __init__(self,ability_name: str, hit:AbilityHit, tick_to_land: int, channel_index: int = 0, is_lightning_surge: bool = False):
        self.ability_name = ability_name
        self.hit = hit
        self.tick_to_land = tick_to_land
        self.channel_index = channel_index
        self.is_lightning_surge = is_lightning_surge

class RotationSimulator:
    def __init__(self,player: Player, abilities: dict):
        self.player = player
        self.abilities = abilities
        self.time_ticks = 0
        self.total_damage = 0

        # Engine State
        self.pending_hits = []
        self.active_buffs_timer = {}
        self.aftershock_damage_pool = 0

    def add_buff(self,buff_name: str,duration_ticks: int,effect_val: float=0):
        self.active_buffs_timer[buff_name] = duration_ticks
        if buff_name not in self.player.active_buffs:
            self.player.active_buffs.append(buff_name)

    def process_tick(self):
        """Processes a single game tick, resolving damage and timers."""
        #1. Process Hits landing on this tick
        
        hits_this_tick = [h for h in self.pending_hits if h.tick_to_land == self.time_ticks]
        self.pending_hits = [h for h in self.pending_hits if h.tick_to_land > self.time_ticks]
        
        for p_hit in hits_this_tick:
            self.resolve_hit(p_hit)

        # 2. Process buff decay
        for buff in list(self.active_buffs_timer.keys()):
            self.active_buffs_timer[buff] -= 1
            if self.active_buffs_timer[buff] <= 0:
                del self.active_buffs_timer[buff]
                self.player.active_buffs.remove(buff)
        # 3. Advance cooldowns
        for ab in self.abilities.values():
            ab.tick_cooldown(1)
        self.time_ticks += 1

    def resolve_hit(self,p_hit: PendingHit):
        base_ad = self.player.get_base_ability_damage()

        #Apply Precise
        min_pct = p_hit.hit.min_pct
        if "Precise" in self.player.perks.keys():
            min_pct += (p_hit.hit.max_pct *0.015 *self.player.perks["Precise"])

        is_crit = p_hit.hit.guaranteed_crit or (random.random() < self.player.get_crit_chance(p_hit.hit,p_hit.channel_index))
        if is_crit:
            dmg = (base_ad * p_hit.hit.max_pct) *self.player.get_crit_modifier(p_hit.hit,p_hit.channel_index)

            if "Instability" in self.player.active_buffs and not p_hit.is_lightning_surge:
                lightning_hit = AbilityHit(0.70,0.90)
                # Lands 1 tick after the source hit
                self.pending_hits.append(PendingHit("Lightning Surge", lightning_hit,self.time_ticks+1,is_lightning_surge=True))
        else:
            dmg = base_ad * random.uniform(min_pct,p_hit.hit.max_pct)
        self.total_damage += dmg
        self.track_aftershock(dmg)

    def track_aftershock(self,damage: float):
        if "Aftershock" not in self.player.perks: return
        self.aftershock_damage_pool += damage
        if self.aftershock_damage_pool >= 50000:
            procs = int(self.aftershock_damage_pool // 50000)
            self.aftershock_damage_pool %= 50000
        rank = self.player.perks["Aftershock"]
        for _ in range(procs):
            as_hit = AbilityHit(0.24*rank,0.396*rank)
            self.pending_hits.append(PendingHit("Aftershock Proc",as_hit,self.time_ticks))
# Next steps: add the remaining magic abilities: greater sunshine, tsunami, omnipower, magma tempest, runic charge, greater chain, impact, combust, dragonbreath, corruption blast and basic attack,  add RoA special, add logic for spells: incite fear, exsang and crumble undead.
# Next next steps: add logic for damage modifiers: affliction, vulnerability, tokkul-zo, genocidal, eruptive, essence corruption buff,  conflagrate, kerapac's wristwraps, corrupted slayer helmet, crackling,impatient, ultimatums,
# salve amulet (e), undead slayer ability and undead slayer perk.
# Future steps: add boss dmg, boss hit chance, add boss and Rotation Simulator classes to a PvMSimulator class. Include boss mechanics and defensive abilities to handle them. Logic for hit chance calculation.
# Far away future steps: add necromancy abilities and conjures.