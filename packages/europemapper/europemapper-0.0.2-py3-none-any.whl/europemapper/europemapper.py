import pkg_resources

simple_keys = ['al', 'at', 'ba', 'be', 'bg', 'by', 'ch', 'cy', 'cz', 'de', 'dk', 'ee', 'es', 'fi', 'fr', 'gr', 'hr', 'hu', 'ie', 'is', 'it', 'lt', 'lu', 'lv', 'md', 'me', 'mk', 'mt', 'nl', 'no', 'pl', 'pt', 'ro', 'rs', 'se', 'si', 'sk', 'xk']

def make_map(filename, styles):
    base_map_path = pkg_resources.resource_filename(__name__, 'europe_basemap.svg')
    with open(base_map_path) as f:
        base_map = f.read()
    
    generated_styles = []
    
    for k,v in styles.items():
        if k in simple_keys:
            generated_styles.append("#"+k+" { fill: "+v+" !important; }")
        elif k == "ua":
            generated_styles.append("#"+k+" { fill: "+v+" !important; }")
            generated_styles.append("#crimea_disputed { fill: "+v+" !important; }")
        elif k == "gb":
            generated_styles.append("#gb-gbn { fill: "+v+" !important; }")
            generated_styles.append("#gb-nir { fill: "+v+" !important; }")
        else:
            print("Unknown country code " + k + "\n")
            print("Supported codes are")
            print(simple_keys + ['ua','gb'])
            raise ValueError('unknown country code')
                        
    colored_map = base_map.replace('<style type="text/css"></style>','<style type="text/css">\n'+"\n".join(generated_styles)+'</style>\n')
    
    with open(filename,"w") as f:
        f.write(colored_map)
    
