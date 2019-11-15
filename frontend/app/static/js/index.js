function loadDataTable(id) {
    $(document).ready(function() {
        var table = $('#' + id).DataTable( {
            //data: data,
	    "pageLength": 15,
	    "lengthChange": false,
            "order": [[ 5, "desc" ]],
            "pageLength": 15//,
            //columns: [
            //    { title: "Spieler" },
            //    { title: "Follower" },
            //    { title: "Posts" },
            //    { title: "Tweets" },
            //    { title: "Fame" } ]
        } );
    } );
}
