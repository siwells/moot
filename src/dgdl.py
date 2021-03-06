import exceptions

class DescriptionFactory:
    """
    This factory [1] creates complete DGDLDescription objects from supplied descriptions, [2] scaffolds minimal game or system objects, and [3] generates standard games such as DC
    """
    def __init__(self):
        pass

    def minimal(self):
        turns = Turns()
        part = Participants()
        white = Player("white")
        comp = Composition(turns, part, [white], [])
        moves = [Move("statement", content = ["p"])]
        game = Game("dgdl_simple", comp, [], moves)
        test_desc = DGDLDescription(game)
        return test_desc
    """
    Scaffold add a little syntactic sugar to the description production process by generating an outline DGDLDescription object . The resulting description requires at least one move to be supplied using the add_move() method of the game Class in order to be a valid minimal game, otherwise the description as generated is NOT syntactically correct.
    """   
    def scaffold(self, sys_id="system1", gameid="game1", magnitude="single", ordering="strict", players=["white", "black"], rules=[], moves=[]):
        turns = Turns(magnitude, ordering)
        part = Participants(len(players), len(players))
        player_list = []
        for name in players:
            player_list.append( Player(name) )
        comp = Composition(turns, part, player_list)
        game = Game(gameid, comp, rules, moves)
        sys = System(sys_id)
        sys.add_game(game)
        desc = DGDLDescription(sys)
        return desc
        
class DGDLDescription:
    """
    A class that stores a DGDL system and provides a sugary interface to the system without needing to worry about what the system is built from, e.g. No need to deal with lower level objects such as Compositions, Rules or Moves. 
    NB. Descriptions can be altered after creation as necessary subject to a validate() check on the syntactic (& semantic?) correctness of the resulting description.
    """
    def __init__(self, system):
        self.system = system
    
    def describe(self):
        return self.system.fragment()
        
    def list_conditions(self):
        pass

    def list_effects(self):
        pass
    
    def list_games(self):
        return self.system.list_games()
    
    """
    Labels includes tokens & ids used in the game description
    """
    def list_labels(self):
        pass
    
    def list_moves(self):
        pass

    def list_params(self):
        pass
    
    def list_players(self):
        pass
    
    def list_rules(self):
        pass
    

class System:
    """
    A Dialogue System composed from one or more games
    """
    def __init__(self, name):
        self.name = name
        self.games = []

    def add_game(self, game):
        self.games.append(game)
    
    def fragment(self):
        fragments = []
        fragments.append("system:{id:")
        fragments.append(self.name)
        fragments.append(',')
        fragments.append(', '.join(game.fragment() for game in self.games))

        fragments.append("}")
        return ''.join(fragments)
    
    def list_games(self):
        game_list = []
        for game in self.games:
            game_list.append(game.get_name())
        return game_list
        
class Game:
    """
    A Game composed from a composition, zero or more rules, and at least one move
    """
    def __init__(self, name, comp, rules=[], moves=[]):
        self.name = name
        self.comp = comp
        self.rules = rules
        self.moves = moves

    def fragment(self):
        fragments = []
        fragments.append("game:{id:")
        fragments.append(self.name)
        fragments.append(", ")
        fragments.append(self.comp.fragment())
        if len(self.rules) != 0:
            fragments.append(", rules:{")
            fragments.append(', '.join( rule.fragment() for rule in self.rules ))
            fragments.append("}")
        if len(self.moves) != 0:
            fragments.append(", moves:{")
            fragments.append(', '.join( move.fragment() for move in self.moves ))
            fragments.append("}")
        fragments.append("}")
        return ''.join(fragments)
    
    def get_name(self):
        return self.name

class Composition:
    """
    A Composition defines the pieces of the game such as the board, participants, roles and tokens
    """
    def __init__(self, turns, participants, players=[], stores=[], rolelist=None):
        self.turns = turns
        self.participants = participants
        self.players = players
        self.stores = stores
        self.rolelist = rolelist

    def fragment(self):
        fragments = []
        fragments.append("composition:{")
        fragments.append(self.turns.fragment())
        if self.rolelist is not None:
            fragments.append(", ")
            fragments.append(self.rolelist.fragment())
        fragments.append(", ")
        fragments.append(self.participants.fragment())
        for player in self.players:
            fragments.append(", ")
            fragments.append(player.fragment())
        for store in self.stores:
            fragments.append(", ")
            fragments.append(store.fragment())
        fragments.append("}")
        return ''.join(fragments)

