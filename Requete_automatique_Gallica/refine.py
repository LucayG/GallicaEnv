# -*- coding: utf-8 -*-
import os
try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                import cElementTree as etree
            except ImportError:
                try:
                    import elementtree.ElementTree as etree
                except ImportError:
                    print("goddamn it, something is seriously wrong with the package's installation.")


def refine_it(path, worden, serial, prox, ocr_rate):
    """extract ocr rates and ark links"""

    #prepare xml document for parsing
    surlist = []
    if os.path.exists('GAL.txt') == False :
        with open('GAL.txt', 'w', encoding='utf-8') as GAL:
            GAL.write('')
    with open(path, 'r', encoding=("utf-8")), open('GAL.txt', 'a', encoding='utf-8') as GAL, open('arkgal.txt', 'a', encoding='utf-8') as arkgal :
        try: 
            tree = etree.parse(path)
        except:
            print("Problem, path is : " + str(path))
            return 'stop'
        
        #find where the dc:identifier's are and get their ark's
        arks = tree.findall('.//dc:identifier', namespaces={'dc' : "http://purl.org/dc/elements/1.1/", 'oai_dc' : "http://www.openarchives.org/OAI/2.0/oai_dc/" , 'srw' : "http://www.loc.gov/zing/srw/"})
        ocr = tree.findall('.//nqamoyen', namespaces={'dc' : "http://purl.org/dc/elements/1.1/", 'oai_dc' : "http://www.openarchives.org/OAI/2.0/oai_dc/" , 'srw' : "http://www.loc.gov/zing/srw/"})

        arklist = []
        ocrlist = []
        #clean the results
        for i in range(len(arks)): 
            arklist.append(arks[i].text)

        zurlist = [s.strip() for s in arklist]
        zzurlist = []
        for i in zurlist:
            if i.startswith("ISBN"):
            	continue
            else:
                zzurlist.append(i)
        #if ocr rate is too low, reject document
        for i in zzurlist:
            try :
            	if float(ocr[zzurlist.index(i)].text) <= ocr_rate: #change ocr value to change threshold
            		continue
            	else:
                	surlist.append(zzurlist[zzurlist.index(i)])
                	ocrlist.append("{:.2f}".format(float(ocr[zzurlist.index(i)].text)))
            except IndexError :
            	continue
        
        #write down information into text files
        for i, url in enumerate(surlist) :
            if url[-1] != "/":
                surlist[i] = url + "/"
                indgal = "\nDOCUMENT-{}".format(worden + '_' + serial + '_' + str(i)) + " : "
                GAL.write(indgal + "LIEN ARK : " + str(surlist[i]))
                arkgal.write(str(surlist[i]) + str(ocrlist[i]) + "\n")
    return ''
