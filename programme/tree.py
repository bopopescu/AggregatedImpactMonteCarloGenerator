def tree(liste,UP_meta_info, impact_method, CF_categories, all_system_scores, all_unit_scores, impact_units, path):
	from tree_path import tree_path
	import os
	
	
	name=""
	for UP in liste:
		if liste[UP]['parent']=='RF':
			name=str(liste[UP]['origine'])
	fichier = open(os.path.join(path,name+".html"), "w")
		
	fichier.write("<html>\n")
	fichier.write("	<head>\n		<meta content='text/html; charset=utf-8' http-equiv='Content-Type'></meta>\n		<link href='style.css' type='text/css' rel='stylesheet'></link>\n		<script src='script.js'></script>\n</head>\n")
	fichier.write("	<body>\n")
	fichier.write("		<div class='tree'>\n")
	fichier.write("			<ul>\n	")
	for UP in liste:
		if liste[UP]['parent']=='RF':
			
			tree_path(UP,liste, fichier, UP_meta_info, impact_method, CF_categories, all_system_scores, all_unit_scores, impact_units)
	
	fichier.write("			</ul>\n")
	fichier.write("		</div>\n")
	fichier.write("	</body>\n")
	fichier.write("</html>")

	fichier.close()
