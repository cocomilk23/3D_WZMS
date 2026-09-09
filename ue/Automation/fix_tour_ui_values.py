"""Correct typed float colors and explicit destination yaw, based on actual runtime failures."""
import runpy
from pathlib import Path
here=Path(__file__).parent
runpy.run_path(str(here/'build_tour_savegame.py'),init_globals={'TOUR_EXPLORER_FUNCTIONS':{'TravelToTourPlace'}},run_name='__main__')
runpy.run_path(str(here/'build_tour_hud.py'),init_globals={'TOUR_HUD_FUNCTIONS':{'DrawTourButton','DrawTourMapDot','DrawTourMap','DrawTourMenu','DrawTourMinimap'}},run_name='__main__')
