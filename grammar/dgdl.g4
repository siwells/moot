grammar dgdl;

// Game ::= game:{id:ID, Composition [,Regulations]? Interactions}
game: GAME COLON LBRA ID COLON identifier COMMA composition (COMMA regulations)? COMMA interactions RBRA EOF;

// ID ::= UChar|LChar[UChar|LChar|Num|Link]*
identifier: UCHAR(UCHAR|LCHAR|NUM|LINK)*;

// Composition ::= {Turns, Participants [,Player]+ [,Store]* [,RoleList]?}
composition: COMPOSITION COLON LBRA turns COMMA participants (COMMA player)+ (COMMA store)* (COMMA rolelist)? RBRA;

//Turns ::= turns:{magnitude:Magnitude, ordering:Ordering[, max:Number]?}
turns: TURNS COLON LBRA MAGNITUDE COLON magnitude COMMA ORDERING COLON ordering (COMMA MAX COLON NUM)? RBRA;

// Participants ::= players:{min:Number, max:Number|undefined}
participants: PLAYERS COLON LBRA MIN COLON NUM COMMA MAX COLON (NUM | UNDEFINED) RBRA;

// Player ::= player:{id:ID [, roleList]? }
player: PLAYER COLON LBRA ID COLON identifier (COMMA rolelist)? RBRA;

// RoleList ::= roles:{ID[, ID]*}
rolelist: ROLES COLON LBRA identifier (COMMA identifier)* RBRA;

// Store ::= store:{id:ID, owner:{ID[, ID]*}, structure:Structure, visibility:Visibility}
store: STORE COLON LBRA ID COLON identifier COMMA OWNER COLON LBRA identifier (COMMA identifier)* RBRA COMMA STRUCTURE COLON structure COMMA VISIBILITY COLON visibility RBRA;

// Regulations ::= rules:{regulation [, regulation]*}
regulations: RULES COLON LBRA regulation (COMMA regulation)* RBRA;

// Regulation ::= rule:{id:ID, scope:Scope, RuleExpr}
regulation: RULE COLON LBRA ID COLON identifier COMMA SCOPE COLON scope COMMA ruleExpr RBRA;

// RuleExpr ::= body:{Effects | Rule [, Rule]*}
ruleExpr: BODY COLON LBRA (effects|rle (COMMA rle)*) RBRA;

// Rule ::= if Condition [and Condition]* then Effects
rle: IF condition (AND condition)* THEN effects;

// Effects ::= Effect[ and Effect]*
effects: effect (AND effect)*;

// Effect ::= ID{Param[, Param]*}
effect: identifier LBRA param (COMMA param)* RBRA;

// Condition ::= ID{Param[, Param]*}
condition: identifier LBRA param (COMMA param)* RBRA;

// Param ::= ID | Content
param: identifier | content;

// Content ::= {[!]?ID[, [!]?ID]*}
content: LBRA (NEG)? identifier (COMMA (NEG)? identifier)* RBRA;

// Interactions ::= moves:{interaction [, interaction]*}
interactions: MOVES COLON LBRA interaction (COMMA interaction)* RBRA;

// Interaction ::= move:{id:ID, content:{Content}, RuleExpr}
interaction: MOVE COLON LBRA ID COLON identifier COMMA CONTENT COLON content COMMA ruleExpr RBRA;

// Magnitude ::= single | multiple
magnitude: SINGLE | MULTIPLE;

// Ordering ::= strict | liberal
ordering: STRICT | LIBERAL;

// Structure ::= set | queue | stack
structure: SET | QUEUE | STACK;

// Visibility ::= public | private
visibility: PUBLIC | PRIVATE;

// Scope ::= initial | turnwise | movewise
scope: INITIAL | TURNWISE | MOVEWISE;

AND:    'and';
BODY:   'body';
COMPOSITION: 'composition';
CONTENT: 'content';
ELSE:   'else';
GAME: 'game';
ID: 'id';
IF: 'if';
INITIAL: 'initial';
LIBERAL: 'liberal';
MAGNITUDE: 'magnitude';
MAX:    'max';
MIN:    'min';
MOVE: 'move';
MOVES: 'moves';
MOVEWISE: 'movewise';
MULTIPLE: 'multiple';
NEG:    '!';
ORDERING: 'ordering';
OWNER: 'owner';
PLAYERS: 'players';
PLAYER: 'player';
PRIVATE: 'private';
PUBLIC: 'public';
QUEUE: 'queue';
ROLES: 'roles';
RULE: 'rule';
RULES: 'rules';
SCOPE: 'scope';
SET: 'set';
SINGLE: 'single';
STACK: 'stack';
STORE: 'store';
STRICT: 'strict';
STRUCTURE: 'structure';
SYSTEM: 'system';
TURNS: 'turns';
TURNWISE: 'turnwise';
THEN:   'then';
UNDEFINED:  'undefined';
VISIBILITY: 'visibility';
COLON   : ':';
COMMA   : ',';
LBRA    : '{' ;
RBRA    : '}' ;
LINK:   '_';

NUM:    [0-9]+;
UCHAR:  [A-Z]+;
LCHAR:  [a-z]+;       
WS:     [ \t\r\n]+ -> skip; 
