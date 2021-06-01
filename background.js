// Called when the user clicks on the browser action.
// chrome.action.onClicked.addListener(() => {
//   var newURL = "http://stackoverflow.com/";
//   chrome.tabs.create({ url: newURL });
// });

// let color = '#3aa757';

chrome.runtime.onMessage.addListener((msg, sender, response) => {
  // First, validate the message's structure.
  console.log("Background")
  console.log(msg)
  if ((msg.from === 'popup') && (msg.subject === 'DOMInfo')) {
    // Collect the necessary data. 
    // (For your specific requirements `document.querySelectorAll(...)`
    //  should be equivalent to jquery's `$(...)`.)
    alert("Baz")
  }
});

// chrome.runtime.onInstalled.addListener(() => {
//   chrome.storage.sync.set({ color });
//   console.log('Default background color set to %cgreen', `color: ${color}`);
// });

//   // Called when the user clicks on the browser action.
// chrome.browserAction.onClicked.addListener(function(tab) {
//   var newURL = "http://stackoverflow.com/";
//   chrome.tabs.create({ url: newURL });

//   // Send a message to the active tab
//   chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//     var activeTab = tabs[0];
//     chrome.tabs.sendMessage(activeTab.id, {"message": "clicked_browser_action"});
//   });
// });

// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//   if( request.action === "getContent" ) {
//     chrome.tabs.create({"url": request.url});
//   }
// });

