/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

grammar dgdl;

// System       ::= system:{id:ID [,Game]+} | Game
system: SYSTEM COLON LBRA ID COLON id (COMMA game)+ RBRA | game; 

// Game         ::= game:{id:ID, Composition [, Regulation]* [, Interaction]+}
game: GAME COLON LBRA ID COLON id 
      COMMA composition (COMMA regulations)* (COMMA interactions)+ RBRA;

//Composition   ::= {Turns, Participants [,Player]+ [,Store]* [,RoleList]?}
composition: COMPOSITION COLON LBRA turns COMMA participants (COMMA player)+ (COMMA store)* (COMMA rolelist)? RBRA;

//Turns         ::= turns:{magnitude:Magnitude, 
//                  ordering:Ordering[, max:Number]?}
turns: TURNS COLON LBRA MAGNITUDE COLON magnitude 
       COMMA ORDERING COLON ordering (COMMA MAX COLON NUM)? RBRA;

//Magnitude     ::= single | multiple
magnitude: SINGLE | MULTIPLE;

//Ordering      ::= strict | liberal
ordering: STRICT | LIBERAL;

//Participants  ::= players:{min:Number, max:Number|undefined}
participants: PLAYERS COLON LBRA MIN COLON NUM 
              COMMA MAX COLON (NUM | UNDEFINED) RBRA;

//Player        ::= player:{id:ID [, roleList]? }
player: PLAYER COLON LBRA ID COLON id (COMMA rolelist)? RBRA;

//Store         ::= store:{id:ID, owner:{ID[, ID]*}, 
//                  structure:Structure, visibility:Visibility}
store: STORE COLON LBRA ID COLON id COMMA OWNER COLON LBRA id (COMMA id)* RBRA
       COMMA STRUCTURE COLON structure COMMA VISIBILITY COLON visibility RBRA;

//Structure         ::= set | queue | stack
structure: SET | QUEUE | STACK;

//Visibility        ::= public | private
visibility: PUBLIC | PRIVATE;

//RoleList        ::= roles:{ID[, ID]*}
rolelist: ROLES COLON LBRA id (COMMA id)* RBRA;

//Regulations       ::= rules:{Regulation[, Regulation]*}
regulations: RULES COLON LBRA regulation (COMMA regulation)* RBRA;
//Regulation        ::= rule:{id:ID, scope:Scope, RuleExpr}
regulation: RULE COLON LBRA ID COLON id 
            COMMA SCOPE COLON scope COMMA ruleExpr RBRA;

//Scope             ::= initial | turnwise | movewise
scope: INITIAL | TURNWISE | MOVEWISE;

//Interactions       ::= moves:{Move[, Move]*}
interactions: MOVES COLON LBRA interaction (COMMA interaction)* RBRA;

//Interaction       ::= move:{id:ID, content:Content, RuleExpr}
interaction: MOVE COLON LBRA ID COLON id
             COMMA CONTENT COLON content 
             COMMA ruleExpr RBRA;

//Content           ::= {[!]?ID[, [!]?ID]*}
content: LBRA (NEG)? id (COMMA (NEG)? id)* RBRA;

//RuleExpr          ::= body:{Effects | Rule [, Rule]*} 
ruleExpr: BODY COLON LBRA (effects|rle (COMMA rle)*) RBRA;
            
//Rule              ::= if Condition [and Condition]* then Effects
rle: IF condition (AND condition)* THEN effects;

//Effects           ::= Effect[ and Effect]*
effects: effect (AND effect)*;

//Effect            ::= ID{Param[, Param]*}
effect: id LBRA param (COMMA param)* RBRA;

//Condition         ::= ID{Param[, Param]*}
condition: id LBRA param (COMMA param)* RBRA;

//ID                ::= UChar|LChar[UChar|LChar|Num|Link]*
id: (UCHAR|LCHAR)+(UCHAR|LCHAR|NUM|LINK)*;

//Param             ::= ID | Content
param: id | content;

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

LBRA: '{';
RBRA: '}';
COLON: ':';
COMMA: ',';

NUM:    [0-9]+;
UCHAR:  [A-Z]+;
LCHAR:  [a-z]+;
LINK:   '_';