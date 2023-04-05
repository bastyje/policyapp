CREATE SCHEMA [conf];
GO

CREATE TABLE [dbo].[Insurer] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Name] NVARCHAR(128) NOT NULL,
    [Krs] CHAR(10) NOT NULL,
    [TaxId] CHAR(9) NOT NULL,
    CONSTRAINT [PK__Insurer] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE conf.PolicyOfferTemplate (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    [InsurerId] INT NOT NULL CONSTRAINT FK__PolicyOfferTemplate_Insurer REFERENCES [dbo].[Insurer](Id),
    [QuotationAlgorithm] NVARCHAR(MAX) NOT NULL,
    [ValidFrom] DATETIMEOFFSET NOT NULL,
    [ValidTo] DATETIMEOFFSET NULL
    CONSTRAINT [PK__PolicyOfferTemplate] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE SCHEMA [dict];
GO

CREATE TABLE [dict].[Currency] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    CONSTRAINT [PK__Currency] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dict].[CustomerType] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    CONSTRAINT [PK__CustomerType] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dict].[PolicyObjectType] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    CONSTRAINT [PK__PolicyObjectType] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dict].[Risk] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    CONSTRAINT [PK__Risk] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Company] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    [Krs] CHAR(10) NOT NULL,
    [TaxId] CHAR(9) NOT NULL,
    CONSTRAINT [PK__Company] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE SCHEMA [security];
GO

CREATE TABLE [security].[User] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [ApiKeyHash] VARCHAR(512) NOT NULL,
    [FailedAttempts] INT DEFAULT 0 NOT NULL,
    [LockoutEnd] DATETIMEOFFSET NULL,
    CONSTRAINT [PK__User] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Broker] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    [UserId] INT NOT NULL CONSTRAINT FK__Broker_User REFERENCES [security].[User](Id),
    CONSTRAINT [PK__Broker] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Person] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Name] VARCHAR(128) NOT NULL,
    [LastName] VARCHAR(128) NOT NULL,
    [BirthDate] DATETIMEOFFSET NULL,
    [Pesel] CHAR(11) NOT NULL,
    [Email] VARCHAR(128),
    [PhoneNumber] VARCHAR(9),
    CONSTRAINT [PK__Person] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Customer] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [CustomerId] INT NOT NULL,
    [CustomerTypeId] INT NOT NULL CONSTRAINT FK__Customer_CustomerType REFERENCES [dict].[CustomerType](Id),
    CONSTRAINT [PK__Customer] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[PolicyObject] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [PolicyObjectId] INT NOT NULL,
    [PolicyObjectTypeId] INT NOT NULL CONSTRAINT FK__PolicyObject_PolicyObjectType REFERENCES [dict].[PolicyObjectType](Id),
    CONSTRAINT [PK__PolicyObject] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Policy] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [PolicyObjectId] INT NOT NULL CONSTRAINT FK__Policy_PolicyObject REFERENCES [dbo].[PolicyObject](Id),
    [InsurerId] INT NOT NULL CONSTRAINT FK__Policy_Insurer REFERENCES [dbo].[Insurer](Id),
    [CreationDate] DATETIMEOFFSET NOT NULL,
    [IsOffer] BIT DEFAULT 0 NOT NULL,
    [Version] INT DEFAULT 1 NOT NULL,
    CONSTRAINT [PK__Policy] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[PolicyRisk] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [PolicyObjectId] INT NOT NULL CONSTRAINT FK__PolicyRisk_Policy REFERENCES [dbo].[Policy](Id),
    [CurrencyId] INT NOT NULL CONSTRAINT FK__PolicyRisk_Currency REFERENCES [dict].[Currency](Id),
    [RiskId] INT NOT NULL CONSTRAINT FK__PolicyRisk_Risk REFERENCES [dict].[Risk](Id),
    [CreationDate] DATETIMEOFFSET NOT NULL,
    [StartDate] DATETIMEOFFSET NOT NULL,
    [EndDate] DATETIMEOFFSET NOT NULL,
    [Premium] INT NOT NULL,
    CONSTRAINT [PK__PolicyRisk] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Property] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [ConstructionYear] INT NOT NULL,
    [AntiTheftWindows] BIT NOT NULL,
    [Country] VARCHAR(3) NOT NULL,
    [City] VARCHAR(128) NOT NULL,
    [Street] VARCHAR(128) NOT NULL,
    [Number] VARCHAR(8) NOT NULL,
    [PostalCode] CHAR(6) NOT NULL,
    CONSTRAINT [PK__Property] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO

CREATE TABLE [dbo].[Vehicle] (
    [Id] INT IDENTITY (1, 1) NOT NULL,
    [Make] VARCHAR(64) NOT NULL,
    [Model] VARCHAR(64) NOT NULL,
    [RegistrationNumber] VARCHAR(16) NOT NULL,
    [Vin] CHAR(17) NOT NULL,
    [ProductionYear] INT NOT NULL,
    [RegistrationDate] DATETIMEOFFSET NOT NULL,
    [OwnerCount] INT NOT NULL,
    CONSTRAINT [PK__Vehicle] PRIMARY KEY CLUSTERED ([Id] ASC)
);
GO