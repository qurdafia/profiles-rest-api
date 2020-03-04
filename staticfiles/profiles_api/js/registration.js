/* Disable registration if PDPA is unchecked */
var reg_but = document.getElementById('reg-submit');
reg_but.disabled = true;
reg_but.style.backgroundColor = "#bbb";

function lockReg() {
  var reg_but = document.getElementById('reg-submit');
  var pdpa = document.getElementById('id_is_pdpa_checked');

  if (pdpa.checked === false) {
    reg_but.disabled = true;
    reg_but.style.backgroundColor = "#bbb";
  } else if (pdpa.checked === true) {
    reg_but.disabled = false;
    reg_but.style.backgroundColor = "rgba(255, 51, 51, 1)";
  }
}

/* Validate if Name is provided */

var file_input = document.getElementById('id_photo');
file_input.disabled = true;
function unlockFile() {
  var name = document.getElementById('id_name');
  var file_input = document.getElementById('id_photo');
  if (name.value !== "") {
    file_input.disabled = false;
  } else {
    file_input.disabled = true;
  }
}

/* Validate NRIC / Fin */

function validate(ic) {
  var icArray = new Array(9);
  for (i = 0; i < 9; i++) {
    icArray[i] = ic.charAt(i);
  }
  icArray[1] *= 2;
  icArray[2] *= 7;
  icArray[3] *= 6;
  icArray[4] *= 5;
  icArray[5] *= 4;
  icArray[6] *= 3;
  icArray[7] *= 2;
  var weight = 0;
  for (i = 1; i < 8; i++) {
    weight += parseInt(icArray[i]);
  }
  var offset = (icArray[0] == "T" || icArray[0] == "G") ? 4 : 0;
  var temp = (offset + weight) % 11;
  var st = Array("J", "Z", "I", "H", "G", "F", "E", "D", "C", "B", "A");
  var fg = Array("X", "W", "U", "T", "R", "Q", "P", "N", "M", "L", "K");
  var theAlpha;
  if (icArray[0] == "S" || icArray[0] == "T") {
    theAlpha = st[temp];
  } else if (icArray[0] == "F" || icArray[0] == "G") {
    theAlpha = fg[temp];
  }
  return (icArray[8] == theAlpha);
}


valIcon = $('#validateIcon');
  $('#id_nric_number').change(function() {
    var nric_num = $(this).val();
    nric_num = nric_num.replace(/[^0-9 a-z A-Z]+/g, "").replace(/(^\s||\s$)+/, "").toUpperCase();
    $(this).val(nric_num);
    valIcon.removeClass("valid").attr("title", "Not Valid!");
    if (nric_num.length == 9 && validate(nric_num)) {
       valIcon.addClass("valid").attr("title", "Valid!");
    } else {
      alert('Invalid NRIC/FIN, must provide a correct one.');
      $(this).val("");
    }
  }).click(function() {
    $(this).select();
  });
