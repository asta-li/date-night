// Inform the background page that this tab should have a page-action.
// chrome.runtime.sendMessage({
//   from: 'content',
//   subject: 'showPageAction',
// });


// https://stackoverflow.com/questions/20019958/chrome-extension-how-to-send-data-from-content-script-to-popup-html
chrome.runtime.onMessage.addListener(async (msg, sender, response) => {
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

    
  // if (request.action === "fillFields") {
  //   console.log("FILL FIELDS!")
  //   $("#user").val("name@email.com")
  //   $("#pw").val("pass123")
  // }
  
  if (msg.from === "popup" && msg.subject === "makeReservation") {
    console.log("makeReservation");
    console.log(window.location.href);

    let time_index = 0;
    for (; time_index < msg.times; ++time_index) {
      let success = False;
      // Try to book this time!
      success = True;
      if (success) {
        break;
      }
    }

    var updated_times = msg.times;
    // Successfully booked a reservation!
    if (time_index < msg.times.length) {
      updated_times.splice(time_index, 1);
    }

    response({
      tabId: msg.to,
      times: updated_times,
      index: msg.index,
      recommendedRestaurants: msg.recommendedRestaurants,
    });
  }
});