class Turns:
    """
    Defines how the progression of the game is managed

    Composed from:
        Turnsize = {single | multiple}
        Ordering = {strict | liberal}
        MaxTurns = Number [OPTIONAL]

    """
    def __init__(self, size="single", ordering="strict", max_turns=None):
        self.size = size
        self.ordering = ordering
        self.max_turns = max_turns

    def fragment(self):
        fragments = []
        opener = "turns:{magnitude:"
        fragments.append(opener)
        fragments.append(str(self.size))
        fragments.append(", ordering:")
        fragments.append(str(self.ordering))

        if self.max_turns is not None:
            fragments.append(", max:")
            fragments.append(str(self.max_turns))
        closer = "}"
        fragments.append(closer)
        return ''.join(fragments)

class Store:
    """
    Defines an artifact store.

    An example  is a commitment store in the tradition of Hamblin, but basically any collection of dialogue artifacts from the set of {content, locution, argument}, structured as a set, queue or stack and with either public or private visibility. Name parameter is a label for the store. Composed from:
        Structure = {set, queue, stack}, 
        Visibility = {public, private}
        Owners is a list of Players.

    """
    def __init__(self, name="cstore", structure="set", visibility="public", *owners):
        self.name = name
        self.structure = structure
        self.visibility = visibility
        self.owners = list(owners)

    def fragment(self):
        fragments = []
        opener = "store:{id:"
        fragments.append(opener)
        fragments.append(str(self.name))
        fragments.append(", owner:{")
        owners = ', '.join([owner.name for owner in self.owners])
        fragments.append(owners)
        fragments.append("}")
        fragments.append(", structure:")
        fragments.append(str(self.structure))
        fragments.append(", visibility:")
        fragments.append(str(self.visibility))
        closer = "}"
        fragments.append(closer)
        return ''.join(fragments)

class RoleList:
    """
    Defines a list of roles that can be assigned to players to help manage the kinds of actions
        that players can perform.
    """
    def __init__(self, *roles):
        self.roles = list(roles)

    def fragment(self):
        fragments = []
        opener = "{roles, {"
        fragments.append(opener)
        body = ', '.join(self.roles)
        fragments.append(body)
        closer = "}}"
        fragments.append(closer)
        return ''.join(fragments)

class Participants:
    """
    Defines the minimum & maximum numbers of participants
    """
    def __init__(self, min=1, max=None):
        self.min = min
        self.max = max

    def fragment(self):
        fragments = []
        opener = "players:{min:"
        fragments.append(opener)
        fragments.append(str(self.min))
        fragments.append(", max:")
        if self.max is None:
            fragments.append("undefined")
        else:
            fragments.append(str(self.max))
        closer = "}"
        fragments.append(closer)
        return ''.join(fragments)

class Player:
    """
    Defines a player
    """
    def __init__(self, name, *roles):
        self.name = name
        self.roles = list(roles)

    def fragment(self):
        fragments = []
        opener = "player:{id:"
        fragments.append(opener)
        fragments.append(self.name)
        if len(self.roles) != 0:
            fragments.append(", roles:{")
            body = ', '.join(self.roles)
            fragments.append(body)
            fragments.append("}")
        closer = "}"
        fragments.append(closer)
        return ''.join(fragments)

class Rule:
    """
    Defines a rule associated with playing the game.

    A Rule is a set of conditions which, if satisfied, require an effect to be performed on the state of the game. Rules differ from moves in that rules should be executed whenever their conditions are met whereas moves are only executed if a player plays the move associated with that move.
    
    A rule is composed from:
        An identifier
        A scope from {initial | turnwise | movewise}
        A rule
    """
    def __init__(self, name, scope="movewise", body=None):
        self.name = name
        self.scope = scope
        self.body = body

    def fragment(self):
        fragments = []
        opener = "rule:{"
        fragments.append(opener)
        fragments.append("id:")
        fragments.append(self.name)
        fragments.append(", scope:")
        fragments.append(self.scope)
        if self.body is not None:
            fragments.append(", ")
            fragments.append(self.body.fragment())
        closer = "}"
        fragments.append(closer)
        return ''.join(fragments)

