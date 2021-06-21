import execnet
import os


def make_ott_taxonomy(reftax_path: str, newtax_path: str, reftax_src_path: str) -> bool:
    """Reconstructs OpenTreeOfLife taxonomy by removing non-microbial life clades.

    Parameters
    ----------
    reftax_path :
        Path to reference taxonomy directory.
        `Download Latest OTT <https://tree.opentreeoflife.org/about/taxonomy-version>`_
        Run Make to compile OTT Jython files.
    newtax_path :
        Path to output taxonomy directory.
    reftax_src_path :
        Path to OTL reference-taxonomy tool('smasher')'s source code.
    reftax_path: str :
        
    newtax_path: str :
        
    reftax_src_path: str :
        

    Returns
    -------
    
        Result status

    """

    if not os.path.isdir(reftax_src_path):
        raise NotADirectoryError("Parameter `otl_reftax_src` must be a directory.")
    local_ott_path = os.path.abspath(reftax_src_path)
    jython_jar_path = local_ott_path + "/lib/jython-standalone-2.7.0.jar"
    sys_path_suffix_list = ["", "/util", "/lib", "/lib/json-simple-1.1.1.jar"]
    sys_path_list = [local_ott_path + suffix for suffix in sys_path_suffix_list]
    jythonpath_env = ":".join(sys_path_list)
    sys_path_list_repr = repr(sys_path_list)
    javaflags = "-Xmx14G"
    java_exec = "java {} -jar {}".format(javaflags, jython_jar_path)

    gate_str = "popen//python={0}//chdir={1}//env:PWD={1}//env:JYTHONPATH={2}".format(
        java_exec, local_ott_path, jythonpath_env
    )

    ret = False
    reftax_path = (
        os.path.abspath(reftax_path) if not os.path.isabs(reftax_path) else reftax_path
    )
    newtax_path = (
        os.path.abspath(newtax_path) if not os.path.isabs(newtax_path) else newtax_path
    )
    if not os.path.isdir(newtax_path):
        os.mkdir(newtax_path)
    if not os.path.isdir(reftax_path):
        raise NotADirectoryError(
            "Parameter `reference_taxonomy_path` must be a directory."
        )
    if reftax_path[-1] != "/" and newtax_path[-1] != "/":
        jython_channel_out = []

        def jython_receiver(message):
            """

            Parameters
            ----------
            message :
                

            Returns
            -------

            """
            print(message)
            jython_channel_out.append(message)
            return

        gw = execnet.makegateway(gate_str)
        jython_channel = gw.remote_exec(
            """
                                channel.send('Preparing for ReAssembly')
                                import sys
                                sys.path.extend({0})
                                from org.opentreeoflife.taxa import Taxonomy
                                from org.opentreeoflife.taxa import Newick
                                from java.lang import System 
                                from java.io import PrintStream, OutputStream
                                oldOut = System.out
                                class NoOutputStream(OutputStream):
                                    """ """
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
                                """.format(
                sys_path_list_repr, reftax_path, newtax_path
            )
        )
        jython_channel.setcallback(jython_receiver)
        jython_channel.waitclose()
        gw.exit()
        ret = jython_channel_out
    return ret
