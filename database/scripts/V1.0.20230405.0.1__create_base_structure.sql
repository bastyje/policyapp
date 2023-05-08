CREATE SCHEMA [conf];
GO

CREATE TABLE [dbo].[Insurer] (
    [Id] INT NOT NULL,
    [Name] NVARCHAR(128) NOT NULL,
    [Krs] CHAR(10) NOT NULL,
    [TaxId] CHAR(10) NOT NULL,
    CONSTRAINT [PK__Insurer] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [conf].[PolicyOfferTemplate] (
    [Id] INT NOT NULL,
    [Name] NVARCHAR(128) NOT NULL,
    [InsurerId] INT NOT NULL CONSTRAINT FK__PolicyOfferTemplate_Insurer REFERENCES [dbo].[Insurer](Id),
    [QuotationAlgorithm] NVARCHAR(MAX) NOT NULL,
    [ValidFrom] DATETIME2 NOT NULL,
    [ValidTo] DATETIME2 NULL
    CONSTRAINT [PK__PolicyOfferTemplate] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE SCHEMA [dict];
GO

CREATE TABLE [dict].[Currency] (
    [Id] INT NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    CONSTRAINT [PK__Currency] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

INSERT INTO dict.Currency (Id, Name) VALUES (1, N'EUR');
INSERT INTO dict.Currency (Id, Name) VALUES (2, N'PLN');
INSERT INTO dict.Currency (Id, Name) VALUES (3, N'USD');
GO

CREATE TABLE [dict].[Risk] (
    [Id] INT NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    CONSTRAINT [PK__Risk] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

INSERT INTO dict.Risk (Id, Name) VALUES (1, N'TPL');
INSERT INTO dict.Risk (Id, Name) VALUES (2, N'CASCO');
INSERT INTO dict.Risk (Id, Name) VALUES (3, N'ASSISTANCE');
INSERT INTO dict.Risk (Id, Name) VALUES (4, N'GAP');
GO

CREATE SCHEMA [security];
GO

CREATE TABLE [security].[User] (
    [Id] INT NOT NULL,
    [ApiKey] VARCHAR(512) NOT NULL,
    CONSTRAINT [PK__User] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Broker] (
    [Id] INT NOT NULL,
    [Name] NVARCHAR(128) NOT NULL,
    [UserId] INT NOT NULL CONSTRAINT FK__Broker_User REFERENCES [security].[User](Id),
    CONSTRAINT [PK__Broker] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Person] (
    [Id] INT NOT NULL,
    [Name] NVARCHAR(128) NOT NULL,
    [LastName] NVARCHAR(128) NOT NULL,
    [BirthDate] DATETIME2 NULL,
    [Pesel] CHAR(11) NOT NULL,
    [Email] NVARCHAR(128),
    [PhoneNumber] VARCHAR(9),
    CONSTRAINT [PK__Person] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Vehicle] (
    [Id] INT NOT NULL,
    [Make] NVARCHAR(64) NOT NULL,
    [Model] NVARCHAR(64) NOT NULL,
    [RegistrationNumber] VARCHAR(16) NOT NULL,
    [Vin] CHAR(17) NOT NULL,
    [ProductionYear] INT NOT NULL,
    [RegistrationDate] DATETIME2 NOT NULL,
    [OwnerCount] INT NOT NULL,
    CONSTRAINT [PK__Vehicle] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Policy] (
    [Id] INT NOT NULL,
    [VehicleId] INT NOT NULL CONSTRAINT FK__Policy_Vehicle REFERENCES [dbo].[Vehicle](Id),
    [InsurerId] INT NOT NULL CONSTRAINT FK__Policy_Insurer REFERENCES [dbo].[Insurer](Id),
    [BrokerId] INT NOT NULL CONSTRAINT FK__Policy_Broker REFERENCES [dbo].[Broker](Id),
    [PersonId] INT NOT NULL CONSTRAINT FK__Policy_Person REFERENCES [dbo].[Person](Id),
    [OfferId] INT NULL CONSTRAINT FK__Policy_Policy REFERENCES [dbo].[Policy](Id),
    [CreationDate] DATETIME2 NOT NULL,
    [IsOffer] BIT DEFAULT 0 NOT NULL,
    [Version] INT DEFAULT 1 NOT NULL,
    CONSTRAINT [PK__Policy] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[PolicyRisk] (
    [Id] INT NOT NULL,
    [PolicyId] INT NOT NULL CONSTRAINT FK__PolicyRisk_Policy REFERENCES [dbo].[Policy](Id),
    [CurrencyId] INT NOT NULL CONSTRAINT FK__PolicyRisk_Currency REFERENCES [dict].[Currency](Id),
    [RiskId] INT NOT NULL CONSTRAINT FK__PolicyRisk_Risk REFERENCES [dict].[Risk](Id),
    [CreationDate] DATETIME2 NOT NULL,
    [StartDate] DATETIME2 NOT NULL,
    [EndDate] DATETIME2 NOT NULL,
    [Premium] DECIMAL(20, 2) NOT NULL,
    CONSTRAINT [PK__PolicyRisk] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO