# The 'project' with the emphasis on the second syllable, as in a
# relational algebra projection.

import csv, string, sys

with open(sys.argv[1], 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    csvreader.next()
    print '# coding=utf-8'
    print '# This file is automatically generated.  Do not put under version control.'
    print 'def fixChromista(tax):'
    print '    count = [0]'
    print '    already = [0]'
    print '    count_all = [0]'
    print '    euk = tax.taxon("Eukaryota")'

    print '    def fixonetaxon(tax, taxon, proposed):'
    print '      count_all[0] += 1'
    print '      curr = tax.taxon(taxon)'
    print '      if curr != None:'
    print '        if curr.getParent() == euk:'
    print '            prop = tax.taxon(proposed)'
    print '            if (prop != None) and (curr.getParent() != prop):'
    print '                prop.take(curr)'
    print '                count[0] += 1'
    print '        else:'
    print '            already[0] += 1'

    print '    def incertae(tax, taxon):'
    print '        curr = tax.maybeTaxon(taxon)'
    print '        if curr != None:'
    print '            curr.incertaeSedis()'

    for row in csvreader:
        taxon = row[0].strip()
        currentparent = row[1].strip()
        proposed = row[2].strip()
        if taxon != '' and proposed != '' and not ('incertae' in proposed):
            reference = row[3].strip()
            notes = row[4].strip()

            if reference != '':
                print '    # See %s'%(reference)
            if notes != '':
                print '    # %s'%(notes)
            print "    fixonetaxon(tax, '%s', '%s')"%(taxon, proposed)
            if 'incertae sedis' in notes:
                print "    incertae(tax, '%s')"%(taxon)

    print '    print "| Chromista successes %s out of %s (%s already):" % (count[0], count_all[0], already[0])'
