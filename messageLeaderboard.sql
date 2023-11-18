SELECT
    m.Sender,
    SUM(CASE WHEN m.associated_message_type = 0 THEN 1 ELSE 0 END) AS NumberOfMessages,
    
    SUM(CASE WHEN m.associated_message_type != 0 THEN 1 ELSE 0 END) AS NumberOfReactions,
    SUM(CASE WHEN m.associated_message_type = 2000 THEN 1 ELSE 0 END) AS LovedCount,
    SUM(CASE WHEN m.associated_message_type = 2001 THEN 1 ELSE 0 END) AS LikedCount,
    SUM(CASE WHEN m.associated_message_type = 2002 THEN 1 ELSE 0 END) AS DislikedCount,
    SUM(CASE WHEN m.associated_message_type = 2003 THEN 1 ELSE 0 END) AS LaughedAtCount,
    SUM(CASE WHEN m.associated_message_type = 2004 THEN 1 ELSE 0 END) AS EmphasizedCount,
    SUM(CASE WHEN m.associated_message_type = 2005 THEN 1 ELSE 0 END) AS QuestionedCount,
    
    SUM(CASE WHEN am.associated_message_type != 0 THEN 1 ELSE 0 END) AS NumberOfReceivedReactions,
    SUM(CASE WHEN am.associated_message_type = 2000 THEN 1 ELSE 0 END) AS LovedReceivedCount,
    SUM(CASE WHEN am.associated_message_type = 2001 THEN 1 ELSE 0 END) AS LikedReceivedCount,
    SUM(CASE WHEN am.associated_message_type = 2002 THEN 1 ELSE 0 END) AS DislikedReceivedCount,
    SUM(CASE WHEN am.associated_message_type = 2003 THEN 1 ELSE 0 END) AS LaughedAtReceivedCount,
    SUM(CASE WHEN am.associated_message_type = 2004 THEN 1 ELSE 0 END) AS EmphasizedReceivedCount,
    SUM(CASE WHEN am.associated_message_type = 2005 THEN 1 ELSE 0 END) AS QuestionedReceivedCount
FROM
    message m
LEFT JOIN message am ON m.guid = am.associated_message_guid
WHERE
    m.group_id = '3738601B-0454-4E66-BBB8-303184AD2760' -- Put the desired group GUID here 
GROUP BY
    m.Sender
ORDER BY
    NumberOfReactions DESC, NumberOfReceivedReactions DESC;