class Move:
    """
    Defines individual moves of the game.
    
    Moves are used by a player to interact with the game pieces & thereby change the state of the game.
    
    Moves are composed from:
        An identifer - The UID for the move
        Content - The "propositional" content of the move, e.g. 'p', 'q', 'r', &c.
        NB. Such that identifier(content)  constitutes a basic speech act descriptor
        Opener [OPTIONAL] - A string that can be prepended to the speech act, e.g. "Is it the case that..."
        Rule - A set of requirements & effects that define when a move can be played & the effect of doing so.

    """
    def __init__(self, name, content=[], opener=None, body=None):
        self.name = name
        self.content = content
        self.opener = opener
        self.body = body
        
    def fragment(self):
        fragments = []
        opener = "move:{"
        fragments.append(opener)
        fragments.append("id:")
        fragments.append(self.name)
        fragments.append(", content:{")
        fragments.append(', '.join( element for element in self.content ))
        fragments.append("}")
        closer = "}"
        if self.opener is not None:
            fragments.append(", opener:\"")
            fragments.append(self.opener)
            fragments.append("\"")
        if self.body is not None:
            fragments.append(", ")
            fragments.append(self.body.fragment())
        fragments.append(closer)
        return ''.join(fragments)
        
class Body:
    """
    An expression made from Rule objects
    
    An individual Rule or Move could encompass multiple alternative sets of rules, enabling the resultant effect to differ dependent upon the circumstances in which they occur, i.e. if a then x else if b and c then y.
    
    Well formedness: (1) the last Rule block in the Rules list can optionally contain only effects. This gives a catch all set of effects to apply if none of the conditional elements of the Rules are satisfied and has the general form "if a then x else if b and c then y else z"; (2) The first Rule block in the Rules list can also contain only a single set of effects with no conditions. In this case we are specifying a set of mandatory effects that must be applied to the game state if this move is played regardless of whether there are any subsequent conditionals. NB. Subsequent conditionals may undo the effects of this block because of the linear manner in which effects are applied. Rules of this type have the general form "x and if b then c".
    """
    def __init__(self, body=[]):
        self.body = body
        if len(body[0].conditions) == 0:
            self.catchall = True
        else:
            self.catchall = False
        
    def fragment(self):

        fragments = []
        opener = "body:{"
        fragments.append(opener)
        if self.catchall:
            fragments.append(' and '.join( conditional.fragment() for conditional in self.body))
        else:
            fragments.append(' else '.join( conditional.fragment() for conditional in self.body))
        closer = "}"
        fragments.append(closer)
        return ''.join(fragments)
        
class Conditional:
    """
    Used to express a condition & what should happen as a result of that condition pertaining
    
    A Rule consists of a set of conditions & a set of effects. If the rule is in effect and the set of conditions is met then the effects must be applied.
    """
    def __init__(self, conditions=[], effects=[]):    
        self.conditions = conditions
        self.effects = effects
    
    def fragment(self):
        fragments = []

        if len(self.conditions) and len(self.effects) != 0:
            fragments.append("if ")
            fragments.append(self.condition_fragment())
            fragments.append(" then ")
            fragments.append(self.effects_fragment())
            return ''.join(fragments)

        elif len(self.conditions) == 0  and len(self.effects) != 0:
            fragments.append(self.effects_fragment())
            return ''.join(fragments)
            
        else:
            return ''.join(fragments)
    
    def condition_fragment(self):
        fragments = []
        cond = ' and '.join(condition.fragment() for condition in self.conditions)
        fragments.append(cond)
        return ''.join(fragments)

    def conditions_list(self):
        return self.conditions[:]

    def effects_fragment(self):
        fragments = []
        eff = ' and '.join(effect.fragment() for effect in self.effects)
        fragments.append(eff)
        return ''.join(fragments)

    def effects_list(self):
        return self.effects[:]
                
class Effect:
    """
    Defines an atomic update of the game state
    """
    def __init__(self, name, *params):
        self.name = name
        self.params = list(params)
        
    def fragment(self):
        fragments = []
        fragments.append(str(self.name))
        fragments.append("{")
        body = ', '.join(self.params)
        fragments.append(body)
        fragments.append("}")
        return ''.join(fragments)
        
class Condition:
    """
    Defines a state of the game
    """
    def __init__(self, name, *params):
        self.name = name
        self.params = list(params)
    
    def fragment(self):
        fragments = []
        fragments.append(str(self.name))
        fragments.append("{")
        body = ', '.join(self.params)
        fragments.append(body)
        fragments.append("}")
        return ''.join(fragments)

if __name__ == '__main__':
    print "Dialogue Game Description Language (DGDL)"

