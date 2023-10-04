// leagues.js

$(document).ready(function() {
  // Function to load predictions into the "Predictions" tab content
  function loadPredictions(leagueId) {
    // Make an AJAX request to fetch user predictions for the league
    $.ajax({
      url: "{% url 'predictions' league_id=leagueId %}",
      method: 'GET',
      success: function(data) {
        // Inject the fetched predictions into the "Predictions" tab content
        $('#predictions').html(data);
      },
      error: function(error) {
        console.error('Error fetching predictions:', error);
      }
    });
  }

  // Event handler for when the "Predictions" tab is clicked
  $('#predictions-tab').on('click', function() {
    const leagueId = /* Retrieve the league ID from your template */;
    loadPredictions(leagueId);
  });
});
