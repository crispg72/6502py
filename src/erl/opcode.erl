-module(opcode).
-export[execute/2].
-include_lib("eunit/include/eunit.hrl").

-record(registers, {pc=0, sp=0, accumulator=0}).

execute(16#ea, #registers{pc = PC, sp = SP, accumulator = ACCUMULATOR}) ->
    #registers{pc=PC+1, sp=SP};
execute(_, #registers{pc = PC, sp = SP, accumulator = ACCUMULATOR}) ->
    throw(unknown_opcode).

execute_nop_test_() ->
    ?_assert(execute(16#ea, #registers{}) =:= #registers{pc=1, sp=0}).

unknown_opcode_test_() ->
    ?_assertException(throw, unknown_opcode, execute(17, #registers{})).
