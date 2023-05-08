IF EXISTS (SELECT * FROM sysobjects WHERE id = object_id('fntGetPoliciesByVehicle') AND xtype IN ('FN', 'IF', 'TF'))
	DROP FUNCTION [dbo].[fntGetPoliciesByVehicle]
GO


CREATE FUNCTION [dbo].[fntGetPoliciesByVehicle] (@vehicleId INT)
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
        [pe].[Name],
        [pe].[LastName],
        [pe].[Pesel],
        [i].[Name] AS [InsurerName],
        [b].[Name] AS [BrokerName]
    FROM [dbo].[Policy] [p]
    JOIN [dbo].[PolicyRisk] [pr] ON [pr].[PolicyId] = [p].[Id]
    JOIN [dbo].[Vehicle] [v] ON [v].[Id] = [p].[VehicleId]
    JOIN [dbo].[Person] [pe] ON [pe].[Id] = [p].[PersonId]
    JOIN [dbo].[Insurer] [i] ON [i].[Id] = [p].[InsurerId]
    JOIN [dbo].[Broker] [b] ON [b].[Id] = [p].[BrokerId]
    JOIN [dict].[Risk] [r] ON [r].[Id] = [pr].[RiskId]
    JOIN [dict].[Currency] [c] ON [c].[Id] = [pr].[CurrencyId]
    WHERE [v].[Id] = @vehicleId AND [p].[IsOffer] = 0
)
GO