// Inform the background page that this tab should have a page-action.
// chrome.runtime.sendMessage({
//   from: 'content',
//   subject: 'showPageAction',
// });

// window.onready

// https://stackoverflow.com/questions/20019958/chrome-extension-how-to-send-data-from-content-script-to-popup-html
chrome.runtime.onMessage.addListener((msg, sender, response) => {
  console.log("Content");
  console.log(msg);
  console.log(sender);

  if (msg.from === "popup" && msg.subject === "getPastReservations") {
    console.log("getPastReservations");
    
    // Scrape past reservation links from page.
    const links = [
      "https://www.opentable.com/r/burma-love-san-francisco",
      "https://www.opentable.com/r/nakama-sushi-san-francisco",
      "https://www.opentable.com/otoro-sushi"
    ];
    
    // Send past reservation links back as response.
    // tabId: sender.tab.id
    response({pastReservations: links, tabId: msg.to});
  }

    // chrome.runtime.sendMessage({from: "context", subject: "pastReservations", links: links});

  // if (request.action === "fillFields") {
  //   console.log("FILL FIELDS!")
  //   $("#user").val("name@email.com")
  //   $("#pw").val("pass123")
  // }
  
  if (msg.from === "popup" && msg.subject === "makeReservation") {
    console.log("makeReservation");
    console.log(window.location.href)
    
    // TODO: Get the timeSlots and hours (+/- 0.5 hr) for reservations.
    // chrome.storage.sync.get("color", ({ color }) => {

    for (const restaurant_url of msg.recommendedRestaurants) {
      window.location.href = restaurant_url;
      alert(restaurant_url);
      console.log("RELOADED!");
    }
    alert("RELOADED! DONE!!");
  }
});
