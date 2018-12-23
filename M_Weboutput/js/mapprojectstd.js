$( function() {
    var availableTags = city_array

    $( "#form-city" ).autocomplete({
      source: availableTags
    });
  } );
