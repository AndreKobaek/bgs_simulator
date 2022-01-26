from main import dogdog_perm_opp_test, dogdog_perm_test
from minions import DefenderofArgus, Sellemental, WrathWeaver
from tasks import add, perform_simulation
from warband import Warband

warbands_json = (
    Warband([Sellemental(), WrathWeaver()]).toPickle(),
    Warband([DefenderofArgus()]).toPickle(),
)
results = perform_simulation.delay(warbands_json, 1_000)
