-- [Decide aurora] Script sur WH_Aurora, type Requête : la meilleure fenêtre de chaque zone, GO ou annulation, et la phrase msg pour Teams
WITH s AS (
  SELECT zone, CAST(hour_local AS datetime2(0)) AS h,
         CAST(kp_index AS decimal(3,1)) AS kp, CAST(cloud_pct AS int) AS cl
  FROM LH_Aurora.dbo.sky
),
ok AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY zone ORDER BY kp DESC, cl ASC) AS rn
  FROM s WHERE kp >= 3 AND cl <= 40
),
best AS (SELECT zone, h, kp, cl FROM ok WHERE rn = 1),
b AS (
  SELECT zone, COUNT(*) AS tours, SUM(CAST(booked AS int)) AS pax
  FROM LH_Aurora.dbo.bookings GROUP BY zone
),
k AS (
  SELECT
    (SELECT COUNT(*) FROM best) AS go_zones,
    (SELECT COUNT(*) FROM b) AS zones,
    (SELECT TOP 1 zone FROM best ORDER BY kp DESC, cl ASC) AS top_zone,
    (SELECT TOP 1 CONVERT(varchar(5), h, 108) FROM best ORDER BY kp DESC, cl ASC) AS top_hour,
    (SELECT TOP 1 kp FROM best ORDER BY kp DESC, cl ASC) AS top_kp,
    (SELECT TOP 1 cl FROM best ORDER BY kp DESC, cl ASC) AS top_cloud,
    (SELECT SUM(tours) FROM b WHERE zone IN (SELECT zone FROM best)) AS go_tours,
    (SELECT SUM(pax) FROM b WHERE zone IN (SELECT zone FROM best)) AS go_pax,
    (SELECT STRING_AGG(zone, ', ') FROM b WHERE zone NOT IN (SELECT zone FROM best)) AS cancelled,
    (SELECT SUM(pax) FROM b WHERE zone NOT IN (SELECT zone FROM best)) AS cancelled_pax
)
SELECT *,
  CONCAT('Aurores boréales, nuit du 27 novembre 2026 : GO pour ', go_zones, ' zones sur ', zones, '. ',
    'Meilleure fenêtre : ', top_zone, ' à ', top_hour, ', Kp ', top_kp, ', ', top_cloud, ' % de nuages. ',
    go_tours, ' tours confirmés, ', go_pax, ' voyageurs. ',
    'Annulé : ', cancelled, ' (', cancelled_pax, ' voyageurs, ciel couvert).') AS msg
FROM k;
