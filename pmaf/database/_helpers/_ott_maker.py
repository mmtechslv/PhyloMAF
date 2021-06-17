import execnet
import os


def make_ott_taxonomy(
        reference_taxonomy_path: str,
        new_taxonomy_path: str,
        otl_reftax_src: str,
        jython_jar_src: str,
        json_simple_jar_src: str
) -> bool:
    """Reconstructs OpenTreeOfLife taxonomy by removing non-microbial life clades.

    Args:
        reference_taxonomy_path: Path to reference taxonomy directory. `Download Latest OTT <https://tree.opentreeoflife.org/about/taxonomy-version>`_
        new_taxonomy_path: Path to output taxonomy directory.
        otl_reftax_src: Path to OTL reference-taxonomy tool('smasher')'s source code. `Link to repo <https://github.com/OpenTreeOfLife/reference-taxonomy>`_
        jython_jar_src: Path to 'jython-standalone-[version].jar' file. `Download Jython Standalone <https://www.jython.org/download.html>`_
        json_simple_jar_src: Path to 'json_simple-[version].jar' file. `Download Json Simple <https://code.google.com/archive/p/json-simple/downloads>`_

    Returns:
        Result status

    """

    if not os.path.isdir(otl_reftax_src):
        raise NotADirectoryError("Parameter `otl_reftax_src` must be a directory.")
    if not os.path.isfile(jython_jar_src):
        raise FileNotFoundError('File `jython_jar_src` was not found. ')
    if not os.path.isfile(json_simple_jar_src):
        raise FileNotFoundError('File `json_simple_jar_src` was not found. ')
    local_ott_path = os.path.abspath(otl_reftax_src)
    jython_jar_path = os.path.abspath(jython_jar_src) #local_ott_path + "/lib/jython-standalone-2.7.0.jar"
    json_simple_jar_path = os.path.abspath(json_simple_jar_src)
    sys_path_suffix_list = ["", "/util", "/lib"]
    sys_path_list = [local_ott_path + suffix for suffix in sys_path_suffix_list] + [json_simple_jar_path, jython_jar_path]
    jythonpath_env = ":".join(sys_path_list)
    sys_path_list_repr = repr(sys_path_list)
    javaflags = "-Xmx14G"
    java_exec = "java {} -jar {}".format(javaflags, jython_jar_path)

    gate_str = "popen//python={0}//chdir={1}//env:PWD={1}//env:JYTHONPATH={2}".format(
        java_exec, local_ott_path, jythonpath_env
    )
    print(gate_str)

    ret = False
    reference_taxonomy_path = (
        os.path.abspath(reference_taxonomy_path)
        if not os.path.isabs(reference_taxonomy_path)
        else reference_taxonomy_path
    )
    new_taxonomy_path = (
        os.path.abspath(new_taxonomy_path)
        if not os.path.isabs(new_taxonomy_path)
        else new_taxonomy_path
    )
    if not os.path.isdir(new_taxonomy_path):
        os.mkdir(new_taxonomy_path)
    if os.path.isdir(reference_taxonomy_path):
        if reference_taxonomy_path[-1] != "/" and new_taxonomy_path[-1] != "/":
            jython_channel_out = []

            def jython_receiver(message):
                """

                Args:
                  message:

                Returns:

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
                                        ''' '''
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
                    sys_path_list_repr, reference_taxonomy_path, new_taxonomy_path
                )
            )
            jython_channel.setcallback(jython_receiver)
            jython_channel.waitclose()
            gw.exit()
            ret = jython_channel_out
    return ret
