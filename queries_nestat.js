db.getCollection('load').aggregate([{$group : {_id : "$r_ip",  count : {$sum : 1} }}, {$sort : {count : -1}}])

db.getCollection('load').aggregate([{$group : {_id : "$pname",  count : {$sum : 1} }}, {$sort : {count : -1}}])
