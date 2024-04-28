chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    fetch('http://localhost:8000/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    })
    .then(response => response.json())
    .then(data => {
        let executableCode = data.result.replace(/```javascript|```/g, '').trim();
        console.log("Final executable code:", executableCode);
        if (executableCode) {
          chrome.tabs.executeScript(sender.tab.id, {code: executableCode});
        } else {
          console.error("Executable code is empty or not valid.");
        }
      })
    .catch(error => console.error('Error:', error));
  });