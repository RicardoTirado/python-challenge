// Get references to the tbody element, input field and button
var $tbody = document.querySelector("tbody");
var $dateInput = document.querySelector("#date");
var $cityInput = document.querySelector("#city");
var $stateInput = document.querySelector("#state");
var $countryInput = document.querySelector("#country");
var $shapeInput = document.querySelector("#shape");
var $searchBtn = document.querySelector("#search");

// Add an event listener to the searchButton, call handleSearchButtonClick when clicked
$searchBtn.addEventListener("click", handleSearchButtonClick);

// Set filteredSightings to dataSet initially
var filteredSightings = dataSet;

// renderTable renders the filteredSighting to the tbody
function renderTable() {
  $tbody.innerHTML = "";
  for (var i = 0; i < filteredSightings.length; i++) {
    // Get the current sighting object and its fields
    var sighting = filteredSightings[i];
    var fields = Object.keys(sighting);
    // Create a new row in the tbody, set the index to be i + startingIndex
    var $row = $tbody.insertRow(i);
    for (var j = 0; j < fields.length; j++) {
      // For every field in the sighting object, create a new cell at set its inner text to be the current value at the current sighting's field
      var field = fields[j];
      var $cell = $row.insertCell(j);
      $cell.innerText = sighting[field];
    }
  }
}

function handleSearchButtonClick() {
  // Format the user's search by removing leading and trailing whitespace
  var filterDate = $dateInput.value.trim();
  var filterCity = $cityInput.value.trim().toLowerCase();
  var filterState = $stateInput.value.trim().toLowerCase();
  var filterCountry = $countryInput.value.trim().toLowerCase();
  var filterShape = $shapeInput.value.trim().toLowerCase();

  // Set filteredSightings to an array of all sightings whose "values" matches the filter
  filteredSightings = dataSet.filter(function(sighting) {
    var sightingDate = sighting.datetime;
    var sightingCity = sighting.city;
    var sightingState = sighting.state;
    var sightingCountry = sighting.country;
    var sightingShape = sighting.shape;

    // If true, add the sighting to the filteredSightings, otherwise don't add it to filteredSightings
    return sightingDate === filterDate || sightingCity === filterCity  || 
      sightingState === filterState || sightingCountry === filterCountry || sightingShape === filterShape;
  });
  renderTable();
}

// Render the table for the first time on page load
renderTable();