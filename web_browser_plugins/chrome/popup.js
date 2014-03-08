chrome.extension.onMessage.addListener(function(request, sender) {
    if (request.action == "onTextExtracted") {
        message.innerText = request.source;
    }
});

function onWindowLoad() {
    chrome.tabs.executeScript(null, {
            file: "html_text_extractor.js"
        }, function() {
            if (chrome.extension.lastError) {
                var message = document.querySelector('#message');
                message.innerText = 'There was an error injecting script : \n' +
                chrome.extension.lastError.message;
            }
        });
}

window.onload = onWindowLoad;

