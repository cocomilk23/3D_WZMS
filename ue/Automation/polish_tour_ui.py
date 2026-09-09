"""Apply the input and typography fixes established by actual window testing."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('build_tour_hud.py')),init_globals={'TOUR_HUD_FUNCTIONS':{'DrawTourLabel','DrawTourButton','DrawTourMapDot','DrawTourMap','DrawTourMenu','DrawTourMinimap','SetTourMenu'}},run_name='__main__')
