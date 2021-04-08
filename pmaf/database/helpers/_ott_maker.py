from pmaf.internal._shared import get_package_root
import execnet
import os

local_ott_path = os.path.join(get_package_root(),'_externals','OTL')
jython_jar_path = local_ott_path+'/lib/jython-standalone-2.7.0.jar'
sys_path_suffix_list = ['','/util','/lib','/lib/json-simple-1.1.1.jar']
sys_path_list = [local_ott_path + suffix for suffix in sys_path_suffix_list]
jythonpath_env =':'.join(sys_path_list)
sys_path_list_repr = repr(sys_path_list)
javaflags ="-Xmx14G"
java_exec = "java {} -jar {}".format(javaflags,jython_jar_path)

gate_str = "popen//python={0}//chdir={1}//env:PWD={1}//env:JYTHONPATH={2}".format(java_exec,local_ott_path,jythonpath_env)

def make_ott_taxonomy(reference_taxonomy_path,new_taxonomy_path):
    """
    Args:
        reference_taxonomy_path:
        new_taxonomy_path:
    """
    ret = False
    reference_taxonomy_path = os.path.abspath(reference_taxonomy_path) if not os.path.isabs(reference_taxonomy_path) else reference_taxonomy_path
    new_taxonomy_path = os.path.abspath(new_taxonomy_path) if not os.path.isabs(new_taxonomy_path) else new_taxonomy_path
    if not os.path.isdir(new_taxonomy_path):
       os.mkdir(new_taxonomy_path)
    if os.path.isdir(reference_taxonomy_path):
        if reference_taxonomy_path[-1] != '/' and new_taxonomy_path[-1] != '/':
            jython_channel_out = []
            def jython_receiver(message):
                print(message)
                jython_channel_out.append(message)
                return
            gw = execnet.makegateway(gate_str)
            jython_channel = gw.remote_exec("""
                                    channel.send('Preparing for ReAssembly')
                                    import sys
                                    sys.path.extend({0})
                                    from org.opentreeoflife.taxa import Taxonomy
                                    from org.opentreeoflife.taxa import Newick
                                    from java.lang import System 
                                    from java.io import PrintStream, OutputStream
                                    oldOut = System.out
                                    class NoOutputStream(OutputStream):
                                        def write(self, b, off, len): pass
                                    System.setOut(PrintStream(NoOutputStream()))
                                    result = [] 
                                    ott_path = '{1}/'
                                    output_path = '{2}/'
                                    tree_path = output_path + 'ott_tree.tre' 
                                    channel.send('Loading OpenTreeOfLife Taxonomy')
                                    ott_tax_all = Taxonomy.getTaxonomy(ott_path, 'ott_full')
                                    channel.send('OTL taxonomy is loaded')
                                    ott_tax = ott_tax_all.selectVisible('life')
                                    channel.send('Hidden nodes are removed.')
                                    metazoa = ott_tax.taxon('Metazoa', 'life')
                                    insecta = ott_tax.taxon('Insecta', 'life')
                                    metazoa_pruned = metazoa.prune()
                                    channel.send('Metazoa Removal: '+('Success' if metazoa_pruned else 'Failed'))
                                    insecta_pruned = insecta.prune()
                                    channel.send('Insecta Removal: '+('Success' if insecta_pruned else 'Failed'))
                                    ott_tax.dump(output_path, '|')
                                    channel.send('Taxonomy was successfully saved.')
                                    tree_string = ott_tax.toNewick(Newick.USE_IDS)
                                    tree_nw = Taxonomy.openw(tree_path)
                                    tree_nw.print(tree_string)
                                    tree_nw.close()
                                    channel.send('Newick tree was successfully saved.')
                                    channel.send('End of ReAssembly')
                                    """.format(sys_path_list_repr,reference_taxonomy_path,new_taxonomy_path))
            jython_channel.setcallback(jython_receiver)
            jython_channel.waitclose()
            gw.exit()
            ret = jython_channel_out
    return ret




