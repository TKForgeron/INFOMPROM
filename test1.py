


SELECT *
FROM df1
WHERE `Incident ID` IN (SELECT `Incident ID`
                    from df1 
                    where `Incident ID` in ( select `Incident ID`  
                        from df1
                        where Activity = 'Open') 
                        AND `Incident ID` in ( select `Incident ID`  
                        from df1
                        where Activity = 'Close')
                    )
            AND `Incident ID` NOT IN(select `Incident ID`
                    from df1 
                    where Activity = 'Open' and `Incident ID` in (
                                        select REOPEN.`Incident ID`
                                        FROM
                                            (select `Incident ID`,MAX(ActivityTimeStamp) AS ActivityTimeStamp,Activity
                                            from df1
                                            where  Activity = 'Re-open'
                                            GROUP BY `Incident ID`,Activity) REOPEN   
                                            JOIN
                                            (select `Incident ID`,MAX(ActivityTimeStamp) AS ActivityTimeStamp,Activity
                                            from df1
                                            where  Activity = 'Close'
                                            GROUP BY `Incident ID`,Activity) CLOSE
                                            ON REOPEN.`Incident ID`=CLOSE.`Incident ID` AND TO_TIMESTAMP(REOPEN.ActivityTimeStamp,'yyyy-mm-dd hh24:mi:ss.ff')>TO_TIMESTAMP(CLOSE.ActivityTimeStamp,'yyyy-mm-dd hh24:mi:ss.ff')
                                            ))
