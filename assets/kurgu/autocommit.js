var timeout = null;
var minlength = 0;


$("#image_query").keyup(function() {
  // clear last timeout check
  clearTimeout(timeout);

  var value = $(this).val();
  var txtbox = $("#image_query").attr("name");
  console.log(txtbox)
  if (value.length >= minlength) {
    //
    // run ajax call 1 second after user has stopped typing
    //
    timeout = setTimeout(function() {
      $.ajax({
        type: "GET",
        url: "https://www.google.com/search",
        data: {
          [txtbox] : value
        },
        dataType: "text",
      });
    }, 1000);
  }});
