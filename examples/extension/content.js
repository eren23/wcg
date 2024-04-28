chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "sendHTML") {
        chrome.runtime.sendMessage({
            html_content: document.documentElement.outerHTML,
            query: `search the model "Mistral 7b" model`,  
            prompt_template: "js"  
        });
    }
});