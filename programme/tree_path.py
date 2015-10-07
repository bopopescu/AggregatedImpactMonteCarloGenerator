def tree_path(UP, liste, fichier, UP_meta_info, impact_method, CF_categories, all_system_scores, all_unit_scores, CF_units):
	from tree_path import tree_path

	fichier.write("<li ")
	if liste[UP]['parent']=='RF':
		fichier.write("class='origine'")
	fichier.write(">\n	<div>\n")
	
	#--construction de la fiche detaillee.--
	fichier.write("		<div class='fiche")
	if liste[UP]['pruned']==1:
		fichier.write(" pruned")
	else:
		fichier.write(" nopruned")
	fichier.write("' id="+str(UP)+">\n")
	fichier.write("			<img class='exit cible' src='croix.png' width=20 height=20 onclick='cachage("+str(UP)+")'>\n")
	fichier.write("			<h3>"+liste[UP]['process']+"</h3>\n")
	fichier.write("			<span>Demande : "+str("%.3e"% float(liste[UP]['demand']))+" "+UP_meta_info[liste[UP]['process']]['unit']+"</span><br>\n")			
	if UP_meta_info[liste[UP]['process']]['Infrastructure']=='Yes':
		fichier.write("			<span>Infrastructure</span><br>\n")
	fichier.write("			<h3>Impact : </h3>\n")
	if liste[UP]['pruned'] == 1:
		for impact_category in CF_categories: 
			matrix_line = CF_categories.index(impact_category)
			fichier.write("			<span>"+impact_category+" : ")
			fichier.write(str(all_system_scores[matrix_line, liste[UP]['origine']] * liste[UP]['demand'])+" "+CF_units[matrix_line])
			impact_percent=100*all_system_scores[matrix_line,liste[UP]['origine']] * liste[UP]['demand']/(all_system_scores[matrix_line,liste[0]['origine']]*liste[0]['demand'])
			fichier.write(" ("+str(round(impact_percent,3))+"%)</span><br>\n")
	else:	
		for impact_category in CF_categories: 
			matrix_line = CF_categories.index(impact_category)
			fichier.write("			<span>"+impact_category+" : "+str(all_unit_scores[matrix_line, liste[UP]['origine']] * liste[UP]['demand'])+" "+CF_units[matrix_line]+"</span><br>\n")
		fichier.write("			<h3>Impact agregee : </h3>\n")
		for impact_category in CF_categories: 
			matrix_line = CF_categories.index(impact_category)
			fichier.write("			<span>"+impact_category+" : ")
			fichier.write(str(all_system_scores[matrix_line, liste[UP]['origine']] * liste[UP]['demand'])+" "+CF_units[matrix_line])
			if all_system_scores[matrix_line,liste[0]['origine']]==0:
				fichier.write(" (-%)</span><br>\n")
			else:
				impact_percent=100*all_system_scores[matrix_line,liste[UP]['origine']]*liste[UP]['demand']/(all_system_scores[matrix_line,liste[0]['origine']]*liste[0]['demand'])
				fichier.write(" ("+str(int(impact_percent))+"%)</span><br>\n")
	fichier.write("			</div>\n")
	
	# --construction cellule--
	fichier.write("		<a class='cible")
	if liste[UP]['pruned']==1:
		fichier.write(" pruned")
	else:
		fichier.write(" nopruned")
	fichier.write("' onclick=revelation('"+str(UP)+"','inline-block')>\n")
	fichier.write("		"+liste[UP]['process']+"\n		</a>\n")
	
	# --construction fleche pour reveler la suite s'il y a lieu--
	if liste[UP]['pruned']!=1:
		fichier.write("<img id='fleche_b_"+str(UP)+"' src='fleche_bas.png' class='fleche' onclick=revelation('suite"+str(UP)+"','table');cachage('fleche_b_"+str(UP)+"');revelation('fleche_h_"+str(UP)+"','block');>")
		fichier.write("<img id='fleche_h_"+str(UP)+"' src='fleche_haut.png' class='fleche' style='display:none;' onclick=cachage('suite"+str(UP)+"');cachage('fleche_h_"+str(UP)+"');revelation('fleche_b_"+str(UP)+"','block')>")
	
	fichier.write("</div>\n")
	
	# --construction des enfants si il y a lieu
	if liste[UP]['pruned']==0:
		fichier.write("	<ul class='suite' id='suite"+str(UP)+"'>\n")
		for enfant in liste[UP]['enfants']:
			tree_path(enfant,liste,fichier, UP_meta_info, impact_method, CF_categories, all_system_scores, all_unit_scores, CF_units);
		fichier.write("	</ul>\n")
	fichier.write("</li>\n")

