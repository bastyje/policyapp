IF EXISTS (SELECT * FROM sysobjects WHERE id = object_id('fntGetPremiumCountByInsurer') AND xtype IN ('FN', 'IF', 'TF'))
	DROP FUNCTION [dbo].[fntGetPremiumCountByInsurer]
GO


CREATE FUNCTION [dbo].[fntGetPremiumCountByInsurer] (@insurerId INT)
RETURNS TABLE
AS
RETURN (
    SELECT
        [p].[Id] AS [PolicyId],
        [r].[Name] AS [Risk],
        [c].[Name] AS [Currency],
        SUM([pr].[Premium]) AS [PremiumSum],
        [pe].[Name],
        [pe].[LastName],
        [pe].[Pesel],
        [v].[Make],
        [v].[Model],
        [v].[Vin],
        [v].[RegistrationNumber],
        [b].[Name] AS [BrokerName]
    FROM [dbo].[Policy] [p]
    JOIN [dbo].[PolicyRisk] [pr] ON [pr].[PolicyId] = [p].[Id]
    JOIN [dbo].[Vehicle] [v] ON [v].[Id] = [p].[VehicleId]
    JOIN [dbo].[Person] [pe] ON [pe].[Id] = [p].[PersonId]
    JOIN [dbo].[Insurer] [i] ON [i].[Id] = [p].[InsurerId]
    JOIN [dbo].[Broker] [b] ON [b].[Id] = [p].[BrokerId]
    JOIN [dict].[Risk] [r] ON [r].[Id] = [pr].[RiskId]
    JOIN [dict].[Currency] [c] ON [c].[Id] = [pr].[CurrencyId]
    WHERE [v].[Id] = 1 AND [p].[IsOffer] = 0
    GROUP BY
        [p].[Id],
        [r].[Name],
        [c].[Name],
        [pe].[Name],
        [pe].[LastName],
        [pe].[Pesel],
        [v].[Make],
        [v].[Model],
        [v].[Vin],
        [v].[RegistrationNumber],
        [b].[Name]
)
GO