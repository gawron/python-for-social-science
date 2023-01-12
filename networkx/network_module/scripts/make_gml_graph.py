"""
Two different format conversions into GML graph rep:

1) Turn IBM graph base representation
of character relationships in novels
into GML format graphs.

IBM graph base rep (two cases)::

    CharacterLine => Char_id (two chars) Description (arbitrary string)
    ChapterLine =>  PartNum(one digit).ChapterNum(up to two digs) SceneList
    SceneList => Scene (; Scene)*
    Scene => Char_id (, Charid)*

So scene lists are semicolon separated lists of scenes and
scenes are commas separated lists of characters.

2) GDF format, which is a newish graph allowing both
node and edge attributes.  The latter are not yet handled.
Turn it into GML.

"""
import networkx as nx
from collections import defaultdict
   
def convert_to_gml(path,anonymize=False, new_names_file=None,
                   relabel=False):
    global nodes, edges
    (base,ext) = os.path.splitext(path)
    if ext == '.dat':
       (nodes, edges) =  make_stanford_gb_graph(path,relabel=relabel)
       edge_attrs = None
    elif ext == '.gdf':
       print 'Anonymizing: %s' % (anonymize,)
       (nodes,edges,edge_attrs,mapped) = \
                       make_gdf_graph(path,anonymize=anonymize, \
                                      new_names_file=new_names_file)
       if anonymize:
           base = base + '_anon'
    else:
       print 'Unknown file type.'
       print 'This script only converts files in Stanford graph base fiction format (extension .dat)'
       print 'and in gdf format (extension .gdf). If you have a file in one of those formats'
       print 'with a different extension, please rename.'
       sys.exit()
    print_gml_graph(nodes, edges,base + '.gml',edge_attrs)
    return (nodes, edges)

from collections import Counter
import re, datetime

chapter_line_re = re.compile(r'((\d\.)?\d\d?|&):')
character_line_re = re.compile(r'(\w\w)\s+(.+)')

def make_stanford_gb_graph (path,relabel=False):
    """
    Use relabel = True to extract disabbreviated names from
    description.  Works with HOmer, should work with others.
    """
    nodes = dict()
    ids_to_index = dict()
    edges = Counter()
    ctr = 0
    with open(path, 'r') as fh:
        for (i,line) in enumerate(fh):
            line = line.strip()
            if line.startswith('*'):
                # comment line
                continue
            elif line == '':
                # separating nodes frm edges
                continue
            elif chapter_line_re.match(line):
                (chap, scene_str) = line.split(':')
                scenes = scene_str.split(';')
                for scene in scenes:
                    ## This is an UNDIRECTED graph, so
                    ## we represent all start/end edge pairs in sorted order.
                    nodelist = \
                      [ids_to_index[char] for char in\
                         sorted(scene.split(','))]
                    #print sorted(scene.split(','), reverse=True)
                    add_edges(edges, nodelist)
            else:
                m = character_line_re.match(line)
                if m:
                    (id, desc) = m.groups()
                    nodes[ctr] = dict(label=id,desc=desc)
                    ids_to_index[id] = ctr
                    ctr += 1
                else:
                    print "Couldn't parse line %d: %s" % (i+1,line)
    if relabel:
        # Switch long names, take from descriptions
        relabel_nodes(nodes)
    return (nodes, edges)

def relabel_nodes (nodes):
    """
    Structure of node dict::
     
       nodes[ctr] = dict(label=id,desc=desc)

    re.sub('DI','Diana', 'Xanthus, brother of 1C, killed by DI')
    """
    global new_names, abbrevs
    new_names = set()
    abbrevs = dict()
    for (index, att_dict) in nodes.iteritems():
        new_name = (att_dict['desc'].split(',')[0]).split()[0]
        if new_name in new_names:
            print '%s used twice! Uniquifying ' % (new_name,),
            new_name = make_unique_name(new_name,new_names)
            print 'to %s!' % (new_name,)
        new_names.add(new_name)
        abbrev = att_dict['label']
        abbrevs[abbrev] = new_name
        att_dict['abbrev'] = abbrev
        att_dict['label'] = new_name
    ## Now that we know all abbrevs, let's get rid of refs to them.
    for (index, att_dict) in nodes.iteritems():
        desc = subst_full_names(abbrevs,att_dict)
        att_dict['desc'] = desc
        
