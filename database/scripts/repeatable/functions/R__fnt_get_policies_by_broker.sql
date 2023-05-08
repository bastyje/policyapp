IF EXISTS (SELECT * FROM sysobjects WHERE id = object_id('fntGetPoliciesByBroker') AND xtype IN ('FN', 'IF', 'TF'))
	DROP FUNCTION [dbo].[fntGetPoliciesByBroker]
GO


CREATE FUNCTION [dbo].[fntGetPoliciesByBroker] (@brokerId INT, @isOffer BIT)
RETURNS TABLE
AS
RETURN (
    SELECT
        [p].[Id] AS [PolicyId],
        [r].[Name] AS [Risk],
        [c].[Name] AS [Currency],
        [pr].[StartDate],
        [pr].[EndDate],
        [pr].[Premium],
        [v].[Make],
        [v].[Model],
        [v].[Vin],
        [v].[RegistrationNumber],
        [pe].[Name],
        [pe].[LastName],
        [pe].[Pesel],
        [i].[Name] AS [InsurerName]
    FROM [dbo].[Policy] [p]
    JOIN [dbo].[PolicyRisk] [pr] ON [pr].[PolicyId] = [p].[Id]
    JOIN [dbo].[Vehicle] [v] ON [v].[Id] = [p].[VehicleId]
    JOIN [dbo].[Person] [pe] ON [pe].[Id] = [p].[PersonId]
    JOIN [dbo].[Broker] [b] ON [b].[Id] = [p].[BrokerId]
    JOIN [dbo].[Insurer] [i] ON [i].[Id] = [p].[InsurerId]
    JOIN [dict].[Risk] [r] ON [r].[Id] = [pr].[RiskId]
    JOIN [dict].[Currency] [c] ON [c].[Id] = [pr].[CurrencyId]
    WHERE [b].[Id] = @brokerId AND [p].[IsOffer] = @isOffer
)
GO