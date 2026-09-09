"""Resume only the two unsaved color fixes after the diagnosed editor allocation failure."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('build_tour_hud.py')),init_globals={'TOUR_HUD_FUNCTIONS':{'DrawTourMenu','DrawTourMinimap'}},run_name='__main__')
