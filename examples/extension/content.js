chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "sendHTML") {
        console.log("Received message from popup.js:", request);
        chrome.runtime.sendMessage({
            html_content: document.documentElement.outerHTML,
            query: request.query,  
            prompt_template: "js"  
        });
    }
});