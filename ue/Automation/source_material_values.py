"""Follow recorded Blender colour links, retaining tint through multiply nodes."""
def base_parameters(row):
    nodes={n['name']:n for n in row['nodes']}
    links={(x[2],x[3]):x[0] for x in row['links']}
    bs=next((n for n in row['nodes'] if n['type']=='ShaderNodeBsdfPrincipled'),None)
    values=bs['inputs'] if bs else {}
    def value(name,default):return next((v for k,v in values.items() if k.endswith(':'+name)),default)
    base=value('Base Color',row['diffuse_color'])[:3]
    def pair(v):
        vec=list(v[:3]) if isinstance(v,(list,tuple)) else [v]*3
        return [vec[:],vec[:]]
    def inp(node,name,default):
        source=links.get((node['name'],name))
        if source:return evaluate(nodes[source])
        return pair(next((v for k,v in node['inputs'].items() if k.endswith(':'+name)),default))
    def evaluate(node):
        kind=node['type']
        if kind=='ShaderNodeValToRGB':
            ramp=node['ramp']['elements'];return [ramp[0][1][:3],ramp[-1][1][:3]]
        if kind=='ShaderNodeMixRGB':
            a=inp(node,'Color1',base);b=inp(node,'Color2',base);f=inp(node,'Factor',.5)
            operation=node.get('blend_type','MIX');out=[]
            for end in range(2):
                result=[]
                for j in range(3):
                    x,y,t=a[end][j],b[end][j],f[end][0]
                    mixed=x*y if operation=='MULTIPLY' else x+y if operation=='ADD' else x-y if operation=='SUBTRACT' else 1-(1-x)*(1-y) if operation=='SCREEN' else y
                    result.append(max(0,x*(1-t)+mixed*t))
                out.append(result)
            return out
        if kind=='ShaderNodeTexNoise':return [[0]*3,[1]*3]
        return pair(base)
    source=links.get(((bs or {}).get('name'),'Base Color'))
    a,b=evaluate(nodes[source]) if source else ([v*.94 for v in base],[v*1.06 for v in base])
    return a,b,float(value('Roughness',.65)),float(value('Metallic',0))