def subst_full_names(abbrevs,att_dict):
    desc = att_dict['desc']
    #desc_words = desc.split()
    # A little inline tokenizatiomn need for descs containing
    # punctuation, apostrophe,
    desc_words = [x for y in desc.split() for x in re.split(r"[\(\),']",y)]
    for abbrev in abbrevs:
        if abbrev in desc_words:
            abbrev_re = re.compile(r'\b%s\b' % (abbrev,))
            desc = re.sub(abbrev_re,
                          abbrevs[abbrev],
                          desc)
    return desc

def add_edges(edges, nodelist):
    """
    Increment weight on the pairwise links between all edge pairs in C{edges}

    We normalize the weight increment on the link to another character by
    how many characters there are in the scene.  (Solo scenes between
    Anna and Vronsky add more to the link weight between them than
    scenes in which they both appear at the opera with a dozen
    other socialites).
    
    Implementation: the total link weight mass for any give character in a 
    scene is 1, distributed equally among the other characters in
    the scene;  therefore, the sum of all the link weights for
    any character is equal to the number of scenes they appear in
    (minus the solo scenes; Vronsky's attempted suicide scene does not
    contribute any link weight).  This makes weighted degree centrality
    more meaningful.
    """
    try:
        norm = 1.0/float(len(nodelist) - 1)
    except ZeroDivisionError:
        # Vronsky trying to shoot himself.  Solo scene.
        # No edge to add.  Return
        return
    for (i,start) in enumerate(nodelist):
        for end in nodelist[i+1:]:
            edges[(start,end)] += norm

## We are going to treat edge ids as strings, so we dont
## allow nodeid dfns that request them to be treated as ints.
nodedef_line_re = re.compile(r'nodedef>\s*name\s+VARCHAR,?\s*(.*)')
## And do the same in edgepairs
edgedef_line_re = re.compile(r'edgedef>node1\s+VARCHAR,node2\s+VARCHAR,?(.*)')
## We are assuming nodeids are digit sequences (which we'll treat as strings)
node_line_re = re.compile(r'\d+,?(.*)')
## And therfore edges start with pairs of digit sequences.
edge_line_re = re.compile(r'(\d+),(\d+),?(.*)')
from random import randint

