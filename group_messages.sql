select 
datetime((m.date / 1000000000) + 978307200, 'unixepoch', 'localtime') as TextDate,
m.text,
m.handle_id,
h.id as "Sender",
m.service,
m.is_from_me,
cmj.message_id,
cmj.chat_id,
c.service_name,
c.group_id,
m.associated_message_type
from message m 
left join chat_message_join cmj on m.ROWID = cmj.message_id  
left join chat c on cmj.chat_id = c.ROWID
left join handle h on m.handle_id = h.ROWID 
where c.group_id = 'F10BB39C-461D-4E72-8D4C-8718998118CF'
and m.text is not null
and m.service = c.service_name
order by "date" ASC
