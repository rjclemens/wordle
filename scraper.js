var words = document.getElementsByClassName('dl') 
for (let i = 0; i<words.length; i++){ 
  data += (words[i].innerText.substring(0,5) + ","); 
}

