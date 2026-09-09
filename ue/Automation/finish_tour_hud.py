"""Resume event graph after all HUD drawing functions have been saved successfully."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('build_tour_hud.py')),init_globals={'TOUR_HUD_EVENTS_ONLY':True},run_name='__main__')
