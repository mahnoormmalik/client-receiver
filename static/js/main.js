function showPopup() {
    document.getElementById('2').style.display = "block";
  }
  
  function syncValueWith2() {
    document.getElementById('2').value = document.getElementById('1').value;
  }
  
  function syncValueWith1() {
    document.getElementById('1').value = document.getElementById('2').value;
  }