def make_gdf_graph (path,undirected=True, anonymize=False, new_names_file=None):
    global edge_attrs,node_attrs, mapped_ids, mapped_names, nodes,e0,e1, edge_info, labels,new_names
    if anonymize:
        if new_names_file:
            new_names = nx.read_gml(new_names_file,relabel=True).nodes()
        else:
            new_names = homer_chars.split('\n')
        print 'len(new_names) %d' % len(new_names)
    else:
        new_names = None
    mapped_names = defaultdict(list)
    mapped_ids = defaultdict(list)
    map_to_python_type = dict(VARCHAR = str,INT = int)
    nodes = dict()
    (node_attrs, edge_attrs) = ([],[])
    edge_attrs_dict = dict()
    edges = Counter()
    edge_info_started = False
    labels = set()
    label_ctr = 0
    node_line_ctr = 0
    with open(path, 'r') as fh:
        for (i,line) in enumerate(fh):
            line = line.strip()
            ndm = nodedef_line_re.match(line)
            edm = edgedef_line_re.match(line)
            nm = node_line_re.match(line)
            em = edge_line_re.match(line)
            if line == '':
                # may not be needed
                continue
            elif ndm:
                node_def_info = ndm.groups()[0].split(",")
                for attr in node_def_info:
                    (attr_name, tp) = attr.split()
                    tp = map_to_python_type[tp]
                    node_attrs.append((attr_name,tp))
            elif edm:
                group_str = edm.groups()[0]
                if group_str:
                    edge_def_info = group_str.split(",")
                else:
                    edge_def_info = []
                for attr in edge_def_info:
                    (attr_name, tp) = attr.split()
                    tp = map_to_python_type[tp]
                    edge_attrs.append((attr_name,tp))
                edge_info_started=True
            elif em and edge_info_started:
                edge_info = line.split(",")
                assert len(edge_info) == len(edge_attrs) + 2, 'Line %d %s : Illegal edge line' % (i,line)
                e0 = name_map(int(edge_info[0]),[], mapped_names, mapped_ids, anonymize,labels)
                e1 = name_map(int(edge_info[1]),[], mapped_names, mapped_ids, anonymize,labels)
                #e0 = mapped_ids[int(edge_info[0])][0]
                #e1 = mapped_ids[int(edge_info[1])][0]
                edge_tup = (e0,e1)
                for e in edge_tup:
                    assert e in nodes, 'Unknown node in edge tuple: %s' % (line,)
                if undirected:
                    node_tup = tuple(sorted(edge_tup))
                add_edges(edges, edge_tup)
                if edge_info[2:]:
                    edge_attr_dict = dict()
                    edge_attrs_dict[edge_tup] = edge_attr_dict
                    for (i, val) in enumerate(edge_info[2:]):
                        (attr_name,tp) = edge_attrs[i]
                        edge_attr_dict[attr_name] = tp(val)
            elif nm:
                node_line_ctr += 1
                node_info = line.split(",")
                attr_info = node_info[1:]
                assert len(attr_info) == len(node_attrs), 'Line %d %s : Illegal node line' % (i,line)
                node_attr_dict = dict()
                this_id = name_map(int(node_info[0]),\
                                   [], mapped_names, mapped_ids, anonymize, labels, create=True)
                nodes[this_id] = node_attr_dict
                if attr_info:
                    for (i, val) in enumerate(attr_info):
                        (attr_name,tp) = node_attrs[i]
                        if val is not '':
                            try:
                                val = tp(val)
                            except ValueError as e:
                                print 'Invalid value: ',line, attr_name, val
                                raise e
                            node_attr_dict[attr_name] = val
                this_label = name_map(node_attr_dict['label'],\
                                      new_names, mapped_names, mapped_ids,
                                      anonymize,labels,create=True)
                assert this_label not in labels, 'Duplicate label somehow created %s %s' % (this_label, line)
                labels.add(this_label)
                label_ctr += 1
                print '%d. Added %s (line %d) [%d]' % (label_ctr, this_label, node_line_ctr,len(labels))
                node_attr_dict['label'] = this_label
                
    mapped_names.update(mapped_ids)
    return (nodes, edges, edge_attrs_dict, mapped_names)

def name_map(real_name, new_names, mapped_names, mapped_ids, anonymize, labels,
             create=False):
    if real_name in labels:
        ctr = 0
        real_name0 = real_name
        while real_name in labels:
            ctr += 1
            real_name = '%s_%d' % (real_name0,ctr)
    if anonymize:
        if create:
            alias = get_new_name(new_names,labels,real_name,\
                                 mapped_names,mapped_ids)
            return alias
        elif real_name in mapped_names:
            mappings = mapped_names[real_name]
            if len(mappings) > 1:
                print 'Warning: Retrieving one-many name map for %s! Using first.' % (real_name,)
            return mappings[0]
        elif real_name in mapped_ids:
            mappings = mapped_ids[real_name]
            if len(mappings) > 1:
                raise Exceptions, 'Error: Found one-many id map for %s!' % (real_name,)
            return mappings[0]
        else:
            raise Exception, 'Unknown name %s' % real_name
    else:
        return real_name
    
def get_new_name (new_names, names_used, real_name, mapped_names,mapped_ids):
    """
    If we've used up all the names in
    mapped, just return a random duplicate name
    and make it unique by indexing.

    If no new names are supplied pick a random
    integer.
    """
    global names_left
    if new_names:
        space_size = len(new_names)-1
        max_index = space_size - (len(names_used) + 1)
        if max_index < 0:
            # Just reuse a name and add index to make it unique
            monicker = make_unique_name(new_names[randint(0,space_size)],names_used)
        else:
            names_left = list(set(new_names).difference(set(names_used)))
            monicker = names_left[randint(0,max_index)]
        mapped_names[real_name].append(monicker)
    else:
        monicker = randint(10000, 1000000)
        ids_used = mapped_ids.values()
        # on the off chance of random choice collision
        while monicker in ids_used:
            monicker = randint(10000, 1000000)
        mapped_ids[real_name].append(monicker)
    return monicker

