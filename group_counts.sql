-- SQL Query for chat_denormalized.db

SELECT
    group_id,
    COUNT(*) AS count
FROM
    message
GROUP BY
    group_id
ORDER BY
    count DESC;
