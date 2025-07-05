
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
  