def make_unique_name(name,names_used):
    (new_name,parts) = (name, None)
    while new_name in names_used:
        if parts is None:
            parts = name.split('_')
            try:
                (stem,index) = parts
                index = int(index)
            except ValueError:
                (stem,index) = (name,1)
        index += 1
        new_name = stem + '_' + str(index)
    return new_name

def print_gml_graph(nodes, edges, filename=None, edge_attrs=None):
    """
    For now we are ignoring edge_attrs.
    """
    n = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    with open(filename,'w') as ofh:
        print >> ofh, 'Creator "Jean Mark Gawron on %s"' % (n,)
        print >> ofh, 'graph'
        print >> ofh, '['
        for (node, node_dict) in nodes.iteritems():
            print_gml_node(node,node_dict, ofh)
        for ((start,end), count) in edges.iteritems():
            print_gml_edge(start,end,count, ofh)
        print >> ofh, ']'



def print_gml_node(node,node_dict,fh):
    node_attr_strs = [node_attr_temp % (key,val) for key,val in node_dict.iteritems()]
    attr_str = '\n'.join(node_attr_strs)
    print >> fh, node_str % (node, attr_str),

def print_gml_edge(start,end,count,fh):
    print >> fh, edge_str % (start,end,count),


def print_characters (nodes,print_desc=False):
    n_itr = nodes.iteritems()
    try:
        char_list = [(att_dict['label'], att_dict['abbrev'], att_dict['desc']) for (index, att_dict) in n_itr]
        abbrevs = True
    except KeyError:
        char_list = [(att_dict['label'],) for (index, att_dict) in n_itr]
        abbrevs = False
    char_list.sort()
    for fields in char_list:
        if print_desc and abbrevs:
            print '%-15s %4s %s' % fields
        else:
            print '%-15s' % (fields[0],)
    


node_attr_temp = '      %s "%s"'

edge_str = """   edge
   [
      source %s
      target %s
      value  %.2f
   ]
"""

node_str = """   node
   [
      id %d
%s
   ]
"""

