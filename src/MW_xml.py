import xml.dom.minidom

def hasAttributes(exml, attr):
    for e in attr:
        if not exml.hasAttribute(e):
            return False
    return True

def getAttributeMap(exml):
    data = dict()
    if exml.hasAttributes():
        attr = exml.attributes
        for i in range(0,attr.length):
            if attr.item(i).value.isdigit():
                data[attr.item(i).name] = int(attr.item(i).value)
            else:  data[attr.item(i).name] = attr.item(i).value
    return data


def isXMLElement(node):
    return node.nodeType == 1

def getElementNodes(childList):
    return filter(isXMLElement,childList)

def quickEltNode(filename,tag,attr,value):
    getChildNodeWithAttribute(xml.dom.minidom.parse(filename),tag,attr,value)

def getChildNode(exml,tag,index = 0):
    ret = None
    counter = 0
    for e in exml.getElementsByTagName(tag):
        ret = e
        if index == counter:
            return ret
        counter += 1
    return ret    

def getChildNodeWithAttribute(exml,tag,attr,value,index = 0):
    ret = None
    counter = 0
    for e in exml.getElementsByTagName(tag):
        if e.hasAttribute(attr) and e.getAttribute(attr) == str(value):
            ret = e
            if index == counter:
                return ret
            counter += 1
    return ret