



function getUrlVars() {
	let vars = {};
	let parts = window.location.href.replace(/[?&]+([^=&]+)=([^&#]*)/gi,
		function(m,key,value) {
			vars[key] = value;
		}
	);
	return vars;
}