homer_chars = \
"""
barbarea      
Abas           
Ablerus        
Acamas         
Acamas_2       
Achilles       
Actor          
Adamas         
Adrestus       
Adrestus_2     
Aegaeon        
Aeneas         
Aenius         
Aeolus         
Aesepus        
Aesymnus       
Aethra         
Agamede        
Agamemnon      
Agapenor       
Agastrophus    
Agathon        
Agelaus        
Agelaus_2      
Agenor         
Agrius         
Alastor        
Alastor_2      
Alcandrus      
Alcathous      
Alcimedon      
Alcimus        
Alcmaon        
Alcmene        
Altes          
Althea         
Amazons        
Amisodarus     
Amopaon        
Amphiclus      
Amphidamas     
Amphimachus    
Amphimachus_2  
Amphion        
Amphius        
Amphius_2      
Amphoterus     
Amyntor        
Ancaeus        
Anchialus      
Anchises       
Andromache     
Anteia         
Antenor        
Antilochus     
Antimachus     
Antiphates     
Antiphonus     
Antiphus       
Antiphus_2     
Antiphus_3     
Aphareus       
Aphrodite      
Apisaon        
Apisaon_2      
Apollo         
Arcesilaus     
Archelochus    
Archeptolemus  
Archesilaus    
Areilycus      
Areilycus_2    
Areithous      
Areithous_2    
Ares           
Aretaon        
Aretus         
Ariadne        
Artemis        
Asaeus         
Ascalaphus     
Ascanius       
Ascanius_2     
Asclepius      
Asius          
Assaracus      
Asteropaeus    
Astyalus       
Astynous       
Astynous_2     
Astyoche       
Astyocheia     
Astypylus      
Ate            
Athene         
Atreus         
Atymnius       
Augeias        
Autolycus      
Automedon      
Autonous       
Autonous_2     
Axius          
Axylus         
Bathycles      
Bellerophon    
Bias           
Bias_2         
Bienor         
Boreas         
Borus          
Briseis        
Bucolion       
Calchas        
Caletor        
Calysius       
Cassandra      
Castor         
Cebriones      
Charis         
Charops        
Chersidamas    
Chimera        
Chiron         
Chromius       
Chromius_2     
Chromius_3     
Chromius_4     
Chromius_5     
Chryseis       
Chryses        
Chrysothemis   
Cinyras        
Cisses         
Cleitus        
Cleobolus      
Cleopatra      
Clonius        
Clymene        
Clysonomus     
Clytia         
Clytius        
Clytomedes     
Coeranus       
Coeranus_2     
Coon           
Copreus        
Crethon        
Croesmus       
Cronus         
Daedalus       
Daetor         
Damasus        
Danae          
Dardanus       
Dares          
Death          
Deicoon        
Deiochus       
Deiopites      
Deiphobus      
Deipyle        
Deipylus       
Deipyrus       
Deisenor       
Demeter        
Democoon       
Demoleon       
Demuchus       
Deucalion      
Dia            
Diomede        
Diomedes       
Dione          
Dionysus       
Diores         
Dius           
Dolon          
Dolops         
Dolops_2       
Doryclus       
Dracius        
Dresus         
Dryops         
Echecles       
Echeclus       
Echeclus_2     
Echemmon       
Echepolus      
Echepolus_2    
Echius         
Echius_2       
Eeriboea       
Eetion         
Eetion_2       
Eileithyia     
Eioneus        
Elasus         
Elatus         
Elephenor      
Eniopeus       
Ennomus        
Ennomus_2      
Enyo           
Eos            
Epaltes        
Epeigeus       
Epeius         
Ephialtes      
Epicles        
Epistor        
Epistrophus    
Epistrophus_2  
Epistrophus_3  
Erechtheus     
Ereuthalion    
Erichtonius    
Erinnyes       
Erymas         
Erymas_2       
Eteocles       
Euchenor       
Eudorus        
Eumelus        
Euneus         
Euphemus       
Euphorbus      
Europa         
Eurus          
Euryalus       
Euryalus_2     
Eurybates      
Eurymedon      
Eurynome       
Eurypylus      
Eurystheus     
Evippus        
False          
Ganymede       
Glaucus        
Glaucus_2      
Gorgythion     
Graces         
Great          
Greek          
Guneus         
Hades          
Haemon         
Halius         
Harpalion      
Hebe           
Hecamede       
Hector         
Hecuba         
Helen          
Helenus        
Helenus_2      
Hephaestus     
Hera           
Heracles       
Hermes         
Hesione        
Hicetaon       
Hippocoon      
Hippodameia    
Hippodamus     
Hippodamus_2   
Hippolochus    
Hippolochus_2  
Hipponous      
Hippothous     
Hippothous_2   
Hippotion      
Homer          
Hours          
Hypeirochus    
Hypeiron       
Hyperenor      
Hypsenor       
Hypsenor_2     
Hypsipyle      
Hyrtius        
Ialmenus       
Iamenus        
Iamenus_2      
Iasus          
Idaeus         
Idaeus_2       
Idas           
Idomeneus      
Ilioneus       
Ilus           
Imbrius        
Iobates        
Ipheus         
Iphianassa     
Iphiclus       
Iphidamus      
Iphinous       
Iphis          
Iphition       
Iris           
Isander        
Isus           
Itymoneus      
Janos          
Lampus         
Laodamas       
Laodameia      
Laodice        
Laodice_2      
Laodocus       
Laogonus       
Laomedon       
Laothoe        
Leiocritus     
Leitus         
Leonteus       
Leto           
Leucus         
Licymnius      
Little         
Loagonus       
Lycaon         
Lycomedes      
Lycon          
Lycophontes    
Lycophron      
Lycurgus       
Lycurgus_2     
Lysander       
Machaon        
Maeon          
Maris          
Marpessa       
Mecisteus      
Mecisteus_2    
Medesicaste    
Medon          
Medon_2        
Meges          
Melanippus     
Melanippus_2   
Melanippus_3   
Melanippus_4   
Melanthius     
Melas          
Meleager       
Menelaus       
Menesthes      
Menestheus     
Menestheus_2   
Menesthius     
Menoetius      
Menon          
Meriones       
Mermerus       
Merops         
Mesthles       
Mestor         
Minos          
Mnesus         
Moira          
Molion         
Moliones       
Moliones_2     
Molus          
Morys          
Mulius         
Mulius_2       
Mulius_3       
Muses          
Mydon          
Mydon_2        
Mygdon         
Mynes          
Nastes         
Neleus         
Nereids        
Nestor         
Night          
Niobe          
Nireus         
Noemon         
Noemon_2       
Notus          
Oceanus        
Odius          
Odius_2        
Odysseus       
Oedipus        
Oeneus         
Oenomaus       
Oileus         
Olympian       
Ophelestes     
Ophelestes_2   
Opheltius      
Opheltius_2    
Opites         
Oresbius       
Orestes        
Orestes_2      
Orestes_3      
Ormenus        
Ormenus_2      
Orsilochus     
Orsilochus_2   
Orthaeus       
Orus           
Othryoneus     
Otreus         
Otus           
Otus_2         
Palmys         
Pammon         
Pandarus       
Pandion        
Pandocus       
Panthous       
Paris          
Patroclus      
Pedaeus        
Pedasus        
Peirithous     
Peirous        
Peisander      
Peisander_2    
Peisander_3    
Pelagon        
Pelagon_2      
Pelegon        
Peleus         
Pelops         
Peneleos       
Periboea       
Perimus        
Periphas       
Periphetes     
Periphetes_2   
Persephone     
Perseus        
Phaestus       
Phalces        
Phegeus        
Pheidas        
Pheidippus     
Phereclus      
Philoctetes    
Philonoe       
Phoenix        
Phorcys        
Phylacus       
Phylas         
Phyleus        
Phylus         
Pidytes        
Podaleirius    
Podarces       
Podarge        
Podes          
Polites        
Polybus        
Polydamus      
Polydeuces     
Polydora       
Polydorus      
Polydorus_2    
Polyeidus      
Polyidus       
Polymele       
Polymelus      
Polyneices     
Polyphetes     
Polypoetes     
Polyxeinus     
Popyphontes    
Poseidon       
Priam          
Proetus        
Promachus      
Pronous        
Protesilaus    
Prothoenor     
Prothoon       
Prothous       
Prytanis       
Pylaemenes     
Pylaeus        
Pylartes       
Pylartes_2     
Pylon          
Pyraechmes     
Pyrasus        
Pyris          
Rhadamanthus   
Rhea           
Rhesus         
Rhigmus        
Robots         
Rumor          
Sarpedon       
Satnius        
Scamandrius    
Scamandrius_2  
Schedius       
Schedius_2     
Semele         
Simoeis        
Simoeisius     
Sisyphus       
Sleep          
Socus          
Solymi         
Spercheius     
Sthenelaus     
Sthenelus      
Stichius       
Strife         
Talthybius     
Telamon        
Tethys         
Teucer         
Teuthras       
Thalpius       
Thamyris       
Theano         
Themis         
Thersilochus   
Thersilochus_2 
Thersites      
Thestor        
Thetis         
Thoas          
Thoas_2        
Thoon          
Thoon_2        
Thoon_3        
Thootes        
Thrasius       
Thrasymedes    
Thrasymelus    
Thyestes       
Thymbraeus     
Thymoetes      
Tithonus       
Tlepolemus     
Tlepolemus_2   
Trechus        
Troilus        
Trojan         
Trojan_2       
Tros           
Tros_2         
Tydeus         
Ucalegon       
Xanthus        
Xanthus_2      
Xanthus_3      
Zephyr         
Zeus           
"""


if __name__ == '__main__':
   import sys,os.path
   #anonymize=False
   if len(sys.argv) == 2:
       path = sys.argv[1]
       anonymize = False
   elif len(sys.argv) == 3:
       path = sys.argv[1]
       anonymize = True
   else:
       print 'Usage: %s <filename> [anonymize?]' % (sys.argv[0],)
       sys.exit()
   (nodes, edges) = convert_to_gml(path,anonymize=anonymize,relabel=True)
   print_characters(nodes)
