
function cachage(id){
	var elem=document.getElementById(id);
	elem.style.display='none';
}

function revelation(id,display){
	var fiche=document.getElementById(id);
	var allelem=document.getElementsByClassName('fiche')
	for (var i = 0; i < allelem.length; ++i) {
		var autrefiche = allelem[i];  
		autrefiche.style.display='none';
	}
	fiche.style.display=display;
}


