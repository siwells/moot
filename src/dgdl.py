import exceptions

class System:
    """
    A Dialogue System composed from one or more games
    """
    def __init__(self, name):
        self.name = name
        self.games = []

    def add_game(self, game):
        self.games.append(game)

class Game:
    """
    A Game composed from a composition, zero or more regulations, and at least one interaction
    """
    def __init__(self, name, comp, regulations=[], moves=[]):
        self.name = name
        self.comp = comp
        self.regulations = regulations
        self.moves = moves

    def fragment(self):
        fragments = []
        fragments.append(self.name)
        fragments.append("{")
        fragments.append(self.comp.fragment())
        if len(self.regulations) != 0:
            fragments.append(", {")
            fragments.append(', '.join( reg.fragment() for reg in self.regulations ))
            fragments.append("}")
        fragments.append("}")
        if len(self.moves) != 0:
            fragments.append(", {")
            fragments.append(', '.join( move.fragment() for move in self.moves ))
            fragments.append("}")
        fragments.append("}")
        return ''.join(fragments)

class Composition:
    """
    A Composition defines the components of the game such as the board and pieces
    """
    def __init__(self, turns, participants, players=[], stores=[], rolelist=None):
        self.turns = turns
        self.participants = participants
        self.players = players
        self.stores = stores
        self.rolelist = rolelist

    def fragment(self):
        fragments = []
        fragments.append(self.turns.fragment())
        fragments.append(", ")
        if self.rolelist is not None:
            fragments.append(self.turns.fragment())
        fragments.append(", ")
        fragments.append(self.participants.fragment())
        for player in self.players:
            fragments.append(", ")
            fragments.append(player.fragment())
        for store in self.stores:
            fragments.append(", ")
            fragments.append(store.fragment())
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
        opener = "{turns, magnitude:"
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
        opener = "{store, id:"
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
    def __init__(self, min=2, max=None):
        self.min = min
        self.max = max

    def fragment(self):
        fragments = []
        opener = "{players, min:"
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
        opener = "{player, id:"
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

class Regulation:
    """
    Defines a regulation associated with playing the game.

    A Regulation is a set of conditions which, if satisfied, require an effect to be performed on the state of the game. Regulations differ from interactions in that regulations should be executed whenever their conditions are met whereas interactions are only executed if a player plays the move associated with that interaction.
    
    A regulation is composed from:
        An identifier
        A scope from {initial | turnwise | movewise}
        A rule
    """
    def __init__(self, name, scope="movewise", rule=None):
        self.name = name
        self.scope = scope
        self.rule = rule

    def fragment(self):
        fragments = []
        opener = "{"
        fragments.append(opener)
        fragments.append(self.name)
        fragments.append(", scope:")
        fragments.append(self.scope)
        closer = "}"
        fragments.append(closer)
        return ''.join(fragments)

class Interaction:
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
    def __init__(self, name, content=[], opener=None, rule=None):
        self.name = name
        self.content = content
        self.opener = opener
        self.rule = rule
        
    def fragment(self):
        fragments = []
        opener = "{"
        fragments.append(opener)
        fragments.append(self.name)
        fragments.append(", {")
        fragments.append(', '.join( element for element in self.content ))
        fragments.append("}")
        closer = "}"
        if self.opener is not None:
            fragments.append(", \"")
            fragments.append(self.opener)
            fragments.append("\"")
        fragments.append(closer)
        return ''.join(fragments)
        
class Rules:
    """
    A set of Rule objects
    
    An individual Regulation or Interaction could encompass multiple sets of rules, enabling the resultant effect to differ dependent upon the circumstances in which they occur.
    """
    def __init__(self):
        pass
        
    def fragment(self):
        pass
        
class Rule:
    """
    Used to express a condition & what should happen as a result of that condition pertaining
    
    A Rule consists of a set of conditions & a set of effects. If rule is in effect and the set of conditions is met then the effects must be applied.
    """
    def __init__(self):
        self.conditions = []
        self.effects = []
        pass
    
    def fragment(self):
        pass
        
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

