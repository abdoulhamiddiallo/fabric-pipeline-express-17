-- [Contrôle] point de terminaison SQL de LH_Aurora : les heures « GO » de chaque zone (Kp 3 ou plus, 40 % de nuages au plus)
SELECT zone, hour_local, kp_index, cloud_pct
FROM dbo.sky
WHERE CAST(kp_index AS decimal(3,1)) >= 3 AND CAST(cloud_pct AS int) <= 40
ORDER BY zone, hour_local;
