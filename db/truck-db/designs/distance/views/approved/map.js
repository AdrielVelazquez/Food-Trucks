function(doc) {
    if (doc.approved === true && doc.latitude !== "") {
        for (var key in doc['schedule']['Hours']) {
            var sm_doc = doc['schedule']['Hours'][key];
            for (var time in sm_doc) {
                if (sm_doc[time] === true) {
                    emit([key, time], [doc.name, doc.latitude, doc.longitude]);
                }
            }
          }
    }
}