import sys, zipfile, re
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
RPR=['rStyle','rFonts','b','bCs','i','iCs','caps','smallCaps','strike','dstrike','outline','shadow','emboss','imprint','noProof','snapToGrid','vanish','webHidden','color','spacing','w','kern','position','sz','szCs','highlight','u','effect','bdr','shd','fitText','vertAlign','rtl','cs','em','lang','eastAsianLayout','specVanish','oMath']
PPR=['pStyle','keepNext','keepLines','pageBreakBefore','framePr','widowControl','numPr','suppressLineNumbers','pBdr','shd','tabs','suppressAutoHyphens','kinsoku','wordWrap','overflowPunct','topLinePunct','autoSpaceDE','autoSpaceDN','bidi','adjustRightInd','snapToGrid','spacing','ind','contextualSpacing','mirrorIndents','suppressOverlap','jc','textDirection','textAlignment','textboxTightWrap','outlineLvl','divId','cnfStyle','rPr','sectPr','pPrChange']
z=zipfile.ZipFile(sys.argv[1])
root=etree.fromstring(z.read('word/document.xml'))
bad=0
for tag,order in (('rPr',RPR),('pPr',PPR)):
    for el in root.iter(W+tag):
        names=[c.tag.replace(W,'') for c in el if c.tag.startswith(W)]
        idx=[order.index(n) if n in order else -1 for n in names]
        known=[i for i in idx if i>=0]
        if known!=sorted(known) or len(set(names))!=len(names):
            bad+=1
            if bad<=8: print(tag, names)
print('elementos fuera de orden o duplicados:', bad)
