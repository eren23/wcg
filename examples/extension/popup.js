document.getElementById('sendContent').addEventListener('click', function() {
    var query = document.getElementById('queryInput').value;
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "sendHTML", query: query});
    });
});