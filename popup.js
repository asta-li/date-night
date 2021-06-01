// Get the submit button object from the popup.
let submitButton = document.getElementById("submitButton");

// chrome.storage.sync.get("color", ({ color }) => {
//   document.body.style.backgroundColor = color;
// });
// }

// When the submit button is clicked, start the workflow.
submitButton.addEventListener("click", async () => {
  // TODO: store options like preferred day of the week, dinner time,
  // and how long into the future to make reservations for.
  let tab = await updateTab("https://www.opentable.com/my/profile/info#reservations-past");

  console.log("Tab updated " + tab.id);
  console.log("Sending message to content getPastReservations.");

  // const handlePastReservationsTab = handlePastReservations.bind(tab.id);
  chrome.tabs.sendMessage(
    tab.id,
    {from: "popup", to: tab.id, subject: "getPastReservations"},
    handlePastReservations);
});

const handlePastReservations = async (response) => {
  console.log("handlePastReservations");
  console.log(response);
  if(chrome.runtime.lastError) {
    console.log("Error in handlePastReservations");
    return;
  }
  // response.pastReservations
  // Make API call to get restaurant recommendations given past reservations.
  // Recommendations are sorted in order of recommendation score.
  let recommendedRestaurants = [
    "https://www.opentable.com/r/burma-love-san-francisco",
    "https://www.opentable.com/r/nakama-sushi-san-francisco",
    "https://www.opentable.com/otoro-sushi"
  ];

  // TODO: maybe move this to content worker.
  var timeSlots = [];
  // Get day of the week and the number of timeslots from the options.
  // TODO: Special-case for today but before or after the cut-off: Date().getHours()
  const numWeeks = 4;
  const dateDay = 3;  // Wednesday
  for (var i = 1; i <= numWeeks; ++i) {
    timeSlots.push(nextDate(dateDay, i));
  }
  console.log(timeSlots);

  // TODO: Get the timeSlots and hours (+/- 0.5 hr) for reservations.
  // chrome.storage.sync.get("color", ({ color }) => {

  let tab = await updateTab(recommendedRestaurants[0]);
  console.log("Loaded: " + recommendedRestaurants[0]);
  
  chrome.tabs.sendMessage(
    response.tabId,
    {
      from: "popup", 
      to: response.tabId,
      subject: "makeReservation", 
      index: 0,
      recommendedRestaurants: recommendedRestaurants,
      times: timeSlots
    },
    makeReservations);
};

const makeReservations = async (response) => {
  console.log("makeReservations");
  console.log(response);
  if (chrome.runtime.lastError) {
    console.log("Error in makeReservations");
    return;
  }

  if (response.times.length == 0) {
    console.log("DONE MAKING RESERVATIONS!");
    return;
  }

  let index = response.index + 1;

  if (index >= response.recommendedRestaurants.length) {
    console.log("REACHED END OF RESTAURANTS LIST!");
    return;
  }

  let tab = await updateTab(response.recommendedRestaurants[index]);
  console.log("Loaded: " + response.recommendedRestaurants[index]);
  
  chrome.tabs.sendMessage(
    response.tabId,
    {
      from: "popup", 
      to: response.tabId,
      subject: "makeReservation", 
      index: index,
      recommendedRestaurants: response.recommendedRestaurants,
      times: response.times
    },
    makeReservations);
};

// chrome.runtime.onMessage.addListener((msg, sender, response) => {
//   if ((msg.from === "content") && (msg.subject === "pastReservations")) {
//     if (msg.index === msg.links.length) {
//       // We reached the end of our list.
//       console.log("Done with list!");
//     }

//     // Navigate to the next reservation in the list.
//     chrome.tabs.update({
//       url: msg.links[msg.index]
//     }, tab => {
//       // Now that we're on the next reservation page, send a 
//       let next_msg = {from: msg.from, subject: msg.subject, links: msg.links, index: msg.index + 1}
//       chrome.tabs.sendMessage(
//         tab.id,
//         {from: "popup", subject: "makeReservation", next_msg: next_msg});
//     });

  // let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  // chrome.scripting.executeScript({
  //   target: { tabId: tab.id },
  //   function: setPageBackgroundColor,
  // });
  // });

function updateTab(url) {
  return new Promise(resolve => {
    chrome.tabs.update({url}, async tab => {
      chrome.tabs.onUpdated.addListener(function listener (tabId, info) {
        if (info.status === "complete" && tabId === tab.id) {
          chrome.tabs.onUpdated.removeListener(listener);
          resolve(tab);
        }
      });
    });
  });
}

// The body of this function will be executed as a content script inside the
// current page
function setPageBackgroundColor() {
  chrome.storage.sync.get("color", ({ color }) => {
    document.body.style.backgroundColor = color;
  });
}

// Returns the next date that matches the requested day of the week.
// targetDay is an integer corresponding to the days of the week: {Sun: 0, Mon: 1, ..., Sat: 6}
// weekIncrement is an integer corresponding to the number of weeks into the future, minimum 0.
function nextDate(targetDay, weekIncrement) {
  // var days = {
  //   sunday: 0
  //   monday: 1,
  //   tuesday: 2,
  //   wednesday: 3,
  //   thursday: 4,
  //   friday: 5,
  //   saturday: 6,
  // };
  let now = new Date();    
  now.setDate(now.getDate() + weekIncrement * 7 + (7 + targetDay - now.getDay()) % 7);
  return now;
}