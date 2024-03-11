
const popup = document.getElementById('popup');
var profile = document.getElementById('profile');
profile.addEventListener('mouseover', () => {    
    popup.style.display = 'block';
    popup.style.cursor ='pointer';
    
});
 
popup.addEventListener('mouseleave', () => {    
    popup.style.display = 'none';
    
});