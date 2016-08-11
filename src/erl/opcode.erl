-module(opcode).
-export[execute/2].
-include_lib("eunit/include/eunit.hrl").

-record(registers, {pc=0, sp=0, accumulator=0, index_x=0, index_y=0}).

%% NOP
execute(16#ea, #registers{
        pc = PC, sp = SP, accumulator = ACCUMULATOR,
        index_x = INDEX_X, index_y = INDEX_Y}) ->
    #registers{pc=PC+1, sp=SP, accumulator=ACCUMULATOR, index_x=INDEX_X, index_y=INDEX_Y};

%% Implied Register opcodes
execute(16#aa, #registers{
        pc = PC, sp = SP, accumulator = ACCUMULATOR,
        index_x = INDEX_X, index_y = INDEX_Y}) ->
    #registers{pc=PC+1, sp=SP, accumulator=ACCUMULATOR, index_x=ACCUMULATOR, index_y=INDEX_Y};

execute(16#8a, #registers{
        pc = PC, sp = SP, accumulator = ACCUMULATOR,
        index_x = INDEX_X, index_y = INDEX_Y}) ->
    #registers{pc=PC+1, sp=SP, accumulator=INDEX_X, index_x=INDEX_X, index_y=INDEX_Y};

execute(_, #registers{pc = PC, sp = SP, accumulator = ACCUMULATOR}) ->
    throw(unknown_opcode).

execute_nop_test_() ->
    ?_assert(execute(16#ea, #registers{}) =:= #registers{pc=1, sp=0}).

execute_txa_test_() ->
    ?_assert(execute(16#8A, #registers{index_x=4}) =:= #registers{pc=1, sp=0, accumulator=4, index_x=4}).

execute_tax_test_() ->
    ?_assert(execute(16#aa, #registers{accumulator=5}) =:= #registers{pc=1, sp=0, accumulator=5, index_x=5}).

unknown_opcode_test_() ->
    ?_assertException(throw, unknown_opcode, execute(17, #registers{})).
