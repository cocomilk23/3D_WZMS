"""Rebuild only map drawing and input routing with distinct map/card hit-box names."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('build_tour_hud.py')),init_globals={'TOUR_HUD_FUNCTIONS':{'DrawTourMap'}},run_name='__main__')
