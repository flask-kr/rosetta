function collectTextNodes(tag, element, items) {
    for (var child = element.firstChild; child!==null; child= child.nextSibling) {
        if (child.nodeType === Node.TEXT_NODE) {
            text = child.data.trim()
            if (text) {
                items.push(
                    {
                        tag: tag,
                        text: text,
                        node: child
                    }
                );
            }
        } else if (child.nodeType === Node.ELEMENT_NODE) {
            if (child.nodeName == 'SCRIPT')
                continue;
            if (child.nodeName == 'STYLE')
                continue;

            collectTextNodes(child.nodeName, child, items);
        }
    }
}

function reprElement(element) {
    var items = [];
    collectTextNodes('', element, items);

    var texts = []
    for (var i = 0; i != items.length; i++ ) {
        texts.push(i + ':' + items[i].tag + ':' + items[i].text);
    }

    return texts.join('\n---------------\n');
}

chrome.extension.sendMessage({
    action: "onTextExtracted",
    source: reprElement(document)
});
