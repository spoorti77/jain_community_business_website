// notification dropdown
function toggleNotificationDropdown() {
    var dropdown = document.getElementById("notificationDropdown");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

// Optional: close dropdown if clicked outside
document.addEventListener("click", function (event) {
    var bell = document.getElementById("notifications");
    var dropdown = document.getElementById("notificationDropdown");
    if (!bell.contains(event.target)) {
        dropdown.style.display = "none";
    }
});
// profile dropdown 
    function toggleProfileDropdown() {
        const dropdown = document.getElementById('profileDropdown');
        dropdown.classList.toggle('open');
    }

    // Close dropdown when clicking outside
    window.addEventListener('click', function(e) {
        const dropdown = document.getElementById('profileDropdown');
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove('open');
        }
    });

    // state and city dropdown code
$(function () {
  let cityData = [];

  $.getJSON("/static/data/cities.json", function (data) {
    cityData = data;
    const states = [...new Set(data.map(item => item.state))].sort();
    states.forEach(state => {
      $('#state').append(new Option(state, state));
    });
  });

  $('#state').on('change', function () {
    const state = this.value;
    const cities = cityData
      .filter(city => city.state === state)
      .map(city => city.name);

    $('#current').autocomplete({
      source: [...new Set(cities)].sort()
    });
  });
});