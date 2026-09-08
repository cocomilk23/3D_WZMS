"""Project-scoped MCP jobs, executed on the editor thread with durable status."""
import json,runpy,traceback,uuid
from pathlib import Path
import unreal,toolset_registry
from toolset_registry.registration import Registration

ROOT=Path(unreal.Paths.project_dir()).resolve()
AUTOMATION=ROOT.parent/'Automation'
JOBS=ROOT/'Saved/AutomationJobs'
_active=None
_registration=None

@unreal.uclass()
class WZMSProjectTools(unreal.ToolsetDefinition):
    """Execute and track scripts belonging to the WZMS workspace."""
    @toolset_registry.tool_call
    @staticmethod
    def run_script(script_name: str) -> str:
        """Schedule a .py file within ue/Automation; returns a durable job report path."""
        global _active
        if _active:raise RuntimeError('Another WZMS job is running: '+_active)
        script=(AUTOMATION/script_name).resolve()
        if not script.is_relative_to(AUTOMATION.resolve()) or script.suffix!='.py' or not script.is_file():
            raise ValueError('Script must exist inside this project Automation directory')
        job=uuid.uuid4().hex;JOBS.mkdir(parents=True,exist_ok=True)
        dest=JOBS/(job+'.json');_active=job
        report={'job':job,'script':str(script),'project':str(Path(unreal.Paths.project_dir()).resolve()/'WZMS.uproject'),'state':'scheduled'}
        dest.write_text(json.dumps(report,indent=2),encoding='utf8')
        holder=[None]
        def execute(dt):
            global _active
            unreal.unregister_slate_post_tick_callback(holder[0])
            report['state']='running';dest.write_text(json.dumps(report,indent=2),encoding='utf8')
            try:
                runpy.run_path(str(script),run_name='__main__')
                report['state']='complete'
            except Exception:
                report['state']='failed';report['error']=traceback.format_exc()
                unreal.log_error(report['error'])
            finally:
                _active=None;dest.write_text(json.dumps(report,indent=2),encoding='utf8')
        holder[0]=unreal.register_slate_post_tick_callback(execute)
        return str(dest)

def register():
    global _registration
    _registration=Registration([WZMSProjectTools]);_registration.register()
    unreal.log('WZMS project MCP automation registered')
